# Pipeline (idea → in-game)

End-to-end path for one asset. Same path for a shed and for the launch pad.

```text
ASSETS.md row
    → Blender grey-box (hand or MCP)
    → OBJ export (BLENDER.md)
    → ModelViewer .nmf + .mtl + dds
    → workshop/ folder + building.ini or script.ini copied from vanilla
    → workshopconfig.ini $OBJECT_* line
    → validate the minimal candidate
    → copy only candidate objects into media_soviet/workshop_wip/<id>/
    → boot game twice (bbox / fire)
    → place on test map, path vehicles
    → only then final mesh, same origin
    → git commit, changelog line
```

## P0 first asset

Do not start with the pad. Start with a disposable shed. The shed may live only in the WIP folder and never in git. The satellite factory is P3 content and should not become the pipeline test by accident.

## Vanilla copy rule

Before writing tokens, copy the entire `building.ini` / `script.ini` of a vanilla object of the **same `$TYPE`** from the game build pinned in `TESTING.md`. Record the source path in the spike note. Then:

1. Preserve a clean copy or diff for evidence, then change `$NAME_STR`.
2. Change worker counts and consumption numbers toward ASSETS.md.
3. Replace connection coordinates with the sheet, keeping token *kinds*.
4. Delete tokens you do not understand; do not invent replacements.

## Workshop config

Steam writes `$ITEM_ID`, `$OWNER_ID`, `$ITEM_TYPE`, `$VISIBILITY`, `$TAGS` when you create a WIP item. We add:

```ini
$OBJECT_BUILDING buildings/kosm_rocket_factory
$OBJECT_BUILDING buildings/kosm_satellite_factory
$OBJECT_BUILDING buildings/kosm_assembly_center
$OBJECT_BUILDING buildings/kosm_fuel_refinery
$OBJECT_BUILDING buildings/kosm_launch_pad
$OBJECT_VEHICLE vehicles/kosm_zarya_k1
$OBJECT_VEHICLE vehicles/kosm_stage_k1
$OBJECT_VEHICLE vehicles/kosm_vestnik_1
$OBJECT_VEHICLE vehicles/kosm_transporter_erector
```

The mixed object list and slash paths are hypotheses until S7 passes. If the game ignores slashes, flatten and record the exact working layout.

`$ITEM_TYPE`: create the WIP as a **building** pack (primary) that also lists vehicles, **or** follow whatever the in-game wizard offers for mixed packs. Do not hand-write an ID.

## Files the game generates

Never commit: `*.bbox`, `*.fire`, `bbox.bin`, `preview.dds`, `preview_side.dds`.

First load after a new building may show it as unbuildable. Second load is the real test.

## Git

- Branch per asset or per phase, not per cube tweak if you are solo — but commit every in-game-verified step.
- `workshop/` is source. `workshop_wip/<id>/` is a deploy target.
- Changelog is part of the commit, not a release-day essay.
- Run `python tools/validate_workshop.py --prototype` during P0 and without the flag for a release candidate.
