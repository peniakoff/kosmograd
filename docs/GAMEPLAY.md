# Gameplay loop

The player never clicks a "Launch" button in empty air. The pad only does something when every input has physically arrived.

## Sputnik core loop (P1) — the contract

1. Mid/late-game republic already smelts steel and aluminium and makes `mcomponents` and `ecomponents` / `eletronics`.
2. **Assembly Center** receives vanilla resources and emits **Zarya-K1**, an airplane flagged for transport as cargo.
3. Player assigns a locomotive plus the **Transporter-Erector** wagon. The verified loading arrangement places Zarya-K1 on the train and carries it over the tested railway geometry to the pad.
4. The pad unloads the rocket onto the airplane stand.
5. If P0 proves fuel transfer, vanilla fuel must reach the pad before departure.
6. The rocket completes the exact lifecycle demonstrated by spike S4. Documentation must name that behavior precisely; it must not say "launch and despawn" unless both occurred in game.
7. Any monument loyalty is a static district or completion benefit unless spike S6 proves an event-driven effect.

If required resources, staff or rail transport are missing, the core loop stops. Fuel is part of this gate only after S5 passes.

## Player-facing difficulty (by design)

- **Professors.** Factories will not run on elementary labour. The player must have universities before aerospace is honest.
- **Verified rail geometry.** The erector mesh is long. P0 records the supported minimum curve and switch layout instead of relying only on a warning.
- **Fuel may be a gate.** Include it only if the pad-to-airplane transfer and consumption are measurable.
- **One pad.** `$STATION_NOT_BLOCK` exists so a fuel tanker and a train can coexist. It is not a second pad.

## What the player is not asked to do in P1

- Train cosmonauts.
- Research a tech tree (years on `$AVAILABLE` are the only gate).
- Win a race against another nation.
- Recover boosters.
- Export Vestnik-1 for cash.

## P3 extended logistics

Rocket Factory, Satellite Factory, K-1 stages, Vestnik-1 and the dedicated Fuel Refinery are P3 content. Start them only after S8 proves that physical vehicle deliveries can causally gate Zarya production. Parallel decorative deliveries that do not affect the output do not satisfy the project pillar of real logistics.

## P4 layers (do not leak into P1 assets)

| Layer | Loop addition |
|---|---|
| Tracking / mission control | Extra workers and a coverage fiction; attraction score |
| Crewed | Citizens (passengers) from quarters → training → pad; Chaika as cargo/airplane |
| Heavy lift | Second pad, Bogatyr, longer rail |
| Museum | Culture + loyalty; the "Glory multiplier" analogue |

Crewed flight uses **passengers**, not a new "crew" resource. Training center is a building that needs educated workers and time; the "roster" is the citizens who live in the quarters. There is no custom crew UI.

## Failure

P1 is deterministic: inputs + staff + verified transport state = the verified endpoint. Random failure is out of scope for the v1 line.
