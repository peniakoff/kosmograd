# Agent brief

Instruction layer for an AI (code, ini, or Blender MCP) working in this repository.

## Product

Kosmograd: Sputnik — a WR:SR mod in feasibility work. First ship is a four-asset rocket production and rail-transport core. Read `README.md`, `ROADMAP.md`, then `docs/DECISIONS.md` and the file that matches the task.

## Hard rules

1. Do not add custom resources.
2. Do not use REJECTED tokens from `docs/ENGINE_TOKENS.md`.
3. Do not use banned names from `docs/NAMING.md` as IDs.
4. One `$TYPE` per building.
5. Grey-box footprints in `docs/ASSETS.md` are frozen.
6. Start every ini from a vanilla file of the same type when the human can provide it; otherwise leave `COPY FROM VANILLA` comments, do not invent a parallel schema.
7. Do not implement P3/P4 assets unless the decision gate and task authorize that phase.
8. Never describe a fallback, launch lifecycle or reward as working without a recorded P0 result.
8. Do not edit vanilla game files.

## Task routing

| Task | Open |
|---|---|
| What are we building? | `docs/VISION.md` `ROADMAP.md` |
| How does a launch exist? | `docs/ARCHITECTURE.md` |
| This building/vehicle | `docs/ASSETS.md` |
| Blender / MCP | `docs/BLENDER.md` `docs/BLENDER_MCP.md` |
| Tokens | `docs/ENGINE_TOKENS.md` |
| Economy numbers | `docs/ECONOMY.md` |
| Put it in Steam | `docs/WORKSHOP.md` `docs/PIPELINE.md` |

## Output style for ini

- `#` comments allowed.
- No spaces except inside quotes.
- Spellings `eletric` `eletronics` `PROFESORS` `aluminium` `VEHICLETYPE_RAIL_VAGON` as the engine has them.
