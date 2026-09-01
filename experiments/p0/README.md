# P0 experiment fixtures

These files are private feasibility fixtures, not Workshop release content and
not P1 art. `manifest.json` composes the object sets used by P0A and S1–S7.

## Build

```bash
blender --factory-startup --background --python experiments/p0/build_fixtures.py
```

This writes canonical test `.blend` files and Y-up OBJ exports under
`generated/`. Open every OBJ in ModelViewer, verify scale/orientation, then save
the resulting NMF as `model.nmf` for buildings or `main.nmf` for vehicles in the
matching `assets/` directory. Save `material.mtl` there and point it at the
generated flat `diffuse.dds`.

The harness refuses to stage an incomplete fixture:

```bash
python tools/p0_harness.py stage --spike P0A \
  --wip /absolute/path/to/media_soviet/workshop_wip/<ITEM_ID>
```

Use `--variant fallback` only after the primary S2 or S3 experiment has a
recorded FAIL. Use `--layout flat` only after nested S7 fails. Split layout needs
the two Steam-created private items:

```bash
python tools/p0_harness.py stage --spike S7 --layout split \
  --wip /.../workshop_wip/<BUILDING_ITEM_ID> \
  --vehicle-wip /.../workshop_wip/<VEHICLE_ITEM_ID>
```

Never copy Steam IDs, saves, generated bbox/fire files, or full recordings into
this directory.
