# Testing and QA

Run this matrix on every published WIP build, not only at 1.0.

## Test save

One dedicated republic. Full P1 complex. Never "just play" on it. Back it up with the git tag of the build.

## Matrix

| Area | Check | When |
|---|---|---|
| Load | Mod alone: no crash, no missing textures | Every build |
| Compatibility | Alone first. Popular-mod mix is P5, not P1 | P5 |
| Chain | Throughput vs ECONOMY.md at 100% staff | Each factory change |
| Pathing | Trucks, trains, (airplanes) reach every listed socket; no deadlock | Every new building |
| Terrain | Place on flat; note slope failures | Every new building |
| Performance | FPS vs grey-box baseline within ~5% | P2 exit, every release |
| Names | No banned strings in UI | Every release |
| Economy | Not free, not a printer | P4 |

## Sputnik loop script (P1 exit)

1. New map, cheat only to skip to a year ≥ 1957 if needed.
2. Place all five buildings with power, road, rail (VAB→pad), pipes.
3. Staff with professors available.
4. Deliver listed vanilla goods.
5. Confirm stage + Vestnik spawn and load onto trucks.
6. Confirm Zarya-K1 exists at the VAB.
7. Couple vanilla loco + erector, load, travel a **wide** curve, unload at pad.
8. Fuel the pad.
9. Confirm takeoff **or** documented consume-fallback.
10. Confirm loyalty effect (or memorial placed).

Write pass/fail into `docs/DECISIONS.md` if a spike is involved; otherwise a line in CHANGELOG.md is enough.

## Pathing hunts

- Two trucks at the rocket factory court (`$STATION_NOT_BLOCK`).
- Train longer than the VAB; `$LONG_TRAINS` / max wagons.
- Fuel tanker + train at the pad together.
- Airplane (if S3 passed) not taxiing to a civilian airport on the same map — **if it does, S3 has failed**.

## Community playtest (from M2 / P1 onwards)

WIP public. Feedback template: bug, reproduction, save file. Crashes same day. Balance batched to P4.
