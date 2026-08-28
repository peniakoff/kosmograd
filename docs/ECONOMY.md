# Economy

All numbers are **starting values**. They freeze only at P4. Tune in-game; do not invent a second table in a spreadsheet that the ini files do not match.

Production amounts in WR:SR are **per worker per workday**. A building with more `$WORKERS_NEEDED` produces more at 100% staffing. The rates below are written as **building totals at 100% staff** and must be converted when writing `$PRODUCTION` / `$CONSUMPTION` lines:

```text
token_amount = building_total_per_day / WORKERS_NEEDED
```

Verify this conversion against a vanilla factory of known throughput during P0. If vanilla uses a different hidden multiplier, copy vanilla's style and scale.

## Capital cost (target band)

The full P1 complex (five buildings, no monuments) should land as a **late-game state project**: tens of millions of rubles, driven by mesh bounding boxes via `$COST_RESOURCE_AUTO`, not a handmade ruble token.

Grey-box footprints in [ASSETS.md](ASSETS.md) are therefore frozen. Changing a hall from 34 × 46 m to "a bit bigger" is an economy change.

## Vanilla inputs only

| Good | Token | Role |
|---|---|---|
| Steel | `steel` | Airframe, railside industry |
| Aluminium | `aluminium` | Airframe, satellite skin |
| Mechanical components | `mcomponents` | Engines, jigs |
| Electronic components | `ecomponents` | Guidance, satellite |
| Electronics | `eletronics` | Same family; pick whichever vanilla electronics plant outputs — **COPY** |
| Oil | `oil` | Fuel chain |
| Chemicals | `chemicals` | Makes space fuel more expensive than civilian fuel |
| Fuel | `fuel` (COPY) | Pad tanks / airplane |
| Electricity | `eletric` | `$CONSUMPTION_PER_SECOND` |
| Workers / professors | — | `$WORKERS_NEEDED` / `$PROFESORS_NEEDED` |

No avionics good. No RP-K good. No Glory good.

## P1 throughput (starting)

### Satellite factory — 1.0 Vestnik-1 per 8 workdays at 100% staff

60 workers, 12 professors.

| | t / vehicle |
|---|---|
| `aluminium` | 0.8 |
| `ecomponents` (or `eletronics`) | 1.2 |
| `mcomponents` | 0.4 |

Slow on purpose. The first satellite is an event.

### Rocket factory — 1.0 stage set per 6 workdays at 100% staff

85 workers, 10 professors.

| | t / vehicle |
|---|---|
| `steel` | 12 |
| `aluminium` | 4 |
| `mcomponents` | 3.2 |

One "stage set" cargo vehicle stands in for the cluster of boosters + core. We do not ship four strap-on vehicles in P1.

### Assembly center — 1.0 Zarya-K1 per 10 workdays at 100% staff

85 workers, 20 professors.

Preferred inputs: 1× `kosm_stage_k1` + 1× `kosm_vestnik_1` as imported vehicles.

Resource-only fallback (if vehicles cannot be inputs):

| | t / rocket |
|---|---|
| `steel` | 12 |
| `aluminium` | 5 |
| `mcomponents` | 3.5 |
| `ecomponents` | 1.4 |

Plus electricity high enough to hurt if the player has a weak grid.

### Fuel refinery — 1.0 t fuel per day at 100% staff (30 workers)

| Input | t / t fuel |
|---|---|
| `oil` | 0.7 |
| `chemicals` | 0.4 |

A light launch should burn on the order of **8–16 t** of fuel (PDF light/medium band). That is several days of this plant, or a pre-fill from tanks. Do not make it 200 t; the truck/pipe route should stay busy, not absurd.

If vanilla airplanes consume fuel from `$STORAGE_FUEL` by tank volume rather than a mission ticket, set Zarya-K1 fuel capacity so that **one fill ≈ one launch**. COPY a vanilla jet's fuel tokens, then scale.

### Pad

No `$PRODUCTION` in the primary design. It is a station. Loyalty is the payout.

If S3 fallback (consume the airplane): treat the pad as a factory that consumes the parked vehicle and emits nothing, with particles. There may be no legal `$CONSUMPTION` for a vehicle type — in that case the "consume" is the airplane taking off and despawning, which is the primary design anyway.

## Loyalty (P1 payout)

Starting monument tokens on the pad **or** memorial:

```text
$MONUMENT_GOVERNMENT_LOYALTY_RADIUS 400
$MONUMENT_GOVERNMENT_LOYALTY_STRENGTH 2.8
```

Radius huge, strength high. Tune so a launch district is felt in nearby cities, not on the other side of a 16 km map unless testing says the engine already maps 400 m as "large". Vanilla monuments are the calibration. **COPY** a Lenin statue or victory monument and go larger, do not guess a 5000 m radius that might be clamped.

## PDF Glory table (design target only)

Kept so P3 content has a north star. **Not implemented as a resource.**

| Tier | Vehicle | Payload | Glory (fiction) |
|---|---|---|---|
| T1a | Zarya-K1 | Vestnik-1 | 10 |
| T1b | Zarya-K1 | Sfera | 12 |
| T1c | Zarya-K1 | Vektor | 14 |
| T2a | Zarya-K2 | Vektor | 30 |
| T2b | Zarya-K2 | Chaika | 45 |
| T3a | Bogatyr | long-duration crew | 90 |

P3 "unlocks" are `$AVAILABLE` years on the heavier vehicles plus extra buildings, not a Glory counter hitting 30.

## Export safety valve (P3)

A sellable Vestnik variant without `$CARGOVEHICLE_MUSTBE_LOADED` (or with `$CARGOVEHICLE_CANBE_LOADED` and a purchase price) can go through customs. Floor price should be worse than flying. Do not add this in P1 or the pad will starve.

## What not to tune

- Do not lower professor counts to "make it accessible". Accessibility is "grey-box loop works", not "space program runs on elementary school".
- Do not add dollars-only vehicles. `$COST_RUB 1` on Soviet hardware.
- Do not modify vanilla factory rates to feed Kosmograd.
