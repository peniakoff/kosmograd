# Roadmap

Playable first, pretty later. Every phase ends with something that runs in the game. Exit criteria are binary.

This plan does **not** use calendar estimates. It is ordered by dependency: pipeline, then the Sputnik loop, then the rest of the cosmodrome, then balance and Workshop polish.

## Phases

```text
P0  Pipeline          one grey-box building loads in a WIP item
P1  Sputnik loop      five buildings + four vehicles, grey-box, end-to-end launch
P2  Art pass          replace grey-boxes that shipped in P1; shared atlas
P3  Cosmodrome        remaining v1.0 buildings/vehicles from the deferred list
P4  Balance freeze    economy numbers locked against a test republic
P5  Workshop release  trailer, screenshots, EN+RU strings, changelog
```

P3 is optional relative to a Sputnik-only public release. Cut lines below say what to drop if P1 or P2 slips.

---

### P0 — Pipeline proven

**Goal.** Learn the real file formats on a disposable asset so Kosmograd assets are not the first import.

**Build**

1. Create a Workshop WIP item in-game. Record `$ITEM_ID` in `workshop/workshopconfig.ini`.
2. Grey-box a small shed in Blender (4 × 6 m). Follow [docs/BLENDER.md](docs/BLENDER.md).
3. Export OBJ → ModelViewer → `.nmf` + `.mtl`.
4. Copy a vanilla decorative or small factory `building.ini` + `renderconfig.ini`. Change only name, workers, footprint-related nodes.
5. Place it on a test map. Confirm pathing and construction.

**Exit criterion**

- The WIP item loads without crash, the shed is constructable on the second map load (bbox generated), and a truck can reach its road connection.

**Also in P0 (engine spikes, not art)**

These three questions decide whether the Sputnik architecture stands. Run them on cubes. Document results in [docs/DECISIONS.md](docs/DECISIONS.md) under "P0 spike results".

| ID | Question | Pass | Fail → fallback |
|---|---|---|---|
| S1 | Can `$TYPE_PRODUCTION_LINE` + `$SUBTYPE_AIRPLANE` produce a vehicle flagged `$CARGOVEHICLE_MUSTBE_LOADED`? | VAB stays one building | Split: factory outputs to a vehicle storage; a second building loads rail |
| S2 | Can a `$TYPE_CARGO_STATION` `$SUBTYPE_AIRPLANE` unload a rail wagon of vehicles **and** park an airplane on `$AIRPLANE_STATION_50M`? | Launch pad stays one building | Split rail terminus + pad |
| S3 | If the airplane mesh is authored nose-up (+Y) and `$TAKEOFF_DISTANCE` is ~1 m, does it climb? | Visual launch is real | Pad consumes the vehicle (factory event); particles are presentation only |

Do not start P1 art until S1–S3 are answered.

---

### P1 — Sputnik vertical slice

**Goal.** A fresh map, no cheats, can run the loop in [README.md](README.md).

**Content (grey-box, gameplay-complete)**

| Folder | Role |
|---|---|
| `workshop/buildings/kosm_rocket_factory` | Stages as cargo vehicles |
| `workshop/buildings/kosm_satellite_factory` | Vestnik-1 as cargo vehicle |
| `workshop/buildings/kosm_assembly_center` | Assembles Zarya-K1 |
| `workshop/buildings/kosm_fuel_refinery` | Oil + chemicals → vanilla fuel |
| `workshop/buildings/kosm_launch_pad` | Unload, fuel, park, launch |
| `workshop/vehicles/kosm_stage_k1` | Cargo, must be loaded |
| `workshop/vehicles/kosm_vestnik_1` | Cargo, must be loaded |
| `workshop/vehicles/kosm_zarya_k1` | Airplane rocket |
| `workshop/vehicles/kosm_transporter_erector` | Rail wagon, vehicles cargo |

Every asset is specified in [docs/ASSETS.md](docs/ASSETS.md). Do not invent extra buildings in this phase.

**Exit criterion**

- Test save: parts leave both factories by truck, Zarya-K1 is assembled, the wagon carries it on a gentle-curve railway, the pad receives it, fuel arrives by pipe or tanker, the vehicle leaves the pad (climb or consume-fallback), loyalty tokens fire.
- No crash on load alone.
- Construction costs are in the late-game band (millions of rubles for the full set), not free.

Publish the WIP publicly at the end of P1. Grey-boxes visible is a feature.

---

### P2 — Art for the loop

**Goal.** Replace P1 grey-boxes with vanilla-adjacent meshes under the budgets in `ASSETS.md`.

**Order** (silhouette first, interiors never)

1. Launch pad
2. Zarya-K1
3. Assembly center
4. Transporter-erector
5. Rocket factory
6. Satellite factory
7. Fuel refinery
8. Vestnik-1 and stage cargo meshes

Shared concrete/metal atlas. Weathering painted into the texture.

**Exit criterion**

- All nine P1 assets have final (or atlas-final) meshes.
- FPS on the test map stays within ~5% of the grey-box baseline.
- Poly and texture budgets in `ASSETS.md` are not exceeded.

---

### P3 — Full cosmodrome (v1.0 expansion)

Only after P1 is playable. These are the buildings from the long design plan that the Sputnik loop does not need.

| Priority | Asset | Why it waits |
|---|---|---|
| A | `kosm_memorial_plaza` | Loyalty companion if pad monument tokens fail |
| A | `kosm_rail_terminus` | Fallback if S2 fails; still useful as a dedicated loader |
| B | `kosm_mission_control` | Staffing / professor sink; no new resource |
| B | `kosm_tracking_station` | Decorative coverage + attraction score |
| B | `kosm_propellant_storage` | Fuel buffer so the pad is not the only tank |
| C | `kosm_research_bureau` | University-worker sink; "unlock" is the 1957–later `$AVAILABLE` window on heavier vehicles |
| C | `kosm_museum` | Culture + loyalty; Glory multiplier analogue |
| C | `kosm_training_center` | Crewed program — citizens as passengers to the pad |
| C | `kosm_quarters` | Housing subtype for crew |
| C | `kosm_recovery_depot` | Capsule return — needs S3 and a second airplane/cargo loop |
| D | `kosm_launch_heavy` | Zarya-K2 / Bogatyr pad |
| D | `kosm_stacking_hall` | Vertical integration building |
| D | `kosm_avionics_line` | **Rejected as a custom good.** If built, it is a themed electronics factory that still outputs vanilla `ecomponents` |
| D | `kosm_gate` | Decorative perimeter |

Vehicles added in P3: Zarya-K2, Bogatyr, Vestnik/Sfera/Vektor variants, Chaika capsule. Same cargo-vehicle + airplane pattern as P1.

**Exit criterion**

- Each shipped P3 asset has a grey-box that pathfinds and a row in `ASSETS.md`.
- Still no custom resources.

---

### P4 — Balance freeze

**Goal.** Numbers in `ASSETS.md` and [docs/ECONOMY.md](docs/ECONOMY.md) stop moving except for bugs.

**Exit criterion**

- A dedicated test republic with the full P1 (and any shipped P3) complex is not a money printer and not a charity.
- Target band: full Sputnik complex costs a late-game republic a serious construction bill; a sustained launch cadence pays it back over a few in-game years.
- Tables in `ECONOMY.md` match in-game throughput at 100% staffing.

---

### P5 — Workshop release

**Exit criterion**

- [docs/TESTING.md](docs/TESTING.md) matrix is green for the release candidate.
- Workshop page: five screenshots, description from `workshop/description.txt`, EN+RU name strings, changelog, tested game version pinned.
- Semver: `1.0.0` only if P1+P2 are done. A Sputnik-only release with grey-box or partial art is `0.x`.

---

## Cut lines (pre-agreed, no renegotiation)

If a phase slips, cut in this order:

1. All of P3.
2. P2 art for factories; keep pad + rocket + wagon pretty.
3. Visual takeoff (S3 fail). Keep logistics; pad consumes the rocket.
4. Satellite factory as a separate building: fold Vestnik-1 production into the rocket factory (worse design, still a loop).

The loop that must survive every cut: **vanilla inputs → a rocket vehicle → the pad → a loyalty payoff**.

## Deferred forever until a later major version

Do not start these in this repository's v1 line:

- Orbital station assembled from launched modules
- Lunar program
- Booster reuse / refurbishment loop
- Foreign contract board / AI space race
- Lasers, space elevators, interplanetary drives
- Edits to any vanilla file

Park ideas in `docs/PARKING.md` if needed. Do not put them in `ASSETS.md` as if they were scheduled.
