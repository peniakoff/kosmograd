# Architecture

Workers & Resources has no space program. Kosmograd is a composition of types the engine already understands.

Read [DECISIONS.md](DECISIONS.md) for why this composition won. Read [ASSETS.md](ASSETS.md) for per-asset tokens. This file is the machine as a whole.

## Constraints the design respects

- One `$TYPE` per building.
- No new resource types.
- No custom UI.
- No launch physics beyond what an airplane already does.
- Max 32 buildings + vehicles per Workshop item (wiki). Sputnik P1 is 5 + 4 = 9. Headroom is for P3.
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

If spike S3 fails (it taxis, tips, or seeks a civilian runway), stop fighting the airplane AI. Switch the pad to the consumption fallback. Do not add a second rocket type "just in case" — change the pad, keep the vehicle as a must-be-loaded hull the factory still produces.

### 2. Stages and the satellite are cargo vehicles

`kosm_stage_k1` and `kosm_vestnik_1` are road vehicles with `$MOVEMENT_SPEED 0` (or omitted / zero) and `$CARGOVEHICLE_MUSTBE_LOADED`. Factories produce them the way a car plant produces cars. Open-hull trucks haul them. They never drive.

This is the only way to "manufacture a satellite" without a new resource.

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

Unloading a vehicle wagon onto an airplane stand **is spike S2**. If a cargo airport will not accept vehicle cargo from rail, split:

```text
kosm_rail_terminus   $TYPE_CARGO_STATION   (rail in, vehicles out to short road)
kosm_launch_pad      $TYPE_AIRPLANE_PARKING or $TYPE_CARGO_STATION $SUBTYPE_AIRPLANE
```

and make the player haul the last hundred metres by a heavy road trailer — worse poetry, same loop.

Loyalty is **not** a second `$TYPE` on the pad. Try monument tokens on the pad first (they sit in the "other tokens" list, not only under `$TYPE_MONUMENT`). If they no-op, ship `kosm_memorial_plaza` as `$TYPE_MONUMENT` beside the pad (P3 priority A, or P1 hotfix).

## Building types (P1)

| Building | `$TYPE` | `$SUBTYPE` | Produces / does |
|---|---|---|---|
| Rocket factory | `$TYPE_PRODUCTION_LINE` | `$SUBTYPE_ROAD` | `kosm_stage_k1` vehicles |
| Satellite factory | `$TYPE_PRODUCTION_LINE` | `$SUBTYPE_ROAD` | `kosm_vestnik_1` vehicles |
| Assembly center | `$TYPE_PRODUCTION_LINE` | `$SUBTYPE_AIRPLANE` | `kosm_zarya_k1` airplane |
| Fuel refinery | `$TYPE_FACTORY` | — | vanilla `fuel` from `oil` + `chemicals` |
| Launch pad | `$TYPE_CARGO_STATION` | `$SUBTYPE_AIRPLANE` | unload, fuel, park, launch |

`$TYPE_PRODUCTION_LINE` `$SUBTYPE_ROAD` is how vanilla vehicle plants work. If a copied vanilla car plant uses a different type, **the vanilla file wins** — retcon this table after P0.

## Fuel

Appendix A of the building guide (2024) lists `oil` and `chemicals` and does not list `fuel`. Vanilla oil refineries still produce vehicle fuel. During P0, open a vanilla refinery `building.ini` and copy the output token **verbatim**.

Until that copy exists, docs use `fuel` as the working name.

The PDF wanted a unique RP-K blend. That would be a new resource. Instead the refinery is a **worse vanilla refinery**: it burns chemicals as well as oil, so the space program is not a free tap on the existing fuel network. The pad stores fuel with `$STORAGE_FUEL`.

If `fuel` cannot be produced by a custom factory, the refinery becomes a themed tank farm (`$STORAGE_FUEL` only, `$TYPE_STORAGE` or a factory that only stores) and the airplane refuels from oil. Record that in DECISIONS.md. Do not invent `rp_k`.

## Power, workers, professors

Space buildings need university labour. Use `$WORKERS_NEEDED` plus `$PROFESORS_NEEDED` (the token is misspelled that way in the engine). Electricity via `$CONSUMPTION_PER_SECOND eletric` (also misspelled). Copy wattage style from a vanilla electronics plant, then raise it.

## Construction

Do not hand-author ruble costs. Use `$COST_WORK` phases and `$COST_RESOURCE_AUTO` so the bounding box of the mesh *is* the bill. Grey-boxes with the final footprint therefore have near-final cost. That is why grey-box dimensions in `ASSETS.md` are frozen.

## Data flow (P1)

```text
                    mcomponents, steel, aluminium
                                │
                     kosm_rocket_factory
                                │  kosm_stage_k1  (truck, open)
                                ▼
                     kosm_assembly_center  ◄── kosm_vestnik_1 (truck)
                                │
                                │  consumes stages + satellite as
                                │  imported vehicles, outputs kosm_zarya_k1
                                ▼
                  kosm_transporter_erector  (train)
                                │
                                ▼
                       kosm_launch_pad
                                ▲
                     kosm_fuel_refinery
                      oil + chemicals → fuel
```

How a production line *consumes vehicles* as inputs is the fragile joint. Vanilla car plants consume **resources** and emit vehicles. They do not eat other cars.

**If the VAB cannot take vehicles as inputs**, use this fallback (still P1, still no new resource):

- Rocket factory and satellite factory still emit cargo vehicles (visual logistics).
- Those vehicles are hauled to the VAB and stored in `$STORAGE_IMPORT` of type `RESOURCE_TRANSPORT_VEHICLES` if the type allows it.
- If import-of-vehicles fails, the two feeder factories become **thematic resource sinks** that consume the same vanilla goods the VAB also consumes, and the cargo vehicles are optional flavour produced at low rate. The VAB then builds Zarya-K1 from resources only.

The preferred fiction is physical stages on trucks. The required fiction is a rocket that must be railed to the pad. Cut the feeder vehicles before cutting the erector.

## What we do not script

There is no mission duration, no countdown UI, no success roll in P1. Staffing + inputs + a takeoff (or consume) **is** the mission. A later optional failure module stays a toggle in the PDF's sense and is out of scope until the loop is boringly reliable.

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
