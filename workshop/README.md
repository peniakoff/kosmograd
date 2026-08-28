# Kosmograd: Sputnik — Workshop staging

This directory is the future canonical Workshop staging tree. It is **not installable yet**; read [NOT_INSTALLABLE_YET.md](NOT_INSTALLABLE_YET.md).

Steam owns `$ITEM_ID` and `$OWNER_ID`. Keep those values in the live deploy copy. Do not commit personal Workshop identifiers to the prototype catalog.

Meshes (`.nmf`, `.dds`) are not in git yet. Grey-boxes are produced in `blender/` and converted with ModelViewer. Until then, each asset folder holds annotated ini templates and a local README.

See [docs/WORKSHOP.md](../docs/WORKSHOP.md) and [docs/PIPELINE.md](../docs/PIPELINE.md).

Static checks:

```bash
python tools/validate_workshop.py --prototype  # current draft structure
python tools/validate_workshop.py              # release completeness
```
