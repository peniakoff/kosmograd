# Legacy P1 concept meshes

These Blender files were recovered from commit `a7c8cd5` on
`feature/some-old-stuff`. They are retained only as sources from which shapes
or components may be salvaged after the P0 feasibility decision.

They are **not canonical asset sources**, are not part of `workshop/`, and do
not count as completion of P0, P1, or P2. The current dimensions, names,
origins, budgets, and export requirements in `docs/ASSETS.md` remain
authoritative. P0 should continue to use disposable cubes.

## Audit

| File | What may be reusable | Known gaps against the current asset bible |
|---|---|---|
| `kosm_assembly_center.blend` | High-bay silhouette, doors, crane beams, transformer and chimney components | Roughly 80 × 90 m scene footprint instead of the current 34 × 46 m asset; 30 separate meshes; 6 n-gons; old rail and socket layout |
| `kosm_launch_pad.blend` | Flame trench, gantry, mast, bunker and rail-detail concepts | Roughly 53 × 73 m scene envelope instead of the current 34 × 34 m pad; 37 separate meshes; 78 n-gons; old four-mast and connection layout |
| `kosm_zarya_k1.blend` | Four-booster silhouette and nozzle-cluster components | Old R-7-specific naming; origin is near mid-stack rather than the nozzle plane; 58 separate meshes; 100 n-gons; four rotated objects; must become an original Zarya-K1 interpretation |

The source scenes contain simple Blender materials but no linked bitmap
textures. Recorded mesh totals are 696 triangles for the assembly center,
3,352 for the launch pad, and 3,544 for the rocket before export-time cleanup.

## Reuse gate

After a `GO` decision, copy only the useful geometry into the matching
canonical path under `blender/assets/`. Then:

1. Rebuild to the current footprint and clearance envelope.
2. Rename and consolidate objects according to `docs/ASSETS.md`.
3. Put the origin on the required ground or nozzle plane.
4. Apply transforms, triangulate, remove n-gons, and verify normals and UVs.
5. Record confirmed authorship and tool assistance in `docs/PROVENANCE.md`.
6. Export and test through the normal OBJ → ModelViewer → Workshop pipeline.

Do not export or ship these files directly.
