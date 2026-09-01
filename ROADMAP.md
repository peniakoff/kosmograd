# Roadmap

Feasibility first, playable second, pretty third. Every phase has a binary exit criterion and a stop decision. Dependency order remains more important than calendar promises, but experiments are timeboxed so the project cannot spend months polishing an engine trick that does not work.

## Phase map

```text
P0A  Asset pipeline       one disposable grey-box building loads in game
P0B  Gameplay feasibility prove the complete rocket lifecycle on cubes
GO / PIVOT / STOP         record the decision and the evidence
P1   Core launch loop     VAB + rocket + erector + pad, resource-fed
P2   Core art             final art for the four core assets
P3   Extended logistics   stages, satellite and dedicated fuel chain
P4   Cosmodrome           optional district buildings and later vehicles
P5   Balance freeze       costs and throughput locked against test saves
P6   Workshop release     public presentation, localization and compatibility
```

The public product may stop after P2. P3 and P4 add depth; they are not prerequisites for a coherent first release.

---

## P0A — Asset pipeline

**Goal.** Prove the file formats and import path on a disposable object.

**Timebox.** One working session; two sessions maximum before asking an experienced WR:SR modder for help.

**Build**

1. Pin the exact game build in `docs/TESTING.md`.
2. Create a private Workshop WIP item in game. Keep Steam-owned identifiers only in the deploy copy.
3. Grey-box a 4 × 6 m shed in Blender.
4. Export OBJ → ModelViewer → `.nmf` + `.mtl`.
5. Start from a vanilla object from the pinned game build and change the minimum necessary fields.
6. Place it on the test map twice; confirm generated bounds, construction and road access.

**Exit criterion**

- The private WIP item loads without a crash, the shed is constructable after bounds generation, and a truck reaches its connection.
- The exact export axes, vanilla source object and tested game build are recorded.

Failure here pauses all gameplay and art work.

---

## P0B — Gameplay feasibility

**Goal.** Prove every fragile joint of the core loop with disposable meshes and copied vanilla definitions.

**Timebox.** Two to four hours per spike. If a spike fails, test only its named fallback. An unproven idea is not a fallback.

| ID | Question | Pass | Failed result |
|---|---|---|---|
| S1 | Can `$TYPE_PRODUCTION_LINE` + `$SUBTYPE_AIRPLANE` produce an airplane flagged `$CARGOVEHICLE_MUSTBE_LOADED`? | VAB can produce Zarya-K1 | Core architecture cannot use the airplane-cargo pattern |
| S2 | Can the produced airplane be loaded onto a rail wagon using `RESOURCE_TRANSPORT_OPEN` + `RESOURCE_ALLOW_ONLY vehicles`? | Erector remains a rail wagon | Test the named road-to-separate-terminal fallback |
| S3 | Can a cargo-airplane station receive that vehicle from rail and place it on an airplane stand? | Pad remains one building | Test a proven rail terminus plus a separate airplane parking building |
| S4 | Does a nose-up airplane with a short takeoff distance leave the pad without requiring an ordinary airport route, and what is its complete lifecycle afterward? | Visual launch is viable and repeatable | No accepted fallback yet; pivot the product promise |
| S5 | Can pad fuel storage refuel the airplane and can one launch consume a measurable amount? | Fuel is part of the core gate | Remove fuel as a launch gate until a proven mechanism exists |
| S6 | Do loyalty tokens work on the pad, and are they static or event-driven? | Document the observed behavior | Use a separate monument only as a static completion reward |
| S7 | Can one Workshop item reliably contain the required building and vehicle objects with the repository path layout? | Keep one item | Split the release into linked building and vehicle items |
| S8 | Can a production line causally require manufactured vehicles as inputs? | P3 may use physical stages and satellite | P3 factories remain deferred; do not fake causality with duplicate sinks |

S8 is deliberately not required for the four-asset P1. It decides whether the extended logistics chain is worth building.

**Evidence required for every spike**

- Date, pinned game build, source vanilla asset and exact ini diff.
- Pass/fail result in `docs/DECISIONS.md`.
- A minimal reproducible WIP folder and test-save note.
- Screenshot or short capture where visual behavior matters.

### P0 decision gate

After S1–S7 choose and record exactly one outcome:

- **GO:** the complete core lifecycle is repeatable; start P1.
- **PIVOT:** transport works but launch/reward does not; rewrite the product as an aerospace-industry or cosmodrome asset pack before making final art.
- **STOP:** the core cargo-airplane lifecycle cannot be made reliable.

Do not begin final meshes before this decision.

Implementation status: the deterministic P0 fixtures, harness, tests and blank evidence records live under `experiments/p0/`, `tools/p0_harness.py` and `docs/evidence/p0/`. This is preparation, not a completed spike; all game observations remain `NOT RUN` until ModelViewer conversion and the private-WIP runs are performed.

---

## P1 — Core launch loop

**Goal.** Deliver the smallest loop that preserves the unique part of Kosmograd.

| Folder | Role |
|---|---|
| `workshop/buildings/kosm_assembly_center` | Consumes vanilla resources and produces Zarya-K1 |
| `workshop/vehicles/kosm_zarya_k1` | Cargo-capable airplane used as the rocket |
| `workshop/vehicles/kosm_transporter_erector` | Rail wagon carrying the rocket |
| `workshop/buildings/kosm_launch_pad` | Receives, fuels and launches the rocket if proven in P0 |

The VAB uses direct vanilla resource inputs in P1. This is an explicit scope choice, not a fallback. Every input is still physically delivered; the rocket is manufactured as a vehicle at the VAB.

**Exit criterion**

- On the technical test save, resources reach the VAB, Zarya-K1 is produced, loaded onto the erector, transported over the verified rail geometry, unloaded and completes the exact lifecycle proven by S4.
- The same sequence succeeds three consecutive times after save/reload.
- Fuel is required only if S5 passed.
- The player-facing text describes the observed reward honestly: no per-launch loyalty or financial payoff unless it was demonstrated.
- No crash when loaded as the only mod.

P1 remains private or closed-test. Grey-boxes are evidence, not the public first impression.

---

## P2 — Core art and closed beta

**Goal.** Replace the four core grey-boxes with vanilla-adjacent art.

**Order**

1. Launch pad
2. Zarya-K1
3. Transporter-erector
4. Assembly center

**Exit criterion**

- All four assets meet the budgets in `docs/ASSETS.md`.
- Performance passes the reproducible benchmark in `docs/TESTING.md`.
- Icons, preview image, basic EN copy and an installation guide exist.
- At least three external testers complete the loop from the supplied test save.

An honest Sputnik-only public beta may ship here as `0.x`.

---

## P3 — Extended logistics

Only start if S8 passed and testers say the core loop needs more production depth.

| Asset | Purpose |
|---|---|
| Rocket factory + K-1 stage set | Physical stage manufacturing and delivery |
| Satellite factory + Vestnik-1 | Physical payload manufacturing and delivery |
| Fuel refinery | Dedicated oil + chemicals fuel chain, only if S5 proved it matters |

If S8 fails, do not create decorative cargo vehicles that are unrelated to VAB output. Keep the VAB resource-fed and spend the effort on art, usability or P4 district buildings.

**Exit criterion**

- Stage and payload deliveries are causally required for Zarya production, not merely parallel role-play.
- Every added asset earns its maintenance and performance cost through a distinct player decision.

---

## P4 — Optional full cosmodrome

Candidate assets remain specified in `docs/ASSETS.md`: memorial plaza, rail terminus, mission control, tracking station, propellant storage, research bureau, museum, training center, quarters, recovery depot, heavy pad, stacking hall and gate.

Each asset requires a short gameplay statement before modelling: what decision it creates, what engine-supported effect it has, and why existing vanilla content cannot fill the role.

No custom resources, UI, orbital simulation or vanilla-file edits enter this phase.

---

## P5 — Balance freeze

**Exit criterion**

- Construction and operating costs match the observed game calculations, not estimated mesh dimensions alone.
- Cost per launch and time to first launch are recorded for both the technical save and a representative late-game republic.
- Documentation calls Kosmograd a prestige sink, static district benefit or profitable program according to measured behavior. It does not promise payback without a revenue mechanism.
- Throughput tables match the shipped ini files at 100% staffing.

---

## P6 — Public Workshop release

**Exit criterion**

- `python tools/validate_workshop.py` passes against the release contents.
- The matrix in `docs/TESTING.md` is green on the pinned game version.
- Workshop page contains tested version, screenshots, honest feature list, known limitations and changelog.
- EN strings are complete. RU is included if reviewed by a speaker; otherwise it is deferred rather than machine-translated silently.
- Release is `1.0.0` only after the core loop and art are stable. Extended logistics and the full district are not required for 1.0.

## Pre-agreed cut order

1. Full cosmodrome.
2. Extended stage, satellite and fuel factories.
3. Secondary factory art.
4. Fuel as a gameplay gate if S5 fails.
5. Vertical-launch claim if S4 fails — this triggers a documented product pivot, not a fictional consume fallback.

The minimum promise that may survive is: **vanilla inputs → manufactured rocket vehicle → physical rail transport → an engine-supported and honestly described endpoint**.

## Out of scope for the v1 line

- Orbital station assembly
- Lunar program
- Booster reuse or refurbishment
- Foreign contract board or AI space race
- Random launch failures
- Lasers, space elevators or interplanetary drives
- Edits to vanilla files

Park later ideas in `docs/PARKING.md`.
