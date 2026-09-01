# Testing and QA

Run the relevant matrix on every private or published WIP build. P0 evidence is more important than broad playtime: each fragile behavior needs a reproducible yes or no.

## Pinned environment

The automated part of the P0 environment is pinned below. A test result without the remaining per-run fields is provisional.

| Field | Value |
|---|---|
| Game version / build | Steam build `23935965` |
| Operating system | Fedora Linux 44, kernel `7.1.10-200.fc44.x86_64` |
| DLC enabled | World Maps installed as a syntax reference; **disabled for final P0 runs** |
| Realistic mode / difficulty settings | `UNSET` |
| Test-map name and revision | `UNSET` |
| GPU / CPU / resolution for FPS checks | `UNSET` |
| Source vanilla assets and paths | Recorded with SHA-256 in `docs/evidence/p0/` and `experiments/p0/manifest.json` |

Whenever the pinned game build changes, rerun P0 loading plus the entire core-loop script before updating Workshop copy.

## Two test saves

### Technical save

A small deterministic republic with power, university workers, roads, broad rail curves, fuel access and the minimum required vanilla inputs. It exists to reproduce mechanics quickly. Using setup cheats is allowed, but the save note must list them.

### Campaign acceptance save

A representative late-game republic reached through normal play. It measures construction cost, staffing burden, time to first launch and whether the loop creates a worthwhile player decision. It is not used to debug sockets.

Back up both saves with the matching git commit or tag. If saves cannot be distributed in the repository, record their local path, checksum and setup recipe.

## Matrix

| Area | Check | When |
|---|---|---|
| Static package | `python tools/validate_workshop.py` | Every candidate build |
| Load | Mod alone: no crash, no missing models or textures | Every build |
| Version | Pinned game build recorded and unchanged | Every evidence run |
| Chain | Throughput vs `ECONOMY.md` at 100% staff | Each factory change |
| Causality | Removing each declared input stops the corresponding output | Each chain change |
| Pathing | Required vehicles reach every socket without deadlock | Every building change |
| Persistence | Three complete cycles with save/reload between cycles | P1 exit, every release |
| Terrain | Place on flat and moderate slope; document limits | Every building change |
| Performance | Reproducible FPS benchmark vs grey-box baseline | P2 exit, every release |
| Names | No banned strings in UI | Every release |
| Economy | Actual construction bill, cost per launch, time to first launch | P5 |
| Compatibility | Alone first; selected popular-mod mix | P6 |

## P0 harness and spike record

Build sources with Blender `5.2.0 LTS`, convert the resulting OBJ files in ModelViewer through Proton 11, then stage only into a Steam-created private WIP:

```bash
python experiments/p0/build_assets.py
python tools/p0_harness.py stage --spike S7 --wip /path/to/workshop_wip/ITEM --layout nested
python tools/p0_harness.py verify --spike S7 --wip /path/to/workshop_wip/ITEM --no-dlc
```

The harness preserves Steam metadata, deletes only paths from its prior managed-state file and refuses targets outside a direct `workshop_wip` child. `workshop/` never receives P0 fixtures.

For P0A and each S1–S7 capture:

1. Question and expected observable result.
2. Pinned environment and source vanilla object.
3. Minimal ini diff.
4. Exact reproduction steps.
5. Observed result, including what happens after save/reload.
6. Screenshot or short capture for visual behavior.
7. `PASS` or `FAIL` in `docs/evidence/p0/` and `docs/DECISIONS.md`.

Do not record `PARTIAL` as architecture approval. Split an ambiguous result into a new question.

## P1 core-loop script

1. Load the technical save with Kosmograd as the only mod.
2. Place or inspect the VAB and pad; connect power, workers, rail and any S5-proven fuel route.
3. Deliver the direct vanilla inputs listed in `ECONOMY.md`.
4. Remove one required input and verify production stops; restore it.
5. Confirm Zarya-K1 is produced at the VAB.
6. Load it onto the transporter-erector using the arrangement proven by S2.
7. Travel the tested curve and unload using the arrangement proven by S3.
8. If S5 passed, verify that missing fuel blocks the endpoint and record fuel consumed.
9. Complete and observe the exact lifecycle proven by S4.
10. Save, reload and verify there is no stranded or duplicated rocket.
11. Repeat the complete sequence twice more.
12. Verify any loyalty effect independently and describe it as static unless S6 proved event timing.

Any failed repetition blocks P1 exit.

## Pathing hunts

- Erector alone, with a locomotive, and in a train longer than the VAB.
- Tight curve failure radius versus the supported minimum radius.
- Fuel tanker and train present at the pad together, if fuel is enabled.
- Rocket behavior with an ordinary airport and external air connection on the same map.
- Save while the rocket is in the VAB, on the wagon, on the pad and after the endpoint.

## Performance benchmark

Record resolution, graphics preset, camera location, game speed and map state. Run at least three 60-second samples for the grey-box and candidate build. Compare median FPS and note 1% lows if available. A regression greater than 5% requires investigation; measurement noise is not an automatic failure.

## Closed playtest

Starts after P2 has representative art. Recruit at least three testers who did not build the mod. Provide the technical save and ask for:

- whether they can complete the loop without verbal help;
- bug, reproduction steps and save file;
- the point at which the loop becomes unclear or tedious;
- whether the endpoint feels worth the logistics.

Public Workshop visibility is a release decision, not the mechanism for finding the first three testers.
