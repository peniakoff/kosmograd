# Economy

All numbers are **starting values**. They freeze only in the balance phase. Tune in game; do not invent a second table that the ini files do not match.

Production amounts in WR:SR are **per worker per workday**. A building with more `$WORKERS_NEEDED` produces more at 100% staffing. The rates below are written as **building totals at 100% staff** and must be converted when writing `$PRODUCTION` / `$CONSUMPTION` lines:

```text
token_amount = building_total_per_day / WORKERS_NEEDED
```

Verify this conversion against a vanilla factory of known throughput during P0. If vanilla uses a different hidden multiplier, copy vanilla's style and scale.

## Capital cost (target band)

The four-asset P1 core should feel like a **late-game state project**. Do not promise a ruble total before the pinned game build calculates one. `$COST_RESOURCE_AUTO` and model geometry influence construction resources; the technical test must record the actual bill shown by the game.

Grey-box footprints in [ASSETS.md](ASSETS.md) are stable inputs to testing. Changing a hall from 34 × 46 m to "a bit bigger" requires a new construction-cost measurement.

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

## P1 core throughput (starting)

### Assembly center — 1.0 Zarya-K1 per 10 workdays at 100% staff

85 workers, 20 professors. P1 deliberately uses direct vanilla resource inputs:

| | t / rocket |
|---|---|
| `steel` | 12 |
| `aluminium` | 5 |
| `mcomponents` | 3.5 |
| `ecomponents` | 1.4 |

This is the only production economy required for P1. Convert these totals to ini amounts only after validating the game's throughput multiplier against a pinned vanilla production line.

## P3 extended-logistics candidates

The following rates remain design candidates. They become shipped economy only if S8 proves that the delivered vehicles can causally gate assembly.

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

One "stage set" cargo vehicle stands in for the cluster of boosters + core. We do not ship four separate strap-on vehicles.

### Fuel refinery — 1.0 t fuel per day at 100% staff (30 workers)

| Input | t / t fuel |
|---|---|
| `oil` | 0.7 |
| `chemicals` | 0.4 |

A light launch design target is **8–16 t** of fuel. This number has no gameplay authority until S5 proves refuelling and records the actual amount consumed.

If vanilla airplanes consume fuel from `$STORAGE_FUEL` by tank volume rather than a mission ticket, set Zarya-K1 fuel capacity so that **one fill ≈ one launch**. COPY a vanilla jet's fuel tokens, then scale.

### P1 pad

No `$PRODUCTION` in the primary design. It is a station. Its function is transport and, if S5 passes, refuelling.

There is currently no accepted consume-vehicle fallback. A factory that consumes a vehicle is not part of the architecture until demonstrated in game. If S4 fails, use the P0 decision gate rather than inventing an economic sink in documentation.

## Loyalty candidate

Starting monument tokens for a dedicated memorial, or for the pad only if S6 confirms that this type accepts them:

```text
$MONUMENT_GOVERNMENT_LOYALTY_RADIUS 400
$MONUMENT_GOVERNMENT_LOYALTY_STRENGTH 2.8
```

Treat this as a static area effect. Do not call it a launch pulse, per-launch payout or proof that launch cadence repays the complex. Calibrate against a pinned vanilla monument and record the measured affected area.

## Economic role decision

Before balance freeze, select exactly one label supported by measurements:

- **Prestige sink:** launches consume resources for spectacle and player goals.
- **Static district benefit:** completing the complex enables a persistent local effect.
- **Revenue program:** an engine-supported export or payment is causally linked to output.

The current prototype is a **prestige sink candidate**. It has no demonstrated launch-dependent revenue and therefore no documented payback period.

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

Later "unlocks" are `$AVAILABLE` years on the heavier vehicles plus extra buildings, not a Glory counter hitting 30.

## Export safety valve candidate (post-P3)

A sellable Vestnik variant without `$CARGOVEHICLE_MUSTBE_LOADED` may be tested after the physical payload chain works. It is a separate revenue mechanic, not evidence of a launch payout. Do not add it while validating S8 because an export route would hide failures in the pad chain.

## What not to tune

- Do not lower professor counts to "make it accessible". Accessibility is "grey-box loop works", not "space program runs on elementary school".
- Do not add dollars-only vehicles. `$COST_RUB 1` on Soviet hardware.
- Do not modify vanilla factory rates to feed Kosmograd.
