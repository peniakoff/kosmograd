# Architecture

Workers & Resources has no space program. Kosmograd is an attempt to compose types the engine already understands. Until P0B passes, this file describes the target architecture rather than confirmed engine behavior.

Read [DECISIONS.md](DECISIONS.md) for why this composition won. Read [ASSETS.md](ASSETS.md) for per-asset tokens. This file is the machine as a whole.

## Constraints the design respects

- One `$TYPE` per building.
- No new resource types.
- No custom UI.
- No launch physics beyond what an airplane already does.
- Max 32 buildings + vehicles per Workshop item (wiki). Sputnik P1 is 2 + 2 = 4. Mixed-pack loading and paths still require spike S7.
- Spaces in `$NAME_STR` quotes only. No spaces in folder names.

## The four engine tricks

### 1. The rocket is an airplane

`kosm_zarya_k1` is `$TYPE VEHICLETYPE_AIRPLANE`.

| Token | Intent |
|---|---|
| `$CARGOVEHICLE_MUSTBE_LOADED` | It does not taxi out of the VAB. It is cargo until the pad. |
| `$TAKEOFF_DISTANCE` ~ 1 | Short / vertical-ish roll. Exact value from vanilla the smallest STOL, then tune. |
| `$MOVEMENT_EMPTY_WEIGHT` ~ 280 | Heavy. Needs a wagon that can take it. |
| Mesh authored **nose up** (+Y in game space) | Parked, it stands. This is the erection illusion. |

Vanilla airplanes sit on their belly along the parking Z axis. We do not animate a tilt-up. We author the mesh already vertical and rotate it **down** only while it is visualized as wagon cargo (`$CARGOVEHICLE_VISUALIZATION` rotation on the erector).

Spike S4 must document the airplane's complete lifecycle: route requirements, departure, persistence or removal, and repeatability after save/load. If it taxis, tips, seeks a civilian runway or cannot reach a stable endpoint, use the P0 **PIVOT** decision. There is no accepted consumption fallback yet.

### 2. Stages and the satellite are P3 cargo-vehicle candidates

`kosm_stage_k1` and `kosm_vestnik_1` are road vehicles with `$MOVEMENT_SPEED 0` (or omitted / zero) and `$CARGOVEHICLE_MUSTBE_LOADED`. Factories produce them the way a car plant produces cars. Open-hull trucks haul them. They never drive.

This is a plausible way to manufacture a satellite without a new resource. P3 proceeds only if S8 proves that delivering these vehicles can causally gate VAB output.

### 3. The erector is a rail wagon that carries vehicles

`kosm_transporter_erector`:

```text
$TYPE VEHICLETYPE_RAIL_VAGON
$TRAINGROUP_VAGON
$RESOURCE_TRANSPORT_TYPE RESOURCE_TRANSPORT_VEHICLES
$RESOURCE_CAPACITY 300
$CARGOVEHICLE_VISUALIZATION   ← box large enough for a 280 t, ~33 m hull
```

Long wheelbase in the **mesh** (multiple bogies as geometry) makes tight curves look wrong and play badly. That is the gentle-curve requirement. There is no `$WHEEL_` token in the vehicle guide; bogies are model.

Couple to any vanilla diesel the player already has (TE3-class). Do not ship a locomotive in P1.

### 4. The pad is a cargo airport, not a monument-that-launches

Intended type: `$TYPE_CARGO_STATION` with `$SUBTYPE_AIRPLANE`.

That one type is allowed to have:

- `$CONNECTION_RAIL` — train pulls in
- `$VEHICLE_STATION` — not always needed for rail; copy a vanilla mixed cargo station
- `$AIRPLANE_STATION_50M` — the rocket stand (50 m class; Zarya-K1 is a large object)
- `$STORAGE_FUEL` — local fuel so the airplane can fill before takeoff
- `$CONNECTION_PIPE_INPUT` — fuel in
- `$STATION_NOT_BLOCK` — do not deadlock the only pad

Unloading a vehicle wagon onto an airplane stand is spike S3. If a cargo airport will not accept vehicle cargo from rail, test the split candidate:

```text
kosm_rail_terminus   $TYPE_CARGO_STATION   (rail in, vehicles out to short road)
kosm_launch_pad      $TYPE_AIRPLANE_PARKING or $TYPE_CARGO_STATION $SUBTYPE_AIRPLANE
```

This split becomes an accepted fallback only after a cube test proves the transfer between both buildings.

Loyalty is not a second `$TYPE` on the pad. S6 checks whether monument tokens are accepted there, but their documented meaning is a static radius/strength effect. If needed, `kosm_memorial_plaza` may become a separate completion reward. Neither form is described as triggered by a launch without evidence.

## Building types

| Building | `$TYPE` | `$SUBTYPE` | Produces / does |
|---|---|---|---|
| Assembly center (P1) | `$TYPE_PRODUCTION_LINE` | `$SUBTYPE_AIRPLANE` | resources → `kosm_zarya_k1` airplane |
| Launch pad | `$TYPE_CARGO_STATION` | `$SUBTYPE_AIRPLANE` | unload, fuel, park, launch |
| Rocket factory (P3 candidate) | `$TYPE_PRODUCTION_LINE` | `$SUBTYPE_ROAD` | `kosm_stage_k1` vehicles |
| Satellite factory (P3 candidate) | `$TYPE_PRODUCTION_LINE` | `$SUBTYPE_ROAD` | `kosm_vestnik_1` vehicles |
| Fuel refinery (P3 candidate) | `$TYPE_FACTORY` | — | vanilla `fuel` from `oil` + `chemicals` |

`$TYPE_PRODUCTION_LINE` `$SUBTYPE_ROAD` is how vanilla vehicle plants work. If a copied vanilla car plant uses a different type, **the vanilla file wins** — retcon this table after P0.

## Fuel

Appendix A of the building guide (2024) lists `oil` and `chemicals` and does not list `fuel`. Vanilla oil refineries still produce vehicle fuel. During P0, open a vanilla refinery `building.ini` and copy the output token **verbatim**.

Until that copy exists, docs use `fuel` as the working name.

The PDF wanted a unique RP-K blend. That would be a new resource. Instead the refinery is a **worse vanilla refinery**: it burns chemicals as well as oil, so the space program is not a free tap on the existing fuel network. The pad stores fuel with `$STORAGE_FUEL`.

The dedicated refinery is P3 content. If custom production is not proven, omit it and use vanilla fuel. Do not add a themed duplicate that creates no new decision, and do not invent `rp_k`.

## Power, workers, professors

Space buildings need university labour. Use `$WORKERS_NEEDED` plus `$PROFESORS_NEEDED` (the token is misspelled that way in the engine). Electricity via `$CONSUMPTION_PER_SECOND eletric` (also misspelled). Copy wattage style from a vanilla electronics plant, then raise it.

## Construction

Do not hand-author ruble costs. Start with copied `$COST_WORK` phases and `$COST_RESOURCE_AUTO`, then record the actual construction bill in the pinned game build. Geometry and named construction nodes affect the result, but documentation must not infer a ruble total from footprint alone.

## Data flow (P1 core)

```text
             steel, aluminium, mcomponents, ecomponents
                                │
                                ▼
                     kosm_assembly_center
                                │
                                │  outputs kosm_zarya_k1
                                ▼
                  kosm_transporter_erector  (train)
                                │
                                ▼
                       kosm_launch_pad
                                ▲
                         vanilla fuel
```

P1 intentionally feeds the VAB with resources. It does not pretend that parallel stage or satellite deliveries are consumed. S8 separately tests whether the physical P3 chain is possible. If S8 fails, the feeder factories and cargo vehicles remain unshipped; duplicated thematic resource sinks are not an acceptable substitute for causality.

## What we do not script

There is no mission duration, countdown UI or success roll in P1. Staffing, inputs, physical transport and the endpoint proven by S4 are the mission. Random failure is out of scope for the v1 line.

## File layout inside a Workshop item

```text
workshop_wip/<ITEM_ID>/          ← Steam creates this
├── workshopconfig.ini           ← Steam writes IDs; we add $OBJECT_* lines
├── previewimage.png
├── description.txt
├── buildings/
│   └── kosm_<name>/
│       ├── model.nmf            ← from Blender OBJ via ModelViewer
│       ├── material.mtl
│       ├── material_e.mtl       ← night emissive, optional
│       ├── diffuse.dds
│       ├── building.ini
│       ├── renderconfig.ini
│       └── imagegui.png         ← 96×96
└── vehicles/
    └── kosm_<name>/
        ├── main.nmf
        ├── material.mtl
        ├── script.ini
        └── (dds as referenced by mtl)
```

`building.bbox`, `building.fire`, `bbox.bin`, `preview.dds` are **generated on first load**. Do not commit them. Do not copy them from another mod.

`$OBJECT_BUILDING buildings/kosm_rocket_factory` must match the folder path relative to the item root. If a given game version rejects slashes, flatten to `kosm_rocket_factory` at the item root and update `workshopconfig.ini`. That flatten is a deploy detail, not a redesign.
