# Blender MCP — agent instructions

This file is the contract for an AI agent driving Blender through MCP. The agent does not invent buildings. It executes [ASSETS.md](ASSETS.md).

## Before the first tool call

1. Read `docs/ASSETS.md` for the named asset only.
2. Read `docs/BLENDER.md` for units, axes, hygiene.
3. Read `docs/NAMING.md` so no banned string appears as object or texture text.
4. Confirm Blender MCP is connected (scene list should return objects). If it is not, stop and say so. Do not emit an OBJ from memory.

## What the agent is allowed to do

- Create grey-boxes to the millimetre.
- Place Empty sockets with the names in the asset sheet.
- Assign flat viewport materials (hex from ASSETS.md).
- Triangulate, merge by distance, apply transforms.
- Export OBJ to `blender/assets/<kind>/<folder>/export/` using the axis conversion in BLENDER.md.
- Save the `.blend` next to that folder.
- Replace a grey-box with a final mesh **only** if tris stay under budget and origin/sockets do not move.
- Build the shared atlas layout as separate image work in GIMP/paint.net is out of Blender MCP unless an image is already in the scene.

## What the agent must not do

- Add buildings that are not in the current roadmap phase.
- Use R-7, Sputnik-1, Baikonur, Soyuz, Vostok as object names.
- Export FBX as the game delivery (OBJ only).
- Ship live Subdivision Surface, unevaluated Geometry Nodes, or unapplied Boolean operands.
- Model interiors, furniture, or a static rocket on the pad stand.
- Change footprint, height class, or origin to "look better".
- Write `building.ini` tokens that [ENGINE_TOKENS.md](ENGINE_TOKENS.md) marks REJECTED.
- Claim an `.nmf` was created — ModelViewer is a human/game step unless a dedicated NMF exporter is installed and documented.

## Session recipe (copy this)

```text
Asset: <folder name from ASSETS.md>
Phase: grey-box | final
Read: docs/ASSETS.md section <N>
Units: metres, Blender Z-up
Origin rule: <quote the sheet>
Poly ceiling: <n>
Export: blender/assets/.../export/<model|main>.obj  (Y-up for WR:SR)
Then: list object names, bounding box in metres, tri count, socket world positions
```

After export, the agent reports:

- Bounding box size (x, y, z) in metres
- Origin world position
- Triangle count
- Socket empties and their game-space coordinates (convert back: Blender `(x,z,y)` → game `(x,y,z)` if using the documented mapping)
- File paths written

## Preferred modelling style for finals

Vanilla-adjacent, not portfolio-grade:

- Block out with cubes/cylinders first, then inset window strips as texture, not loops of glass.
- Panel lines = texture.
- Dishes, tanks, masts = lathed cylinders with few segments (8–12).
- Gantry = boxes. No truss of 200 beams.
- Merge into `Main` (and listed extra nodes) before export.

## Prompt blocks

Every catalog asset has a **Blender MCP prompt** at the end of its ASSETS.md section. Only the four P1-core prompts are authorized after the P0 `GO` decision. Use the relevant prompt as the first user message, then fix scale/origin if the bounding-box report disagrees with the sheet by more than 0.1 m.

## Failure handling

| Problem | Action |
|---|---|
| MCP cannot export OBJ | Save `.blend`, write a `bpy` export snippet to `blender/scripts/`, ask the human to run it |
| Tri count over budget | Decimate / dissolve, do not raise the cap |
| Origin drifted | Reset origin, do not patch ini coordinates "for now" |
| Axis looks wrong in a screenshot from ModelViewer | Stop modelling more assets. Fix BLENDER.md export settings once |
