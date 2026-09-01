#!/usr/bin/env python3
"""Safely stage and audit Kosmograd P0 experiment fixtures.

The harness never creates Steam Workshop items. It only manages files declared
by experiments/p0/manifest.json inside an existing direct child of a
``workshop_wip`` directory. Steam-owned metadata and unrelated files are kept.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "experiments" / "p0" / "manifest.json"
MANAGED_FILE = ".kosmograd-p0-managed.json"
MANAGED_COMMENT = "# Managed by tools/p0_harness.py"
OBJECT_RE = re.compile(r"^\$OBJECT_(BUILDING|VEHICLE)\s+(\S+)\s*$")
DLC_PATH_RE = re.compile(
    r"(?:^|[^A-Za-z0-9_])(?:cwc|dlc[^/\\\s]*)(?:[/\\]|$)", re.IGNORECASE
)
ABSOLUTE_PATH_RE = re.compile(r"(?:^|\s)(?:[A-Za-z]:[/\\]|/)[^\s]+")
REFERENCE_RE = re.compile(r"(?P<path>[^\s\"']+\.(?:nmf|mtl|dds|ini))", re.IGNORECASE)


class HarnessError(RuntimeError):
    """Expected, user-actionable harness failure."""


@dataclass(frozen=True)
class Target:
    path: Path
    kinds: frozenset[str]
    layout: str


def _load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise HarnessError(f"manifest not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise HarnessError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise HarnessError(f"unsupported manifest schema in {path}")
    return data


def _safe_relative(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or not path.parts or ".." in path.parts:
        raise HarnessError(f"unsafe relative path in manifest: {value}")
    return path


def validate_wip_path(path: Path) -> Path:
    expanded = path.expanduser()
    if expanded.is_symlink():
        raise HarnessError(f"refusing symlink WIP target: {expanded}")
    resolved = expanded.resolve()
    if resolved.parent.name != "workshop_wip" or resolved.name in {"", ".", ".."}:
        raise HarnessError(
            f"refusing target outside a direct workshop_wip child: {resolved}"
        )
    if not resolved.is_dir():
        raise HarnessError(f"WIP directory does not exist: {resolved}")
    config = resolved / "workshopconfig.ini"
    if not config.is_file():
        raise HarnessError(
            f"missing Steam-created workshopconfig.ini in {resolved}; create the private item first"
        )
    return resolved


def _variant(manifest: dict[str, Any], spike: str, variant: str) -> dict[str, Any]:
    spike_key = spike.upper()
    spikes = manifest.get("spikes", {})
    try:
        variants = spikes[spike_key]["variants"]
        selected = variants[variant]
    except (KeyError, TypeError) as exc:
        available = ", ".join(sorted(spikes))
        raise HarnessError(
            f"unknown spike/variant {spike_key}/{variant}; spikes: {available}"
        ) from exc
    if not isinstance(selected, dict) or not isinstance(selected.get("objects"), list):
        raise HarnessError(f"invalid variant definition for {spike_key}/{variant}")
    return selected


def _objects(
    manifest: dict[str, Any], selected: dict[str, Any]
) -> list[tuple[str, dict[str, Any]]]:
    catalog = manifest.get("objects", {})
    result: list[tuple[str, dict[str, Any]]] = []
    for object_id in selected["objects"]:
        try:
            spec = catalog[object_id]
        except KeyError as exc:
            raise HarnessError(f"unknown object in manifest: {object_id}") from exc
        if spec.get("kind") not in {"building", "vehicle"}:
            raise HarnessError(f"invalid kind for {object_id}")
        result.append((object_id, spec))
    return result


def _source_root(manifest_path: Path, spec: dict[str, Any]) -> Path:
    relative = _safe_relative(str(spec["source"]))
    return (manifest_path.parent / relative).resolve()


def _check_sources(
    manifest_path: Path,
    objects: Iterable[tuple[str, dict[str, Any]]],
    overlays: dict[str, str],
) -> None:
    missing: list[str] = []
    for object_id, spec in objects:
        source = _source_root(manifest_path, spec)
        if not source.is_dir():
            missing.append(str(source))
            continue
        for required in spec.get("required", []):
            candidate = source / _safe_relative(str(required))
            if not candidate.is_file():
                missing.append(str(candidate))
        overlay_value = overlays.get(object_id)
        if overlay_value:
            overlay = (manifest_path.parent / _safe_relative(overlay_value)).resolve()
            if not overlay.is_dir():
                missing.append(str(overlay))
    if missing:
        rendered = "\n- ".join(missing)
        raise HarnessError(
            "fixture is not delivery-ready; complete Blender/ModelViewer outputs:\n- "
            + rendered
        )


def _managed_state(wip: Path) -> dict[str, Any]:
    path = wip / MANAGED_FILE
    if not path.exists():
        return {"paths": [], "object_lines": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise HarnessError(f"invalid prior managed manifest: {path}") from exc
    return data


def _remove_managed(wip: Path, state: dict[str, Any]) -> None:
    for value in state.get("paths", []):
        relative = _safe_relative(str(value))
        target = wip / relative
        if target.is_symlink():
            raise HarnessError(f"refusing to remove managed symlink: {target}")
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()


def _rewrite_config(wip: Path, old_lines: Iterable[str], new_lines: list[str]) -> None:
    config = wip / "workshopconfig.ini"
    original = config.read_text(encoding="utf-8")
    old = {line.strip() for line in old_lines}
    kept = [
        line
        for line in original.splitlines()
        if line.strip() not in old and line.strip() != MANAGED_COMMENT
    ]
    while kept and not kept[-1].strip():
        kept.pop()
    content = "\n".join(kept)
    if new_lines:
        content += f"\n\n{MANAGED_COMMENT}\n" + "\n".join(new_lines)
    config.write_text(content + "\n", encoding="utf-8")


def _destination(object_id: str, kind: str, layout: str) -> Path:
    if layout == "nested":
        return Path("buildings" if kind == "building" else "vehicles") / object_id
    return Path(object_id)


def _copy_overlay(source: Path, destination: Path) -> None:
    for path in sorted(source.rglob("*")):
        if path.is_dir():
            continue
        relative = path.relative_to(source)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def _stage_target(
    *,
    target: Target,
    manifest_path: Path,
    manifest: dict[str, Any],
    spike: str,
    variant: str,
    selected: dict[str, Any],
) -> None:
    wip = validate_wip_path(target.path)
    objects = [
        (object_id, spec)
        for object_id, spec in _objects(manifest, selected)
        if spec["kind"] in target.kinds
    ]
    overlays = selected.get("overlays", {})
    _check_sources(manifest_path, objects, overlays)

    prior = _managed_state(wip)
    _remove_managed(wip, prior)

    managed_paths: list[str] = []
    object_lines: list[str] = []
    for object_id, spec in objects:
        kind = spec["kind"]
        relative = _destination(object_id, kind, target.layout)
        destination = wip / relative
        shutil.copytree(_source_root(manifest_path, spec), destination)
        overlay_value = overlays.get(object_id)
        if overlay_value:
            overlay = (manifest_path.parent / _safe_relative(overlay_value)).resolve()
            _copy_overlay(overlay, destination)
        managed_paths.append(relative.as_posix())
        token = "BUILDING" if kind == "building" else "VEHICLE"
        object_lines.append(f"$OBJECT_{token} {relative.as_posix()}")

    _rewrite_config(wip, prior.get("object_lines", []), object_lines)
    state = {
        "schema_version": 1,
        "spike": spike.upper(),
        "variant": variant,
        "layout": target.layout,
        "paths": managed_paths,
        "object_lines": object_lines,
    }
    (wip / MANAGED_FILE).write_text(
        json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def stage(
    *,
    manifest_path: Path,
    spike: str,
    variant: str,
    layout: str,
    wip: Path,
    vehicle_wip: Path | None = None,
) -> list[Path]:
    manifest_path = manifest_path.resolve()
    manifest = _load_json(manifest_path)
    selected = _variant(manifest, spike, variant)
    if layout == "split":
        if vehicle_wip is None:
            raise HarnessError("--vehicle-wip is required with --layout split")
        targets = [
            Target(wip, frozenset({"building"}), "flat"),
            Target(vehicle_wip, frozenset({"vehicle"}), "flat"),
        ]
    else:
        if vehicle_wip is not None:
            raise HarnessError("--vehicle-wip is valid only with --layout split")
        targets = [Target(wip, frozenset({"building", "vehicle"}), layout)]
    resolved_targets = [validate_wip_path(target.path) for target in targets]
    if len(set(resolved_targets)) != len(resolved_targets):
        raise HarnessError("split layout requires two different WIP directories")
    # Preflight every target before changing either side of a split stage.
    all_objects = _objects(manifest, selected)
    overlays = selected.get("overlays", {})
    for target in targets:
        applicable = [item for item in all_objects if item[1]["kind"] in target.kinds]
        _check_sources(manifest_path, applicable, overlays)
    for target in targets:
        _stage_target(
            target=target,
            manifest_path=manifest_path,
            manifest=manifest,
            spike=spike,
            variant=variant,
            selected=selected,
        )
    return [validate_wip_path(target.path) for target in targets]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_hash(paths: Iterable[Path], base: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted((p for p in paths if p.is_file()), key=lambda p: p.as_posix()):
        relative = path.relative_to(base).as_posix().encode("utf-8")
        digest.update(relative + b"\0" + bytes.fromhex(sha256_file(path)))
    return digest.hexdigest()


def _detect_game_root() -> Path | None:
    configured = os.environ.get("KOSMOGRAD_GAME_ROOT")
    candidates = [
        Path(configured).expanduser() if configured else None,
        Path.home() / ".steam/steam/steamapps/common/SovietRepublic",
        Path.home() / ".local/share/Steam/steamapps/common/SovietRepublic",
    ]
    for candidate in candidates:
        if candidate and (candidate / "media_soviet").is_dir():
            return candidate.resolve()
    return None


def _scan_text_dependencies(
    files: Iterable[Path], *, wip: Path, no_dlc: bool, game_root: Path | None
) -> list[str]:
    errors: list[str] = []
    media_root = game_root / "media_soviet" if game_root else None
    for path in files:
        if path.suffix.lower() not in {".ini", ".mtl"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for line_number, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", "--", "//", "-")):
                continue
            if no_dlc and DLC_PATH_RE.search(stripped):
                errors.append(f"{path}:{line_number}: DLC path reference: {stripped}")
            if ABSOLUTE_PATH_RE.search(stripped):
                errors.append(f"{path}:{line_number}: absolute path reference: {stripped}")
            for match in REFERENCE_RE.finditer(stripped):
                reference = match.group("path")
                reference_path = Path(reference.replace("\\", "/"))
                if reference_path.is_absolute():
                    errors.append(
                        f"{path}:{line_number}: absolute path reference: {reference}"
                    )
                    continue
                candidates = [path.parent / reference_path, wip / reference_path]
                if media_root:
                    candidates.append(media_root / reference_path)
                if not any(candidate.is_file() for candidate in candidates):
                    errors.append(
                        f"{path}:{line_number}: missing referenced file {reference}"
                    )
    return errors


def verify(
    *,
    wips: Iterable[Path],
    no_dlc: bool = False,
    game_root: Path | None = None,
    spike: str | None = None,
) -> dict[str, str]:
    results: dict[str, str] = {}
    detected_game_root = game_root.resolve() if game_root else _detect_game_root()
    for raw_wip in wips:
        wip = validate_wip_path(raw_wip)
        state = _managed_state(wip)
        if not state.get("paths"):
            raise HarnessError(f"no managed P0 fixture staged in {wip}")
        if spike and state.get("spike") != spike.upper():
            raise HarnessError(
                f"{wip} contains {state.get('spike', 'UNKNOWN')}, not {spike.upper()}"
            )
        config_lines = set((wip / "workshopconfig.ini").read_text(encoding="utf-8").splitlines())
        errors: list[str] = []
        for line in state.get("object_lines", []):
            if line not in config_lines:
                errors.append(f"missing workshop object line: {line}")
        managed_files: list[Path] = []
        for value in state.get("paths", []):
            relative = _safe_relative(str(value))
            root = wip / relative
            if not root.is_dir():
                errors.append(f"missing managed object directory: {relative}")
                continue
            kind = next(
                (
                    match.group(1).lower()
                    for line in state.get("object_lines", [])
                    if (match := OBJECT_RE.match(line))
                    and match.group(2) == relative.as_posix()
                ),
                None,
            )
            required = ["building.ini", "renderconfig.ini", "model.nmf", "material.mtl", "imagegui.png"] if kind == "building" else ["script.ini", "main.nmf", "material.mtl"]
            for name in required:
                if not (root / name).is_file():
                    errors.append(f"missing {relative.as_posix()}/{name}")
            managed_files.extend(path for path in root.rglob("*") if path.is_file())
        errors.extend(
            _scan_text_dependencies(
                managed_files, wip=wip, no_dlc=no_dlc, game_root=detected_game_root
            )
        )
        if errors:
            raise HarnessError("verification failed:\n- " + "\n- ".join(errors))
        results[str(wip)] = tree_hash(managed_files, wip)
    return results


def _git_head() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else "UNAVAILABLE"


def snapshot(
    *,
    manifest_path: Path,
    spike: str,
    variant: str,
    wips: Iterable[Path],
    output: Path,
) -> None:
    manifest = _load_json(manifest_path.resolve())
    selected = _variant(manifest, spike, variant)
    hashes = verify(wips=wips, no_dlc=False, spike=spike)
    game_root = _detect_game_root()
    media_root = game_root / "media_soviet" if game_root else None
    source_rows: list[str] = []
    for source in selected.get("vanilla_sources", []):
        path = Path(source["path"]).expanduser()
        if not path.is_absolute() and media_root:
            path = media_root / path
        checksum = sha256_file(path) if path.is_file() else "MISSING"
        source_rows.append(f"| `{path}` | `{checksum}` |")
    text = f"""# {spike.upper()} — {selected.get('title', variant)}

## Environment

| Field | Value |
|---|---|
| Steam build | `{manifest.get('game_build', 'UNSET')}` |
| Git commit | `{_git_head()}` |
| DLC state | `UNSET` |
| Variant | `{variant}` |

## Vanilla sources

| Path | SHA-256 |
|---|---|
{os.linesep.join(source_rows) if source_rows else '| `UNSET` | `UNSET` |'}

## Fixture hashes

{os.linesep.join(f'- `{path}`: `{digest}`' for path, digest in sorted(hashes.items()))}

## INI diff

`UNSET` — attach the exact diff from the vanilla source(s) above to the staged fixture.

## Reproduction

1. `UNSET`

## Observation

`NOT RUN`

## Evidence

- Screenshot: `UNSET`
- Recording path/checksum: `UNSET`
- Save path/checksum: `UNSET`

## Result

`NOT RUN` — replace with `PASS` or `FAIL` only after the observable criterion is checked in game.
"""
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    subparsers = parser.add_subparsers(dest="command", required=True)

    stage_parser = subparsers.add_parser("stage")
    stage_parser.add_argument("--spike", required=True)
    stage_parser.add_argument("--variant", default="primary")
    stage_parser.add_argument("--wip", type=Path, required=True)
    stage_parser.add_argument("--layout", choices=("nested", "flat", "split"), default="nested")
    stage_parser.add_argument("--vehicle-wip", type=Path)

    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("--spike", required=True, help="Recorded for CLI symmetry")
    verify_parser.add_argument("--wip", type=Path, action="append", required=True)
    verify_parser.add_argument("--no-dlc", action="store_true")
    verify_parser.add_argument("--game-root", type=Path)

    snapshot_parser = subparsers.add_parser("snapshot")
    snapshot_parser.add_argument("--spike", required=True)
    snapshot_parser.add_argument("--variant", default="primary")
    snapshot_parser.add_argument("--wip", type=Path, action="append", required=True)
    snapshot_parser.add_argument("--out", type=Path, required=True)
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        if args.command == "stage":
            targets = stage(
                manifest_path=args.manifest,
                spike=args.spike,
                variant=args.variant,
                layout=args.layout,
                wip=args.wip,
                vehicle_wip=args.vehicle_wip,
            )
            print("Staged P0 fixture:")
            for target in targets:
                print(f"- {target}")
        elif args.command == "verify":
            hashes = verify(
                wips=args.wip,
                no_dlc=args.no_dlc,
                game_root=args.game_root,
                spike=args.spike,
            )
            for path, digest in sorted(hashes.items()):
                print(f"verified {path}: {digest}")
        elif args.command == "snapshot":
            snapshot(
                manifest_path=args.manifest,
                spike=args.spike,
                variant=args.variant,
                wips=args.wip,
                output=args.out,
            )
            print(f"wrote {args.out}")
    except HarnessError as exc:
        print(f"P0 harness error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
