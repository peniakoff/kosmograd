#!/usr/bin/env python3
"""Static completeness checks for the Kosmograd Workshop staging tree.

Prototype mode checks references and draft structure without pretending the
catalog is release-ready. Release mode additionally requires binary assets,
icons, preview art and removal of all known placeholder markers.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSHOP = ROOT / "workshop"
CONFIG = WORKSHOP / "workshopconfig.ini"
BLOCKER = WORKSHOP / "NOT_INSTALLABLE_YET.md"

OBJECT_RE = re.compile(r"^\$OBJECT_(BUILDING|VEHICLE)\s+(\S+)\s*$")
PLACEHOLDER_RE = re.compile(
    r"\bCOPY\b[^\n]*\bvanilla\b|\bUNVERIFIED\b|<paste>|<ITEM_ID>|\bTODO\b|\bFIXME\b",
    re.IGNORECASE,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prototype",
        action="store_true",
        help="allow intentionally missing release assets and placeholder comments",
    )
    return parser.parse_args()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"not UTF-8: {path.relative_to(ROOT)}") from exc


def object_entries(errors: list[str]) -> list[tuple[str, Path]]:
    if not CONFIG.is_file():
        errors.append("missing workshop/workshopconfig.ini")
        return []

    entries: list[tuple[str, Path]] = []
    for line_number, line in enumerate(read_text(CONFIG).splitlines(), start=1):
        match = OBJECT_RE.match(line.strip())
        if not match:
            continue
        kind, relative = match.groups()
        path = WORKSHOP / relative
        if not path.is_dir():
            errors.append(
                f"workshopconfig.ini:{line_number}: missing object directory {relative}"
            )
        entries.append((kind.lower(), path))
    if not entries:
        errors.append("workshopconfig.ini lists no $OBJECT_BUILDING or $OBJECT_VEHICLE")
    return entries


def require(path: Path, errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"missing {path.relative_to(ROOT)}")


def validate_object(kind: str, path: Path, prototype: bool, errors: list[str]) -> None:
    if not path.is_dir():
        return

    ini = path / ("building.ini" if kind == "building" else "script.ini")
    require(ini, errors)

    if kind == "building":
        require(path / "renderconfig.ini", errors)
        if not prototype:
            require(path / "model.nmf", errors)
            require(path / "material.mtl", errors)
            require(path / "imagegui.png", errors)
    elif not prototype:
        require(path / "main.nmf", errors)
        require(path / "material.mtl", errors)

    for text_file in path.glob("*.ini"):
        try:
            content = read_text(text_file)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not prototype and PLACEHOLDER_RE.search(content):
            errors.append(f"placeholder marker in {text_file.relative_to(ROOT)}")


def main() -> int:
    args = parse_args()
    errors: list[str] = []
    entries = object_entries(errors)

    for kind, path in entries:
        validate_object(kind, path, args.prototype, errors)

    if not args.prototype:
        if BLOCKER.exists():
            errors.append("workshop/NOT_INSTALLABLE_YET.md still blocks release")
        require(WORKSHOP / "previewimage.png", errors)
        require(WORKSHOP / "description.txt", errors)
        config_text = read_text(CONFIG) if CONFIG.is_file() else ""
        if PLACEHOLDER_RE.search(config_text):
            errors.append("placeholder metadata remains in workshop/workshopconfig.ini")

    mode = "prototype" if args.prototype else "release"
    if errors:
        print(f"Workshop {mode} validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Workshop {mode} validation passed for {len(entries)} objects.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
