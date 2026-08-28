# Kosmograd: Sputnik

A space-program expansion for **Workers & Resources: Soviet Republic**.

The republic already knows how to mine, smelt, and ship. Kosmograd asks it to put something into the sky. The first chapter — **Sputnik** — is a complete, playable launch loop: fabricate the vehicle, haul it on rails, fuel the pad, and light the candle.

This repository is the design source of truth and the Workshop staging catalog. Models are built in Blender (including Blender MCP). Configuration is the game's real `$TOKEN` language, not a fictional JSON schema.

| | |
|---|---|
| **Game** | Workers & Resources: Soviet Republic |
| **Mod** | Kosmograd: Sputnik |
| **First ship** | One historical-era orbital launch loop |
| **Later** | Full cosmodrome district (see [ROADMAP.md](ROADMAP.md)) |
| **License** | MIT |

## What to read, in order

1. **[docs/VISION.md](docs/VISION.md)** — what the mod is, and what it is not.
2. **[docs/DECISIONS.md](docs/DECISIONS.md)** — how the two source plans were merged, and why.
3. **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** — the engine workarounds that make a launch exist.
4. **[docs/ASSETS.md](docs/ASSETS.md)** — every building and vehicle: `building.ini` / `script.ini` tokens **and** Blender modelling specs. This is the file you open when you model or configure anything.
5. **[ROADMAP.md](ROADMAP.md)** — phases, exit criteria, cut lines.
6. **[docs/BLENDER_MCP.md](docs/BLENDER_MCP.md)** — how an AI agent drives Blender against `ASSETS.md`.

## The Sputnik loop (what we are building first)

```text
vanilla industry
        │
        ├─ steel / aluminium / mcomponents / ecomponents
        │         │
        │         ├─► Rocket Factory  ──► K-1 stages (cargo vehicles, by truck)
        │         └─► Satellite Factory ──► Vestnik-1 (cargo vehicle, by truck)
        │                       │
        │                       ▼
        │              Assembly Center (VAB)
        │                       │  produces Zarya-K1 (airplane that cannot taxi)
        │                       ▼
        │         Transporter-Erector (rail wagon)
        │                       │  gentle-curve railway
        │                       ▼
        │                 Launch Pad
        │                       │  unload → rocket stands on the pad
        └─ oil + chemicals ─► Fuel Refinery ─► vanilla fuel ─┘
                                │
                                ▼
                         vertical takeoff
                         republic-wide loyalty
```

Nothing teleports. If the player cannot route it, it does not launch.

## Repository map

```text
kosmograd/
├── README.md                 ← you are here
├── ROADMAP.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── docs/                     design, engine, pipeline, testing
├── workshop/                 WR:SR Workshop item contents (copy into workshop_wip)
│   ├── workshopconfig.ini
│   ├── description.txt
│   ├── buildings/
│   └── vehicles/
├── blender/                  source 3D (grey-box → final), export scripts
└── tools/                    copy-to-WIP notes and helpers
```

The live Steam folder is **not** this repo. Create a WIP item in-game, then copy `workshop/` into `SovietRepublic/media_soviet/workshop_wip/<item_id>/`. Details: [docs/WORKSHOP.md](docs/WORKSHOP.md).

## Canonical rules (do not drift)

1. **Vanilla-first.** 1960s–80s panel construction, weathered concrete, muted blue-grey metal, sparing red. A Kosmograd building at 200 m must read as the same republic, new district.
2. **No custom resources.** The documented toolchain cannot add new goods. Rockets and satellites **are vehicles**. Fuel is vanilla fuel. Prestige is monument loyalty, not a new resource named Glory.
3. **One `$TYPE` per building.** Never combine a production line and a cargo station in one ini. Split buildings instead.
4. **Original names on Workshop.** Display copy may evoke history. Folder IDs and `$NAME_STR` use the [naming registry](docs/NAMING.md). No Soyuz, Vostok, R-7, Baikonur, Sputnik-1 as product IDs.
5. **Grey-box first.** A correctly sized, correctly pathed cube that produces and consumes is more valuable than a pretty mesh that will not load.
6. **Copy vanilla, then edit.** Every new `building.ini` / `script.ini` starts from a vanilla building or vehicle of the same type. Tokens in this repo that are marked **UNVERIFIED** are hypotheses until a P0 spike confirms them.

## Toolchain

| Tool | Role |
|---|---|
| Blender 4.x | Modelling, UVs, grey-boxes. Driven by hand or [Blender MCP](docs/BLENDER_MCP.md) |
| paint.net / GIMP | Texture atlases, weathering, `imagegui.png` |
| WR:SR ModelViewer | `.obj` → `.nmf`, `.mtl` authoring |
| In-game Building / Vehicle Editor | Placement points, first-load bbox |
| This git repo | Design, ini sources, blend sources, changelog |

All of it is free. There is no custom engine plugin.

## Current status

Documentation and catalog only. No mesh has been imported into the game yet. Phase **P0** is the pipeline spike: one grey-box building in a WIP item. See [ROADMAP.md](ROADMAP.md).

## References

Official wiki and LovelyPL's token guides are listed in [docs/REFERENCES.md](docs/REFERENCES.md). When a token in this repo disagrees with those guides, the guides win until we prove otherwise in-game.
