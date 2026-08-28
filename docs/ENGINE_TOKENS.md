# Engine tokens

Source of truth for "does this token exist?": LovelyPL's Steam guides and vanilla files. This page is a working subset for Kosmograd. When vanilla disagrees, vanilla wins.

Legend: **OK** = in the public guides · **COPY** = copy from a named vanilla file, token may exist beyond the appendix · **UNVERIFIED** = hypothesis, P0 must confirm · **REJECTED** = appeared in early drafts, do not use.

## Buildings — types we actually use

| Token | Status | Notes |
|---|---|---|
| `$TYPE_FACTORY` | OK | Fuel refinery |
| `$TYPE_PRODUCTION_LINE` | OK | Vehicle / airplane plants |
| `$SUBTYPE_ROAD` | OK | With production line |
| `$SUBTYPE_AIRPLANE` | OK | With production line **or** cargo station |
| `$SUBTYPE_RAIL` | OK | Train plants; not P1 pad |
| `$TYPE_CARGO_STATION` | OK | Pad |
| `$TYPE_AIRPLANE_PARKING` | OK | S2 fallback for pad |
| `$TYPE_MONUMENT` | OK | Memorial plaza |
| `$TYPE_ATTRACTION` | OK | Museum |
| `$TYPE_STORAGE` | OK | Fuel farm fallback |
| `$SUBTYPE_SPACE_FOR_VEHICLES` | OK | With storage |

One type only. Subtype is extra, not a second type.

## Buildings — production and people

| Token | Status |
|---|---|
| `$NAME_STR "…"` | OK |
| `$WORKERS_NEEDED n` | OK |
| `$PROFESORS_NEEDED n` | OK (spelling) |
| `$PRODUCTION resource amount` | OK — amount is **per worker per workday** |
| `$CONSUMPTION resource amount` | OK |
| `$CONSUMPTION_PER_SECOND eletric n` | OK (spelling `eletric`) |
| `$STORAGE_IMPORT type capacity` | OK |
| `$STORAGE_EXPORT type capacity` | OK |
| `$STORAGE_IMPORT_SPECIAL type capacity resource` | OK |
| `$STORAGE_EXPORT_SPECIAL type capacity resource` | OK |
| `$STORAGE_IMPORT_CARPLANT type capacity` | OK — copy from vanilla car plant if VAB needs it |
| `$STORAGE_FUEL type amount` | OK |
| `$VEHICLE_LOADING_FACTOR n` | OK |
| `$VEHICLE_UNLOADING_FACTOR n` | OK |
| `$VEHICLE_UNLOADINGLOADING_MAXVAGONS n` | OK |
| `$STATION_NOT_BLOCK` | OK |
| `$WORKING_VEHICLES_NEEDED n` | OK |

## Buildings — connections and slots

Coordinates: two points `(x y z)` `(x2 y2 z2)`. **Y is up.** Y = 0 is ground for vehicle paths.

| Token | Status |
|---|---|
| `$CONNECTION_ROAD` | OK |
| `$CONNECTION_RAIL` | OK |
| `$CONNECTION_PIPE_INPUT` / `_OUTPUT` | OK |
| `$CONNECTION_PEDESTRIAN` | OK |
| `$CONNECTION_ELETRIC_HIGH_INPUT` etc. | OK |
| `$CONNECTION_AIRROAD` | OK |
| `$VEHICLE_STATION x y z x2 y2 z2` | OK |
| `$AIRPLANE_STATION_30M` / `_40M` / `_50M` | OK |
| `$PARTICLE type x y z alpha scale` | OK |
| `$COST_WORK phase factor` | OK |
| `$COST_WORK_BUILDING_NODE Name` | OK |
| `$COST_RESOURCE_AUTO preset factor` | OK |
| `$MONUMENT_GOVERNMENT_LOYALTY_RADIUS n` | OK |
| `$MONUMENT_GOVERNMENT_LOYALTY_STRENGTH n` | OK |
| `$NO_LIFESPAN` | OK |

## Buildings — REJECTED (do not put in ini files)

| Draft token | Use instead |
|---|---|
| `$RAIL_NODE` | `$CONNECTION_RAIL` |
| `$STATION_TRAIN` | cargo station type + `$CONNECTION_RAIL` |
| `$LOADING_VEHICLES` | vehicle cargo type on the **wagon** + stations on the building |
| `$UNLOADING_VEHICLES` | same |
| `$TYPE_AIRPLANE` as a building type | `$TYPE_PRODUCTION_LINE` `$SUBTYPE_AIRPLANE` or `$TYPE_CARGO_STATION` `$SUBTYPE_AIRPLANE` |
| JSON `"inputs": {…}` | `$CONSUMPTION` / `$PRODUCTION` lines |

## Vehicles — types

| Token | Status |
|---|---|
| `$TYPE VEHICLETYPE_AIRPLANE` | OK |
| `$TYPE VEHICLETYPE_RAIL_VAGON` | OK (not `WAGON`) |
| `$TYPE VEHICLETYPE_ROAD` | OK |
| `$TRAINGROUP_VAGON` | OK |
| `$NAME_STR "…"` | OK |
| `$COUNTRY 39011` | OK |
| `$AVAILABLE y1 y2` | OK |
| `$COST_RUB 1` | OK |
| `$MOVEMENT_SPEED n` | OK — **0 means must be hauled** |
| `$MOVEMENT_POWER_KW n` | OK |
| `$MOVEMENT_EMPTY_WEIGHT n` | OK (tons) |
| `$RESOURCE_TRANSPORT_TYPE RESOURCE_TRANSPORT_VEHICLES` | OK |
| `$RESOURCE_CAPACITY n` | OK (tons or passengers) |
| `$CARGOVEHICLE_MUSTBE_LOADED` | OK |
| `$CARGOVEHICLE_CANBE_LOADED` | OK |
| `$CARGOVEHICLE_VISUALIZATION min … max …` | OK |
| `$TAKEOFF_DISTANCE n` | OK (meters) |
| `$MOVEMENT_WHEEL_FRONT` / `_BACK` | OK |
| `$PARTICLE_MOVEMENT type x y z` | OK |
| `$PURCHASE_EXCLUDE` | OK — on cargo hulls the player should not buy in the shop |
| `$SOUND_PARAMS path` | COPY from similar vanilla vehicle |

## Vehicles — REJECTED

| Draft token | Use instead |
|---|---|
| `$TYPE WAGON` | `$TYPE VEHICLETYPE_RAIL_VAGON` |
| `$CARGO_TYPE VEHICLES` | `$RESOURCE_TRANSPORT_TYPE RESOURCE_TRANSPORT_VEHICLES` |
| `$MAX_CARGO_WEIGHT` | `$RESOURCE_CAPACITY` |
| `$WHEEL_BOGIE_…` | mesh naming; game infers turning wheels |
| `$PARTICLE_MOVEMENT factory_big_gray` | building particle; not for vehicles |

## Vanilla resources (Appendix A, plus COPY)

Use these strings in `$PRODUCTION` / `$CONSUMPTION` / `$RESOURCE_ALLOW_ONLY`:

`alcohol alumina aluminium asphalt bauxite boards bricks chemicals clothes concrete ecomponents eletric eletronics food gravel mcomponents meat nuclearfuel oil plants prefabpanels steel uf6 uranium usagewater waste water wood workers yellowcake`

**COPY:** `fuel` — confirm in vanilla oil refinery `building.ini` during P0. Never invent `avionics`, `propellant`, `glory`, `rp_k`.

Note spellings: `aluminium`, `eletronics`, `ecomponents`, `mcomponents`, `eletric`.

## Cargo kinds (Appendix F)

`RESOURCE_TRANSPORT_PASSANGER` (engine spelling), `CEMENT`, `COVERED`, `GRAVEL`, `OIL`, `OPEN`, `COOLER`, `CONCRETE`, `LIVESTOCK`, `GENERAL`, `VEHICLES`, `WATER`, `SEWAGE`.

## Construction phases (Appendix B)

`SOVIET_CONSTRUCTION_GROUNDWORKS`  
`SOVIET_CONSTRUCTION_BOARDS_LAYING`  
`SOVIET_CONSTRUCTION_BRICKS_LAYING`  
`SOVIET_CONSTRUCTION_SKELETON_CASTING`  
`SOVIET_CONSTRUCTION_STEEL_LAYING`  
`SOVIET_CONSTRUCTION_PANELS_LAYING`  
`SOVIET_CONSTRUCTION_ROOFTOP_BUILDING`  
`SOVIET_CONSTRUCTION_WIRE_LAYING`

## Particle names (buildings)

`factory_big_black` `factory_medium_black` `factory_small_black`  
`factory_big_gray` `factory_medium_gray` `factory_small_gray`  
`factory_big_white` `factory_medium_white` `factory_small_white`

Vehicles: `vehicle_medium` `train_electric` `train_small` `train_medium` — plus **COPY** from a vanilla jet for exhaust.
