# Naming registry

Workshop IDs, folder names, and `$NAME_STR` use this table. Historical names appear only in the "Inspired by" column and in designer notes — never as product IDs.

Prefix every folder and internal id with `kosm_`. Collision with other mods becomes a non-issue and grep stays easy.

## Banned series names

Do not use as `$NAME_STR`, folder, or texture text: Kosmos, Meteor, Prognoz, Yantar, Soyuz, Vostok, R-7, Sputnik-1, Sputnik 1, Baikonur, Gagarin (as a vehicle name). *Gagarin Memorial Plaza* as a building display name is allowed — it is a place of memory, not a spacecraft designation. Still avoid putting the word on a rocket.

A trademark / Workshop search runs before public 1.0 (checklist in [WORKSHOP.md](WORKSHOP.md)).

## Registry

| Name | Applied to | Folder / id | Inspired by | Meaning |
|---|---|---|---|---|
| Kosmograd | Mod and district | `kosmograd` | Closed towns at Soviet pads | Space City |
| Sputnik | Chapter / subtitle only | — | 1957 orbital era | The first loop, not the hardware id |
| Zarya-K1 | Light orbital rocket (airplane) | `kosm_zarya_k1` | R-7 / 8K71 class | Sunrise; K = Kosmograd |
| Zarya-K2 | Medium rocket (P3) | `kosm_zarya_k2` | R-7A / Vostok-era lift | |
| Bogatyr | Heavy rocket (P3) | `kosm_bogatyr` | N1-inspired silhouette, not a copy | Epic knight |
| Vestnik-1 | First satellite (cargo vehicle) | `kosm_vestnik_1` | Sputnik 1 | Herald |
| Vestnik | Comms satellite family (P3) | `kosm_vestnik` | | |
| Sfera | Weather satellite (P3) | `kosm_sfera` | | Sphere |
| Vektor | Science satellite (P3) | `kosm_vektor` | | Vector |
| Chaika | Crew capsule (P3) | `kosm_chaika` | Callsign tradition | Seagull |
| K-1 stage | Booster / core as cargo | `kosm_stage_k1` | R-7 strap-on / core as freight | |
| Transporter-erector | Rail wagon | `kosm_transporter_erector` | 8U216-class rail TE | |
| RP-K | Fiction-only nickname for **vanilla fuel** used at the pad | — | T-1 / kerosene-LOX story | Not a resource token |

## Buildings (display name → folder)

| Display `$NAME_STR` | Folder | Phase |
|---|---|---|
| "Kosmograd Rocket Factory" | `kosm_rocket_factory` | P1 |
| "Kosmograd Satellite Factory" | `kosm_satellite_factory` | P1 |
| "Kosmograd Assembly Center" | `kosm_assembly_center` | P1 |
| "Kosmograd Fuel Refinery" | `kosm_fuel_refinery` | P1 |
| "Kosmograd Launch Pad" | `kosm_launch_pad` | P1 |
| "Kosmograd Memorial Plaza" | `kosm_memorial_plaza` | P3 / P1 hotfix |
| "Kosmograd Rail Terminus" | `kosm_rail_terminus` | P3 / S2 fallback |
| "Kosmograd Mission Control" | `kosm_mission_control` | P3 |
| "Kosmograd Tracking Station" | `kosm_tracking_station` | P3 |
| "Kosmograd Propellant Storage" | `kosm_propellant_storage` | P3 |
| "Kosmograd Research Bureau" | `kosm_research_bureau` | P3 |
| "Kosmograd Museum" | `kosm_museum` | P3 |
| "Kosmograd Training Center" | `kosm_training_center` | P3 |
| "Kosmograd Cosmonaut Quarters" | `kosm_quarters` | P3 |
| "Kosmograd Recovery Depot" | `kosm_recovery_depot` | P3 |
| "Kosmograd Heavy Pad" | `kosm_launch_heavy` | P3 |
| "Kosmograd Stacking Hall" | `kosm_stacking_hall` | P3 |
| "Kosmograd Gate" | `kosm_gate` | P3 |

## Blender object names

`KOSM_<category>_<name>_v<NN>`

Examples: `KOSM_bldg_launch_pad_v01`, `KOSM_veh_zarya_k1_v01`.

Construction-phase nodes inside a building mesh: `MainHall`, `Gantry`, `Chimney`, `PadDeck` — ASCII, no spaces. These strings are referenced by `$COST_WORK_BUILDING_NODE`.

## Country and years

- `$COUNTRY 39011` (Soviet Union) on all vehicles.
- Sputnik-loop vehicles: `$AVAILABLE 1957 3000`.
- Heavier P3 vehicles may start later (`1961`, `1967`, …) so a 1957 save still has a first candle.
