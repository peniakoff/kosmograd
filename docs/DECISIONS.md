# Design decisions

Two source documents described Kosmograd. They agree on the feeling and disagree on the machine. This file is the merge. New work follows this file, not the originals.

| Source | What it is |
|---|---|
| **MD** — *Kosmograd: Sputnik – WR:SR Mod Development Master Plan* | MVP: five buildings, airplane-as-rocket, cargo parts, rail erector, historical Sputnik 1 framing, `script.ini` tokens |
| **PDF** — *Kosmograd Mod Design & Development Plan v1.0* | Full expansion: 18 buildings, 3 rockets, 4 spacecraft, Glory economy, original names, grey-box art pipeline, illustrative JSON |

## Decision 1 — Prove and ship the four-asset core first

**Choice.** P1 contains the Assembly Center, Zarya-K1, Transporter-Erector and Launch Pad. It is resource-fed. The stage, satellite and dedicated fuel factories move to P3 and require S8 before implementation. The full cosmodrome is P4.

**Why.** The unique risk is the cargo-airplane lifecycle, not factory modelling. Four assets prove that lifecycle with less sunk art. Parallel stage deliveries that cannot gate rocket output would violate the real-logistics pillar rather than deepen it.

## Decision 2 — Vehicles are the goods. There are no custom resources.

**Choice.** Rockets, stages, and satellites are vehicles. Fuel is vanilla fuel. "Glory" is `$MONUMENT_GOVERNMENT_LOYALTY_*` (and attraction tokens), not a new cargo type.

**Why.** The official wiki is explicit: you can mod maps, skins, vehicles, and buildings. New resource types are not in the supported toolchain. The PDF's avionics / RP-K blend / Glory goods would be the elegant economy — and they are not loadable. The MD already stumbled into the working pattern: **if it has to move, it is a vehicle**.

The PDF's "hook-light" instinct is kept: consume only vanilla intermediates (`steel`, `aluminium`, `mcomponents`, `ecomponents`, `chemicals`, `oil`, `eletronics`). Do not add glass, fibrous plants, or other third-party goods as hard requirements.

## Decision 3 — One `$TYPE` per building; split rather than stack

**Choice.** The Steam building guide: *you can use only one type for a building*. The VAB is a production line. The pad is a cargo/airplane station. Loyalty, if it cannot hang on the pad, is a second monument building.

**Why.** The MD asked the Assembly Center to be `$TYPE_PRODUCTION_LINE` **and** a train station with `$LOADING_VEHICLES`, and the pad to be a cargo airport **and** a monument. Several of those tokens (`$LOADING_VEHICLES`, `$UNLOADING_VEHICLES`, `$STATION_TRAIN`, `$RAIL_NODE`) do not appear in LovelyPL's guides. Connections (`$CONNECTION_RAIL`, `$VEHICLE_STATION`, `$AIRPLANE_STATION_50M`) *can* sit on many types. Functions cannot be stacked by wishing for a second `$TYPE`.

P0 spikes S1 and S2 exist because the remaining uncertainty is empirical, not rhetorical.

## Decision 4 — Airplane rocket is the launch candidate. No fallback is accepted yet.

**Choice.**

1. **Primary (MD).** Zarya-K1 is `$TYPE VEHICLETYPE_AIRPLANE` with `$CARGOVEHICLE_MUSTBE_LOADED`, near-zero `$TAKEOFF_DISTANCE`, mesh authored nose-up. The pad parks it on `$AIRPLANE_STATION_50M`. Takeoff is the show.
2. **Failure handling.** If the airplane taxis to a civilian airport, refuses to stand, will not climb, requires an unsuitable route or cannot reach a repeatable lifecycle endpoint, P0 records **PIVOT**. A consuming pad is only a fallback candidate until a cube test demonstrates legal vehicle consumption and removal.

**Why.** Players will remember a candle, but documentation cannot manufacture one. The endpoint must be observed three times and survive save/reload before art or Workshop copy promises a launch.

## Decision 5 — Original names, Sputnik era

**Choice.** Workshop IDs and `$NAME_STR` use the PDF registry (Kosmograd, Zarya-K1, Vestnik-1, Bogatyr, Chaika, …). The *chapter* is called Sputnik. Concept art and docs may say "R-7-inspired" or "1957 orbital". Product IDs never say R-7, Sputnik-1, Baikonur, Soyuz, Vostok.

**Why.** The MD's historical names are clearer for a design conversation and riskier on Workshop. The PDF's IP rule is cheap now and expensive later. The mod title **Kosmograd: Sputnik** keeps the era without claiming the hardware.

## Decision 6 — Real file names, real tokens

**Choice.**

| Kind | File | Mesh |
|---|---|---|
| Building | `building.ini` + `renderconfig.ini` | `model.nmf` |
| Vehicle | `script.ini` | `main.nmf` |
| Workshop | `workshopconfig.ini` + `description.txt` + preview image | — |

The MD called everything `script.ini`. The PDF used JSON. The wiki and the Getting Started threads win.

Tokens are copied from LovelyPL's building and vehicle guides (see [REFERENCES.md](REFERENCES.md)). Invented tokens are listed in [ENGINE_TOKENS.md](ENGINE_TOKENS.md) as **UNVERIFIED** or **REJECTED**.

Corrected from the MD:

| MD wrote | Engine actually uses |
|---|---|
| `$TYPE WAGON` | `$TYPE VEHICLETYPE_RAIL_VAGON` |
| `$CARGO_TYPE VEHICLES` | `$RESOURCE_TRANSPORT_TYPE RESOURCE_TRANSPORT_VEHICLES` |
| `$MAX_CARGO_WEIGHT 300` | `$RESOURCE_CAPACITY 300` |
| `$RAIL_NODE` | `$CONNECTION_RAIL` |
| `$RESOURCE_ALUMINUM` | `aluminium` (and `ecomponents`, `mcomponents`, `eletronics`) |
| `$WHEEL_...` | Wheel objects in the mesh; the game infers turning from naming/position |
| `$PARTICLE_MOVEMENT factory_big_gray` on a vehicle | Vehicle emitters (`vehicle_medium`, …) or copy a vanilla jet; `factory_*` is a **building** particle |

## Decision 7 — Grey-box, budgets, shared atlas (from the PDF)

**Choice.** Every implemented asset begins as a footprint-correct grey-box. Grey-boxes prove mechanics privately; representative final art is required before public visibility. Polygon and texture ceilings from the PDF concept sheets remain ceilings. Shared concrete/metal atlas. Weathering in the texture, not in the mesh.

**Why.** The MD skipped art process. The PDF's Chapter 8 is the part of that document that should survive any scope cut.

## Decision 8 — Reward language follows observed behavior

**Choice.** The PDF Glory table remains a fiction reference, not an implementation target. In engine:

- Monument tokens are treated as a static area effect unless S6 proves otherwise.
- Optional attraction or museum effects belong to P4 and must be described as persistent building functions.
- Export revenue is a separate later mechanic and cannot be counted as launch payback unless the game causally links it to the launch output.

There is no scripted mission-duration payout, per-launch loyalty pulse or custom Glory counter. Until another mechanism is demonstrated, Kosmograd is a prestige-sink candidate.

## Decision 9 — Git repo vs Workshop WIP

**Choice.** This git repository holds `workshop/` as the canonical contents. Steam assigns `workshop_wip/<id>/`. Copy, do not develop only inside Steam's numbered folder.

**Why.** The PDF said "Git from day one". The MD described only the staging tree. Both are true if git is the parent.

## P0 decision and spike results

Fill these in when S1–S8 from [ROADMAP.md](../ROADMAP.md) are run. Until S1–S7 pass, the architecture in [ARCHITECTURE.md](ARCHITECTURE.md) is a target, not a working machine.

| Spike | Date | Result | Action taken |
|---|---|---|---|
| S1 Production line → must-be-loaded airplane | | | |
| S2 VAB → vehicle-carrying rail wagon | | | |
| S3 Rail wagon → cargo-airplane stand | | | |
| S4 Complete airplane lifecycle | | | |
| S5 Pad refuelling and measured consumption | | | |
| S6 Loyalty context and timing | | | |
| S7 Mixed Workshop item and paths | | | |
| S8 Manufactured vehicles as causal inputs | | | |

**P0 decision:** `NOT MADE` — replace with `GO`, `PIVOT` or `STOP`, date and rationale after S1–S7.
