# Kosmograd: Sputnik

A space-program expansion for **Workers & Resources: Soviet Republic**.

The republic already knows how to mine, smelt, and ship. Kosmograd asks it to put something into the sky. The first chapter — **Sputnik** — aims to deliver a playable launch loop: fabricate the vehicle, haul it on rails, fuel the pad, and light the candle. The required engine behavior is still in feasibility testing; unverified behavior is not a shipped feature.

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
7. **[docs/PROVENANCE.md](docs/PROVENANCE.md)** — what may be copied, what must be attributed, and what the repository license does not relicense.

## The Sputnik loop (target architecture)

```text
vanilla industry
        │
        ├─ steel / aluminium / mcomponents / ecomponents
        │                       │
        │                       ▼
        │              Assembly Center (VAB)
        │                       │  produces Zarya-K1 (cargo-airplane candidate)
        │                       ▼
        │         Transporter-Erector (rail wagon)
        │                       │  gentle-curve railway
        │                       ▼
        │                 Launch Pad
        │                       │  unload → rocket stands on the pad
        └─ vanilla fuel, if S5 passes ───────────────────────┘
                                │
                                ▼
                         S4-verified endpoint
```

P1 proves this four-asset core first. Physical stage, satellite and dedicated fuel factories move to P3 and are built only if the engine can make their deliveries causally necessary.

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
2. **No custom resources.** The documented toolchain cannot add new goods. Rockets and satellites are vehicles. Fuel is vanilla fuel. Static monument loyalty is not described as a per-launch reward.
3. **One `$TYPE` per building.** Never combine a production line and a cargo station in one ini. Split buildings instead.
4. **Original names on Workshop.** Display copy may evoke history. Folder IDs and `$NAME_STR` use the [naming registry](docs/NAMING.md). No Soyuz, Vostok, R-7, Baikonur, Sputnik-1 as product IDs.
5. **Grey-box first.** A correctly sized, correctly pathed cube that produces and consumes is more valuable than a pretty mesh that will not load.
6. **Copy pinned vanilla, then edit.** Every new `building.ini` / `script.ini` starts from a vanilla object of the same type from the game build recorded in `docs/TESTING.md`. A token existing in a guide does not prove that it works on the chosen building type.
7. **Fallbacks must run.** An untested alternative is a fallback candidate, not part of the architecture.

## Toolchain

| Tool | Role |
|---|---|
| Blender 5.2.0 LTS (P0 pin) | Modelling, UVs, grey-boxes. Driven by hand or [Blender MCP](docs/BLENDER_MCP.md) |
| paint.net / GIMP | Texture atlases, weathering, `imagegui.png` |
| WR:SR ModelViewer | `.obj` → `.nmf`, `.mtl` authoring |
| In-game Building / Vehicle Editor | Placement points, first-load bbox |
| This git repo | Design, ini sources, blend sources, changelog |

All of it is free. There is no custom engine plugin.

## Current status

Documentation and non-installable prototype catalog only. No mesh has been imported into the game yet. Do not copy `workshop/` into a live game expecting it to load. P0 first proves the asset pipeline and then the complete gameplay lifecycle. See [ROADMAP.md](ROADMAP.md) and [`workshop/NOT_INSTALLABLE_YET.md`](workshop/NOT_INSTALLABLE_YET.md).

## References

Official wiki and LovelyPL's token guides are listed in [docs/REFERENCES.md](docs/REFERENCES.md). When a token in this repo disagrees with those guides, the guides win until we prove otherwise in-game.
