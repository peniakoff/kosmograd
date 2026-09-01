from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools import p0_harness


class P0HarnessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.fixture_root = self.root / "fixtures"
        self.fixture_root.mkdir()
        self._building("shed")
        self._vehicle("rocket")
        overlay = self.root / "overlays" / "rocket"
        overlay.mkdir(parents=True)
        (overlay / "script.ini").write_text(
            '$TYPE VEHICLETYPE_AIRPLANE\n$NAME_STR "overlaid"\n', encoding="utf-8"
        )
        self.manifest = self.root / "manifest.json"
        self.manifest.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "objects": {
                        "shed": {
                            "kind": "building",
                            "source": "fixtures/shed",
                            "required": [
                                "building.ini",
                                "renderconfig.ini",
                                "model.nmf",
                                "material.mtl",
                                "diffuse.dds",
                                "imagegui.png",
                            ],
                        },
                        "rocket": {
                            "kind": "vehicle",
                            "source": "fixtures/rocket",
                            "required": [
                                "script.ini",
                                "main.nmf",
                                "material.mtl",
                                "diffuse.dds",
                            ],
                        },
                    },
                    "spikes": {
                        "S7": {
                            "variants": {
                                "primary": {"objects": ["shed", "rocket"]},
                                "overlay": {
                                    "objects": ["shed", "rocket"],
                                    "overlays": {"rocket": "overlays/rocket"},
                                },
                            }
                        }
                    },
                }
            ),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _building(self, name: str) -> None:
        target = self.fixture_root / name
        target.mkdir()
        files = {
            "building.ini": "$TYPE_BUILDING\n",
            "renderconfig.ini": "$MODEL model.nmf\n$MATERIAL material.mtl\n",
            "model.nmf": "mesh",
            "material.mtl": "$TEXTURE diffuse.dds\n",
            "diffuse.dds": "texture",
            "imagegui.png": "icon",
        }
        for filename, content in files.items():
            (target / filename).write_text(content, encoding="utf-8")

    def _vehicle(self, name: str) -> None:
        target = self.fixture_root / name
        target.mkdir()
        files = {
            "script.ini": "$TYPE VEHICLETYPE_AIRPLANE\n",
            "main.nmf": "mesh",
            "material.mtl": "$TEXTURE diffuse.dds\n",
            "diffuse.dds": "texture",
        }
        for filename, content in files.items():
            (target / filename).write_text(content, encoding="utf-8")

    def _wip(self, item: str = "100") -> Path:
        target = self.root / "workshop_wip" / item
        target.mkdir(parents=True)
        (target / "workshopconfig.ini").write_text(
            "$ITEM_ID 100\n$OWNER_ID 200\n$ITEM_TYPE 0\n$VISIBILITY 2\n",
            encoding="utf-8",
        )
        return target

    def _stage(self, wip: Path, *, layout: str = "nested", **kwargs: object) -> None:
        p0_harness.stage(
            manifest_path=self.manifest,
            spike="S7",
            variant=str(kwargs.pop("variant", "primary")),
            layout=layout,
            wip=wip,
            vehicle_wip=kwargs.pop("vehicle_wip", None),
        )

    def test_nested_stage_preserves_steam_metadata_and_unrelated_files(self) -> None:
        wip = self._wip()
        (wip / "notes.txt").write_text("keep", encoding="utf-8")
        self._stage(wip)

        config = (wip / "workshopconfig.ini").read_text(encoding="utf-8")
        for line in ("$ITEM_ID 100", "$OWNER_ID 200", "$ITEM_TYPE 0", "$VISIBILITY 2"):
            self.assertIn(line, config)
        self.assertTrue((wip / "buildings" / "shed" / "building.ini").is_file())
        self.assertTrue((wip / "vehicles" / "rocket" / "script.ini").is_file())
        self.assertEqual((wip / "notes.txt").read_text(encoding="utf-8"), "keep")

    def test_staging_is_idempotent_and_replaces_only_managed_trees(self) -> None:
        wip = self._wip()
        self._stage(wip)
        (wip / "vehicles" / "rocket" / "stale.txt").write_text("old", encoding="utf-8")
        (wip / "unmanaged.txt").write_text("keep", encoding="utf-8")
        self._stage(wip, variant="overlay")

        config = (wip / "workshopconfig.ini").read_text(encoding="utf-8")
        self.assertEqual(config.count("$OBJECT_BUILDING"), 1)
        self.assertEqual(config.count("$OBJECT_VEHICLE"), 1)
        self.assertEqual(config.count(p0_harness.MANAGED_COMMENT), 1)
        self.assertFalse((wip / "vehicles" / "rocket" / "stale.txt").exists())
        self.assertTrue((wip / "unmanaged.txt").is_file())
        self.assertIn("overlaid", (wip / "vehicles" / "rocket" / "script.ini").read_text())

    def test_flat_and_split_layouts(self) -> None:
        flat = self._wip("101")
        self._stage(flat, layout="flat")
        self.assertTrue((flat / "shed" / "building.ini").is_file())
        self.assertTrue((flat / "rocket" / "script.ini").is_file())

        buildings = self._wip("102")
        vehicles = self._wip("103")
        self._stage(buildings, layout="split", vehicle_wip=vehicles)
        self.assertTrue((buildings / "shed" / "building.ini").is_file())
        self.assertFalse((buildings / "rocket").exists())
        self.assertTrue((vehicles / "rocket" / "script.ini").is_file())
        self.assertFalse((vehicles / "shed").exists())

        with self.assertRaisesRegex(p0_harness.HarnessError, "two different WIP"):
            self._stage(buildings, layout="split", vehicle_wip=buildings)

    def test_refuses_targets_outside_workshop_wip_and_symlinks(self) -> None:
        outside = self.root / "outside"
        outside.mkdir()
        (outside / "workshopconfig.ini").write_text("$ITEM_ID 1\n", encoding="utf-8")
        with self.assertRaises(p0_harness.HarnessError):
            self._stage(outside)

        real = self._wip("104")
        link = self.root / "workshop_wip" / "linked"
        link.symlink_to(real, target_is_directory=True)
        with self.assertRaises(p0_harness.HarnessError):
            self._stage(link)

    def test_failed_source_check_does_not_touch_existing_stage(self) -> None:
        wip = self._wip()
        self._stage(wip)
        config_before = (wip / "workshopconfig.ini").read_bytes()
        (self.fixture_root / "rocket" / "main.nmf").unlink()
        with self.assertRaises(p0_harness.HarnessError):
            self._stage(wip)
        self.assertEqual((wip / "workshopconfig.ini").read_bytes(), config_before)
        self.assertTrue((wip / "vehicles" / "rocket" / "main.nmf").is_file())

    def test_verify_hash_is_deterministic_and_detects_dlc(self) -> None:
        wip = self._wip()
        self._stage(wip)
        first = p0_harness.verify(wips=[wip], no_dlc=True)
        second = p0_harness.verify(wips=[wip], no_dlc=True)
        self.assertEqual(first, second)
        with self.assertRaisesRegex(p0_harness.HarnessError, "contains S7, not S1"):
            p0_harness.verify(wips=[wip], spike="S1")

        script = wip / "vehicles" / "rocket" / "script.ini"
        script.write_text("$SOUND_PARAMS cwc/vehicles/secret.ini\n", encoding="utf-8")
        with self.assertRaisesRegex(p0_harness.HarnessError, "DLC path reference"):
            p0_harness.verify(wips=[wip], no_dlc=True)

    def test_verify_rejects_absolute_references(self) -> None:
        wip = self._wip()
        self._stage(wip)
        script = wip / "vehicles" / "rocket" / "script.ini"
        script.write_text("$SOUND_PARAMS /tmp/private.ini\n", encoding="utf-8")
        with self.assertRaisesRegex(p0_harness.HarnessError, "absolute path reference"):
            p0_harness.verify(wips=[wip])

    def test_verify_rejects_missing_base_game_dependency(self) -> None:
        wip = self._wip()
        self._stage(wip)
        script = wip / "vehicles" / "rocket" / "script.ini"
        script.write_text("$SOUND_PARAMS vehicles/does_not_exist.ini\n", encoding="utf-8")
        with self.assertRaisesRegex(p0_harness.HarnessError, "missing referenced file"):
            p0_harness.verify(wips=[wip])


if __name__ == "__main__":
    unittest.main()
