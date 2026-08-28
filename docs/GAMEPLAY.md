# Gameplay loop

The player never clicks a "Launch" button in empty air. The pad only does something when every input has physically arrived.

## Sputnik loop (P1) — the contract

1. Mid/late-game republic already smelts steel and aluminium, already makes `mcomponents` and `ecomponents` / `eletronics`, already pumps oil and chemicals.
2. **Rocket Factory** turns steel, aluminium, and mechanical components into **K-1 stages** (cargo vehicles). Open trucks haul them.
3. **Satellite Factory** turns aluminium, electronics/components, and mechanical components into **Vestnik-1** (cargo vehicle). Covered or open trucks haul it.
4. **Assembly Center** receives those vehicles (preferred) or the same vanilla resources (fallback) and emits **Zarya-K1**, an airplane that cannot taxi.
5. Player assigns a locomotive plus the **Transporter-Erector** wagon. The train enters the assembly center (or the adjacent rail terminus), loads Zarya-K1, and runs a **wide-radius** railway to the pad.
6. **Fuel Refinery** turns oil + chemicals into vanilla fuel. Pipes or tankers fill the pad.
7. Pad unloads the rocket onto the 50 m airplane stand (erection illusion), fuels it, and the vehicle takes off — or, if S3 failed, the pad consumes it.
8. Monument loyalty tokens fire. The republic feels the launch.

If any truck, pipe, professor, or rail car is missing, there is no launch. That is the game.

## Player-facing difficulty (by design)

- **Professors.** Factories will not run on elementary labour. The player must have universities before aerospace is honest.
- **Gentle rail.** The erector mesh is long. Tight switches clip, look wrong, and may stuck-queue. The tutorial text in `description.txt` says so.
- **Fuel is not free.** Chemicals + oil, not a tap on the existing petrol network alone.
- **One pad.** `$STATION_NOT_BLOCK` exists so a fuel tanker and a train can coexist. It is not a second pad.

## What the player is not asked to do in P1

- Train cosmonauts.
- Research a tech tree (years on `$AVAILABLE` are the only gate).
- Win a race against another nation.
- Recover boosters.
- Export Vestnik-1 for cash (P3 safety valve).

## P3 layers (do not leak into P1 assets)

| Layer | Loop addition |
|---|---|
| Tracking / mission control | Extra workers and a coverage fiction; attraction score |
| Crewed | Citizens (passengers) from quarters → training → pad; Chaika as cargo/airplane |
| Heavy lift | Second pad, Bogatyr, longer rail |
| Museum | Culture + loyalty; the "Glory multiplier" analogue |

Crewed flight uses **passengers**, not a new "crew" resource. Training center is a building that needs educated workers and time; the "roster" is the citizens who live in the quarters. There is no custom crew UI.

## Failure (optional, post-P1)

P1 is deterministic: inputs + staff = success. A later toggle may add chance. If event scripting cannot do it, it is cut. It must never be on by default in a Sputnik release.
