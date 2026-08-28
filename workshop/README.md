# Kosmograd: Sputnik — Workshop staging

This directory is what gets copied into `media_soviet/workshop_wip/<ITEM_ID>/`.

Steam owns `$ITEM_ID` and `$OWNER_ID`. After you create the WIP item, paste those values into `workshopconfig.ini` and keep the `$OBJECT_*` lines.

Meshes (`.nmf`, `.dds`) are not in git yet. Grey-boxes are produced in `blender/` and converted with ModelViewer. Until then, each asset folder holds annotated ini templates and a local README.

See [docs/WORKSHOP.md](../docs/WORKSHOP.md) and [docs/PIPELINE.md](../docs/PIPELINE.md).
