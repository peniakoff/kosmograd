# Blender pipeline

Kosmograd meshes are made in **Blender 4.x**, exported as **Wavefront OBJ**, and converted with the game's **ModelViewer** to `.nmf`. This is the official wiki path. There is no supported FBX-into-game shortcut (the PDF mentioned FBX; the wiki says triangulate → merge by distance → OBJ → ModelViewer).

Per-asset sizes, origins, and prompts live in [ASSETS.md](ASSETS.md). This file is the shared mechanical recipe.

## Units and axes

| | Blender | Game tokens |
|---|---|---|
| Unit | metre (Scene → Metric, scale 1.0) | metre |
| Up | Z | **Y** |
| Ground | Z = 0 | Y = 0 |

Export OBJ with:

- Forward: **-Z**
- Up: **Y**
- Selection only
- Apply modifiers
- Triangulate faces (or triangulate in Edit Mode before export)
- Write normals
- Include UVs
- **Do not** write materials that the game will ignore — MTL from Blender is not the game `.mtl`. Game materials are authored in ModelViewer.

Confirm this axis pair in P0 with a 2 × 3 × 5 m box whose names are painted on the faces. If the box lies on its side in ModelViewer, change the export axes once and write the working pair here.

## Mandatory mesh hygiene (every export)

1. Origin set as in ASSETS.md.
2. `Ctrl-A` apply all transforms.
3. Edit Mode → all faces → triangulate.
4. Merge by distance (small threshold, do not weld the whole building into a blob).
5. No n-gons, no loose verts, no inverted normals on the exterior.
6. One object named `Main` (buildings) or the `KOSM_veh_…` root (vehicles). Extra objects only when `$COST_WORK_BUILDING_NODE` or `$DUMPER_DECK_PIVOT` needs a named node — those names must survive export. ModelViewer / NMF node naming: **COPY** a vanilla multi-node building in P0. If OBJ flattening destroys names, export as separate OBJs and combine in ModelViewer if the tool allows, or use the community NMF Blender addon if you have it — still produce the same node names.

## Textures

1. Shared atlas for P1 buildings: `blender/atlas/kosm_concrete_metal.png` (working file) → `diffuse.dds` per asset (can be the same DDS copied).
2. Paint weathering into the atlas: soot under vents, rust streaks, oil on the pad, warning stripes.
3. Game DDS: community practice is DXT1 for vehicles (1-bit alpha for glass). Buildings follow vanilla hall format — **COPY**.
4. UV: atlas-based, not a unique 8k bake. Landmark buildings may use 2048²; still one material.
5. Night: duplicate the albedo, paint windows/beacons light, rest black → `material_e.mtl` in ModelViewer as vanilla does.

Do not use Blender Principled BSDF as the delivery artefact. It is viewport only.

## Grey-box → final

```text
cube at exact footprint
    → sockets as Empty objects
    → export, ModelViewer, ini, in-game pathing
    → only then replace cube with final mesh, same origin, same sockets
```

Never move the origin between grey-box and final. If you must, you redo every `$CONNECTION_*` coordinate.

## Folder for source files

```text
blender/
├── atlas/
├── scripts/export_wrsr.py
└── assets/
    ├── buildings/kosm_<name>/
    │   ├── kosm_<name>.blend
    │   └── export/model.obj
    └── vehicles/kosm_<name>/
        ├── kosm_<name>.blend
        └── export/main.obj
```

`.blend` is canonical. `export/` is generated. Workshop `.nmf` is generated from OBJ and is **not** edited by hand.

## ModelViewer

1. Import OBJ.
2. Confirm scale vs a vanilla reference (a 10× error here ruins the district).
3. Save `model.nmf` (buildings) or `main.nmf` (vehicles) into the matching `workshop/…` folder.
4. Assign DDS, save `material.mtl`.
5. Do not create `bbox.bin` here if the game generates it on load.

## Quality gate

Open [ASSETS.md](ASSETS.md) checklist. If tris exceed the ceiling, stop and cut loops — do not raise the ceiling for one hero asset.
