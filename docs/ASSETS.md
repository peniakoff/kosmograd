# Asset bible — configuration and 3D

This is the only per-asset specification. If a value is not here, it is not decided.

For every object: engine tokens, logistics role, Blender geometry, textures, sockets, and a Blender MCP prompt. Grey-box first. Art second. Do not model a pretty hall with the wrong door.

**Related:** [ARCHITECTURE.md](ARCHITECTURE.md) · [ENGINE_TOKENS.md](ENGINE_TOKENS.md) · [NAMING.md](NAMING.md) · [BLENDER.md](BLENDER.md) · [BLENDER_MCP.md](BLENDER_MCP.md) · [ECONOMY.md](ECONOMY.md)

Coordinate system in-game: **X Z ground plane, Y up, metres**. Blender is Z-up internally; export converts (see BLENDER.md). Origins: **ground plane, footprint centre**, unless a vehicle note says otherwise.

---

## Shared 3D laws

| Rule | Value |
|---|---|
| Scale | 1 Blender unit = 1 metre after export |
| Origin (buildings) | Ground, centre of footprint rectangle |
| Origin (road/rail vehicles) | Ground, between the bogies / axles, facing **+Z** in Blender before axis convert (confirm with a vanilla OBJ dump in P0) |
| Origin (Zarya-K1) | Ground at nozzle plane, stack along **+Y game** (vertical) |
| Faces | Triangles only. Merge by distance before export |
| Transforms | Apply all (location, rotation, scale) before export |
| Naming | `KOSM_<cat>_<name>_vNN` for the root; construction nodes ASCII no spaces |
| Textures | DDS after paint.net/GIMP. 1024² default, 2048² landmarks only |
| Atlas | Shared concrete/metal for all P1 buildings (`blender/atlas/kosm_concrete_metal.png`) |
| Weathering | Painted (soot, rust streaks, oil). Not extra geometry |
| Night | Optional `material_e.mtl`: black except lit windows / beacons |
| LOD | Not in P1. Add `$LOD1` only if FPS fails the 5% gate |
| Do not ship | Ngons, unapplied mirrors, subdivision modifiers live on export, PBR node graphs (the game is MTL + DDS) |

### Polygon ceilings (do not exceed)

| Class | Tris | Texture |
|---|---|---|
| Landmark building (pad, VAB) | 8 000 | 2048² |
| Standard production | 5 000 | 1024² |
| Small support | 2 500 | 1024² |
| Rocket airplane | 10 000 | 1024² |
| Wagon | 6 000 | 1024² |
| Cargo hull (stage / satellite) | 4 000 | 1024² |
| Grey-box stand-in | 12–40 | 256² flat colour |

### Grey-box colours (viewport / 256²)

| Role | Hex |
|---|---|
| Production hall | `#8A9AA8` |
| Pad / concrete | `#B7B3A8` |
| Vehicle rocket | `#C9C4B8` |
| Wagon | `#5C6570` |
| Cargo | `#D4A574` |

### Construction phases (every building)

Copy this block into each `building.ini` and keep node names in the mesh:

```ini
$COST_WORK SOVIET_CONSTRUCTION_GROUNDWORKS 0.0
$COST_WORK_BUILDING_NODE Main
$COST_WORK_VEHICLE_STATION_ACCORDING_NODE Main
$COST_RESOURCE_AUTO ground_asphalt 1.0

$COST_WORK SOVIET_CONSTRUCTION_SKELETON_CASTING 1.0
$COST_RESOURCE_AUTO wall_concrete 1.0
$COST_WORK_VEHICLE_STATION 0 0 8  0 0 14

$COST_WORK SOVIET_CONSTRUCTION_PANELS_LAYING 1.0
$COST_RESOURCE_AUTO wall_panels 1.0

$COST_WORK SOVIET_CONSTRUCTION_STEEL_LAYING 1.0
$COST_RESOURCE_AUTO tech_steel 1.0

$COST_WORK SOVIET_CONSTRUCTION_WIRE_LAYING 1.0
$COST_RESOURCE_AUTO electro_steel 0.6
```

Tune factors after the first in-game cost readout. Crane slot coordinates must sit on empty ground next to the grey-box, not inside the mesh.

### `renderconfig.ini` (every building)

Start from a vanilla hall of similar size. Working template (confirm field names in P0):

```ini
MODEL model.nmf
MATERIAL material.mtl
```

Night variant if present: second material `material_e.mtl` as vanilla does.

### `imagegui.png`

96 × 96 px, PNG, readable silhouette, no tiny text.

---

# P1 buildings

## 1. Kosmograd Rocket Factory

| | |
|---|---|
| Folder | `workshop/buildings/kosm_rocket_factory/` |
| Display | `$NAME_STR "Kosmograd Rocket Factory"` |
| Phase | P1 |
| Role | Produces `kosm_stage_k1` cargo vehicles for open trucks |
| Inspired by | MIK / horizontal booster halls, not a named OKB |

### Engine

```ini
$NAME_STR "Kosmograd Rocket Factory"
$TYPE_PRODUCTION_LINE
$SUBTYPE_ROAD

$WORKERS_NEEDED 85
$PROFESORS_NEEDED 10

$CONSUMPTION steel 0.141
$CONSUMPTION aluminium 0.047
$CONSUMPTION mcomponents 0.038
$CONSUMPTION_PER_SECOND eletric 0.35

$STORAGE_IMPORT RESOURCE_TRANSPORT_OPEN 80
$STORAGE_IMPORT RESOURCE_TRANSPORT_COVERED 40
$STORAGE_EXPORT RESOURCE_TRANSPORT_VEHICLES 4

$STATION_NOT_BLOCK
$VEHICLE_LOADING_FACTOR 3
$VEHICLE_UNLOADING_FACTOR 3

$ELETRIC_WITHOUT_WORKING_FACTOR 0.0
$POLLUTION_SMALL
```

`$PRODUCTION` of a **vehicle** is not a resource line. **COPY** a vanilla vehicle production line (car plant / truck plant) for the token that spawns the vehicle, then point it at `kosm_stage_k1`. If the vanilla file uses workshop-relative folder names, use `kosm_stage_k1`.

Per-worker consumption figures assume 85 workers and the [ECONOMY.md](ECONOMY.md) totals. Recalculate if worker count changes.

### Connections (grey-box, metres from origin)

Footprint **34 × 46 m**. Hall long axis along **Z**. Road on the −Z gable (loading court). Pedestrian on the office +X side. Power on the −X service strip.

| Socket | Approx. |
|---|---|
| `$CONNECTION_ROAD` | `(0, 0, -23)` dir `(0, 0, -24)` |
| `$CONNECTION_PEDESTRIAN` | `(17, 0, -8)` dir `(18, 0, -8)` |
| `$CONNECTION_ELETRIC_HIGH_INPUT` | `(-17, 0, 0)` dir `(-18, 0, 0)` |
| `$VEHICLE_STATION` (unload mats) | `(8, 0, -18)` turn `(8, 0, -10)` |
| `$VEHICLE_STATION` (load stages) | `(-8, 0, -18)` turn `(-8, 0, -10)` |

Place `$STATION_NOT_BLOCK_DETOUR_POINT` in the court so two trucks can pass.

### 3D

| | |
|---|---|
| Size | 34 × 12 m high × 46 m |
| Budget | 5 000 tris, 1024² (atlas) |
| Grey-box | One box 34 × 12 × 46 named `Main` |
| Final silhouette | Long MIK-style hall, **two arched roof bays**, rail-style sliding doors on the −Z gable even if P1 is road-only (visual), blue-grey panels, red star **painted** on the texture over the gate (not geometry), external pipe run on −X |
| Nodes | `Main` (always). Optional `Office` as a 6 m front block if tris remain |
| Doors | Opening not required in P1 (`$MOVEABLE_DOOR` later) |
| Particles | Optional `$PARTICLE factory_small_gray` at roof vents |

**Not in the mesh:** interiors, chairs, a full rocket. The product is a vehicle the factory emits.

### Blender MCP prompt (grey-box)

```text
Scene units metres. Delete default cube.
Create a mesh cube named Main, size X=34 Y=12 Z=46, origin at ground centre
(so the cube sits on Z=0 in Blender: origin at geometric centre then
location z = 6). Apply transforms after moving.
Assign a flat material hex #8A9AA8.
Add three Empty objects (plain axes) named sock_road, sock_ped, sock_power
at the connection coordinates converted to Blender Z-up
(game y-up (x,y,z) → Blender (x,z,y)).
Export selected meshes to blender/assets/buildings/kosm_rocket_factory/export/model.obj
with triangulate, applied transforms, axis conversion Y-up.
Save blender/assets/buildings/kosm_rocket_factory/kosm_rocket_factory.blend
```

---

## 2. Kosmograd Satellite Factory

| | |
|---|---|
| Folder | `workshop/buildings/kosm_satellite_factory/` |
| Display | `$NAME_STR "Kosmograd Satellite Factory"` |
| Phase | P1 |
| Role | Produces `kosm_vestnik_1` |
| Inspired by | Clean-room annex + hall, still panel architecture |

### Engine

```ini
$NAME_STR "Kosmograd Satellite Factory"
$TYPE_PRODUCTION_LINE
$SUBTYPE_ROAD

$WORKERS_NEEDED 60
$PROFESORS_NEEDED 12

$CONSUMPTION aluminium 0.013
$CONSUMPTION ecomponents 0.020
$CONSUMPTION mcomponents 0.007
$CONSUMPTION_PER_SECOND eletric 0.28

$STORAGE_IMPORT RESOURCE_TRANSPORT_COVERED 50
$STORAGE_IMPORT RESOURCE_TRANSPORT_OPEN 20
$STORAGE_EXPORT RESOURCE_TRANSPORT_VEHICLES 4

$STATION_NOT_BLOCK
$ELETRIC_WITHOUT_WORKING_FACTOR 0.0
```

If vanilla electronics output is `eletronics` not `ecomponents`, **COPY** that token instead. Vehicle spawn: COPY from the same plant type as the rocket factory, target `kosm_vestnik_1`.

### Connections

Footprint **24 × 32 m**. Long axis Z.

| Socket | Approx. |
|---|---|
| Road | `(0, 0, -16)` dir `(0, 0, -17)` |
| Pedestrian | `(12, 0, -6)` |
| Power | `(-12, 0, 0)` |
| Unload | `(6, 0, -12)` |
| Load | `(-6, 0, -12)` |

### 3D

| | |
|---|---|
| Size | 24 × 10 m high × 32 m |
| Budget | 5 000 tris, 1024² |
| Silhouette | Clean-panel hall, **glass-front office** as a dark-window texture strip (not a glass shader), loading dock −Z, rooftop ventilation farm (simple cylinders), slightly cleaner concrete than the rocket hall |
| Nodes | `Main` |
| Particles | `factory_small_white` at vents if any |

### Blender MCP prompt (grey-box)

```text
Metres. Cube Main 24 × 10 × 32 sitting on the ground, material #8A9AA8.
Empties for road/ped/power sockets using game→Blender axis convert.
Export triangulated OBJ Y-up. Save the blend under
blender/assets/buildings/kosm_satellite_factory/
```

---

## 3. Kosmograd Assembly Center (VAB)

| | |
|---|---|
| Folder | `workshop/buildings/kosm_assembly_center/` |
| Display | `$NAME_STR "Kosmograd Assembly Center"` |
| Phase | P1 |
| Role | Consumes stages + Vestnik (preferred) or resources (fallback). Emits `kosm_zarya_k1`. Loads it onto rail if S1 allows. |
| Inspired by | MIK horizontal integration, both gables open |

### Engine

```ini
$NAME_STR "Kosmograd Assembly Center"
$TYPE_PRODUCTION_LINE
$SUBTYPE_AIRPLANE

$WORKERS_NEEDED 85
$PROFESORS_NEEDED 20

$CONSUMPTION_PER_SECOND eletric 0.55

$STORAGE_IMPORT RESOURCE_TRANSPORT_VEHICLES 6
$STORAGE_IMPORT RESOURCE_TRANSPORT_OPEN 40
$STORAGE_IMPORT RESOURCE_TRANSPORT_COVERED 40
$STORAGE_EXPORT RESOURCE_TRANSPORT_VEHICLES 2

$CONNECTION_RAIL
$STATION_NOT_BLOCK
$VEHICLE_UNLOADINGLOADING_MAXVAGONS 2
$LONG_TRAINS
```

Rail coordinates (long axis Z, rails along Z through the hall):

```ini
$CONNECTION_RAIL
0.0 0.0 -23.0
0.0 0.0 -24.0
$CONNECTION_RAIL
0.0 0.0 23.0
0.0 0.0 24.0
```

If allow-pass-through is needed, **COPY** `$CONNECTION_RAIL_ALLOWPASS` pairing from a vanilla through-station. Do not guess extra tokens.

Resource fallback consumption (only if vehicle inputs fail — see ARCHITECTURE.md):

```ini
$CONSUMPTION steel 0.141
$CONSUMPTION aluminium 0.059
$CONSUMPTION mcomponents 0.041
$CONSUMPTION ecomponents 0.016
```

Vehicle output: COPY vanilla **airplane factory** tokens, target `kosm_zarya_k1`.

Road court on +X for trucks that bring stages if rail is through-running.

### Connections

Footprint **34 × 46 m** (same as rocket factory on purpose: one grey-box template, two skins later).

| Socket | Approx. |
|---|---|
| Rail through | Z = ±23 |
| Road trucks | `(17, 0, 0)` |
| Pedestrian | `(17, 0, -10)` |
| Power | `(-17, 0, 10)` |
| Airplane stand inside (if the type needs it) | `$AIRPLANE_STATION_50M` along hall Z — **UNVERIFIED**, only if vanilla airplane plants have one |

### 3D

| | |
|---|---|
| Size | 34 × 18 m high × 46 m (taller than the rocket factory) |
| Budget | 8 000 tris, **2048²** landmark |
| Silhouette | Two arched bays, **rail doors both gables**, red star painted, crane rail as a simple I-beam under the roof, warning stripes on the apron texture, pipe run |
| Nodes | `Main` `Gantry` |
| Interior | Empty volume. Optional very low-poly gantry. No full rocket parked as static mesh (the vehicle is the rocket) |

### Blender MCP prompt (grey-box)

```text
Metres. Cube Main 34 × 18 × 46 on ground, material #8A9AA8.
A second thin cube Gantry 30 × 0.4 × 0.4 at height 16 along Z, parent or join later.
Empties: sock_rail_a, sock_rail_b, sock_road, sock_ped, sock_power.
Export OBJ Y-up triangulated. Save blend in
blender/assets/buildings/kosm_assembly_center/
```

---

## 4. Kosmograd Fuel Refinery

| | |
|---|---|
| Folder | `workshop/buildings/kosm_fuel_refinery/` |
| Display | `$NAME_STR "Kosmograd Fuel Refinery"` |
| Phase | P1 |
| Role | `oil` + `chemicals` → vanilla `fuel` (token **COPY** from vanilla refinery) |
| Inspired by | Small chemical plant + tank farm, not a civilian mega-refinery |

### Engine

```ini
$NAME_STR "Kosmograd Fuel Refinery"
$TYPE_FACTORY

$WORKERS_NEEDED 30
$PROFESORS_NEEDED 4

$CONSUMPTION oil 0.023
$CONSUMPTION chemicals 0.013
$PRODUCTION fuel 0.033
$CONSUMPTION_PER_SECOND eletric 0.18

$STORAGE_IMPORT_SPECIAL RESOURCE_TRANSPORT_OIL 120 oil
$STORAGE_IMPORT_SPECIAL RESOURCE_TRANSPORT_COVERED 60 chemicals
$STORAGE_EXPORT_SPECIAL RESOURCE_TRANSPORT_OIL 120 fuel
$STORAGE_FUEL RESOURCE_TRANSPORT_OIL 200

$CONNECTION_PIPE_INPUT
$CONNECTION_PIPE_OUTPUT

$POLLUTION_MEDIUM
$PARTICLE factory_medium_gray 0 18 0 1 1
```

**COPY** vanilla oil refinery for: exact `$PRODUCTION` resource name, pipe token layout, whether export is `RESOURCE_TRANSPORT_OIL` or another type. The numbers above assume 30 workers and ~1 t fuel / day building total.

If `fuel` cannot be produced, demote this building to `$TYPE_STORAGE` + `$STORAGE_FUEL` and retcon ECONOMY.md.

### Connections

Footprint **18 × 24 m**.

| Socket | Approx. |
|---|---|
| Road | `(0, 0, -12)` |
| Pipe in | `(-9, 2, 0)` |
| Pipe out | `(9, 2, 0)` |
| Power | `(0, 0, 12)` |
| Pedestrian | `(9, 0, -8)` |

### 3D

| | |
|---|---|
| Size | 18 × 14 m high × 24 m |
| Budget | 5 000 tris, 1024² |
| Silhouette | Distillation column (tapered cylinder), 2–3 tanks, pipe rack, small control hut, concrete berm. Soot under vents **in texture** |
| Nodes | `Main` `Tanks` `Stack` |
| Resource viz | Optional `$RESOURCE_VISUALIZATION` on tanks if vanilla does it; skip in grey-box |

### Blender MCP prompt (grey-box)

```text
Metres. Main box 18 × 8 × 24. Cylinder Stack radius 1.2 height 14 at (0,7,6) in Blender.
Material #8A9AA8 halls, #B7B3A8 tanks.
Pipe empties at game (−9,2,0) and (9,2,0) converted.
Export OBJ. Save blender/assets/buildings/kosm_fuel_refinery/
```

---

## 5. Kosmograd Launch Pad

| | |
|---|---|
| Folder | `workshop/buildings/kosm_launch_pad/` |
| Display | `$NAME_STR "Kosmograd Launch Pad"` |
| Phase | P1 |
| Role | Rail unload, fuel, 50 m airplane stand, takeoff, loyalty |
| Inspired by | Gagarin's Start / Baikonur pad 1 *as a type of place*, not a replica |

### Engine

```ini
$NAME_STR "Kosmograd Launch Pad"
$TYPE_CARGO_STATION
$SUBTYPE_AIRPLANE

$WORKERS_NEEDED 15
$PROFESORS_NEEDED 8

$STATION_NOT_BLOCK
$VEHICLE_UNLOADINGLOADING_MAXVAGONS 2

$STORAGE_FUEL RESOURCE_TRANSPORT_OIL 80
$STORAGE_IMPORT RESOURCE_TRANSPORT_VEHICLES 2

$AIRPLANE_STATION_50M 0.0 0.0 -8.0  0.0 0.0 8.0

$MONUMENT_GOVERNMENT_LOYALTY_RADIUS 400
$MONUMENT_GOVERNMENT_LOYALTY_STRENGTH 2.8

$CONSUMPTION_PER_SECOND eletric 0.12
$ELETRIC_WITHOUT_WORKING_FACTOR 0.0
```

Rail along X or Z — pick **Z** to match the VAB's through axis so a straight test track works:

```ini
$CONNECTION_RAIL
0.0 0.0 -17.0
0.0 0.0 -18.0
```

```ini
$CONNECTION_PIPE_INPUT
-13.0 1.5 0.0
-14.0 1.5 0.0

$CONNECTION_AIRROAD
0.0 0.0 17.0
0.0 0.0 18.0

$CONNECTION_ROAD
13.0 0.0 0.0
14.0 0.0 0.0

$CONNECTION_PEDESTRIAN
10.0 0.0 -10.0
11.0 0.0 -10.0

$CONNECTION_ELETRIC_HIGH_INPUT
-10.0 0.0 13.0
-11.0 0.0 13.0
```

`$PARTICLE factory_big_gray` at flame trench **only if** building particles play on this type. Otherwise rely on the airplane's `$PARTICLE_MOVEMENT`.

If monument tokens no-op, keep the pad functional and add `kosm_memorial_plaza`.

If S2 fails (no rail+airplane together), strip `$CONNECTION_RAIL` here and use `kosm_rail_terminus` 80–150 m away.

### Connections / footprint

Footprint **34 × 34 m**. Flame trench as a depressed box in the mesh (visual), pathing still on Y=0.

### 3D

| | |
|---|---|
| Size | 34 × 34 m pad, lightning masts ~40 m high |
| Budget | 8 000 tris, **2048²** |
| Silhouette | Massive concrete slab, **flame trench**, twin lightning masts, **leaning service gantry** that hugs a vertical rocket, blast-off scorch **decal in texture**, bunker/blockhouse in one corner, no NASA-style tower copy |
| Nodes | `Main` `Gantry` `MastA` `MastB` |
| Airplane stand | Must be empty volume in the centre. Do not put a static rocket mesh on the stand |
| Gantry | Offset so a 4 m-diameter vehicle fits. Leave a clearance cylinder r=3.5 m, h=35 m on the stand origin |

### Blender MCP prompt (grey-box)

```text
Metres. Flat box Main 34 × 1 × 34, origin ground centre, top at y=1 in Blender
then sit it on the ground (origin at 0.5 height). Material #B7B3A8.
Cut or boolean a trench 8 × 2 × 20 along Z on the −X side of centre
(grey-box: a second darker box is enough).
Two cylinders MastA MastB r=0.4 h=40 at (±12, 20, ±12) in Blender Z-up.
Gantry: a thin 2 × 30 × 2 box leaning 10° toward centre, not intersecting
the r=3.5 clearance cylinder at world origin.
Empties: sock_rail, sock_pipe, sock_air, sock_road, sock_stand (at origin).
Export OBJ Y-up. Save blender/assets/buildings/kosm_launch_pad/
```

---

# P1 vehicles

## 6. Zarya-K1 (airplane rocket)

| | |
|---|---|
| Folder | `workshop/vehicles/kosm_zarya_k1/` |
| Display | `$NAME_STR "Zarya-K1"` |
| Phase | P1 |
| Role | The launch vehicle. Airplane. Must be loaded until the pad. |
| Inspired by | R-7 / 8K71 cluster, **not a replica** — four strap-ons + core + small blunt payload fairing |

### Engine

```ini
$TYPE VEHICLETYPE_AIRPLANE
$NAME_STR "Zarya-K1"
$COUNTRY 39011
$AVAILABLE 1957 3000
$COST_RUB 1

$MOVEMENT_SPEED 800
$MOVEMENT_POWER_KW 4000
$MOVEMENT_EMPTY_WEIGHT 280

$TAKEOFF_DISTANCE 1

$CARGOVEHICLE_MUSTBE_LOADED

$MOVEMENT_WHEEL_FRONT 0 0.5 0
$MOVEMENT_WHEEL_BACK 0 0.5 0
```

Fuel / tank tokens: **COPY** a vanilla jet `script.ini` entire fuel section, then scale capacity so one pad fill ≈ one launch.

Particles: **COPY** a vanilla jet `$PARTICLE_MOVEMENT` block. Place emitters at the **nozzle plane** (game coords near origin). Do not use `factory_big_gray` here.

Sound: `$SOUND_PARAMS` COPY from a jet, not a propeller plane.

`$PURCHASE_EXCLUDE` — player should not buy Zarya-K1 in the aircraft shop; it is manufactured. If exclude also blocks factory output, **remove it** (P0).

### 3D

| | |
|---|---|
| Height | ~33 m stack |
| Diameter | Core ~2.8 m, strap-ons ~2.6 m, overall ~10 m across fins/nozzles |
| Budget | 10 000 tris, 1024² |
| Origin | Centre of nozzle cluster, **on the ground**. Stack along **+Y game** (vertical) |
| Silhouette | Four boosters around a core, conical/blunt fairing, four-nozzle (or 5) cluster in a plus, pale metal + orange-brown rust streaks, red ID band **painted**, no NASA flags, no Latin "CCCP" if you cannot do Cyrillic cleanly — use a red star |
| Wheels | Dummy small pads at the base so `$MOVEMENT_WHEEL_*` has somewhere to live. Not a landing-gear comedy |
| Cargo viz on wagon | The wagon, not this mesh, rotates the visualization. This mesh stays vertical |

**Authoring orientation:** In Blender Z-up, build the rocket along +Z, nozzles at Z=0, nose toward +Z. Export axis conversion must map that to game +Y. Confirm with a 1 m cube test in ModelViewer before committing the full mesh.

### Blender MCP prompt (grey-box)

```text
Metres, Z-up. Delete cube.
Cylinder core r=1.4 h=28 at (0,0,14).
Four cylinders r=1.3 h=20 at (±2.6,0,10) and (0,±2.6,10).
Cone fairing r=1.4 → 0.3 h=5 sitting on top of core.
Five small cylinders r=0.4 h=1 as nozzles at z=0.5, plus formation.
Join to one object KOSM_veh_zarya_k1_v01.
Origin at world origin (nozzle plane).
Flat material #C9C4B8.
Export OBJ with axis conversion for WR:SR (Y-up). Save blend in
blender/assets/vehicles/kosm_zarya_k1/
```

---

## 7. K-1 stage set (cargo)

| | |
|---|---|
| Folder | `workshop/vehicles/kosm_stage_k1/` |
| Display | `$NAME_STR "Zarya-K1 Stage Set"` |
| Phase | P1 |
| Role | Factory output. Open truck cargo. Input to VAB. |

### Engine

```ini
$TYPE VEHICLETYPE_ROAD
$NAME_STR "Zarya-K1 Stage Set"
$COUNTRY 39011
$AVAILABLE 1957 3000
$COST_RUB 1

$MOVEMENT_SPEED 0
$MOVEMENT_EMPTY_WEIGHT 40

$CARGOVEHICLE_MUSTBE_LOADED
$PURCHASE_EXCLUDE
```

No `$RESOURCE_TRANSPORT_TYPE` — this vehicle **is** cargo, it does not carry cargo.

### 3D

| | |
|---|---|
| Size | Horizontal cluster ~12 m long, ~6 m across, sitting on a cradle |
| Budget | 4 000 tris, 1024² |
| Origin | Ground, centre of cradle |
| Silhouette | Two or three tank cylinders on a steel cradle with lifting eyes. Must read as "booster on a jig" from 50 m |
| Orientation | **Horizontal** (this is freight, not the stacked rocket) |

### Blender MCP prompt (grey-box)

```text
Metres. Three cylinders r=1.2 length 12 along Y, sitting on a 8×0.4×4 box cradle.
Origin ground centre. Material #D4A574.
Export OBJ Y-up. Save blender/assets/vehicles/kosm_stage_k1/
```

---

## 8. Vestnik-1 (cargo)

| | |
|---|---|
| Folder | `workshop/vehicles/kosm_vestnik_1/` |
| Display | `$NAME_STR "Vestnik-1"` |
| Phase | P1 |
| Role | The satellite. Truck cargo. VAB input. Not a flying vehicle. |
| Inspired by | Polished sphere + four rear antennas — **homage, not a 1:1 Sputnik 1** |

### Engine

```ini
$TYPE VEHICLETYPE_ROAD
$NAME_STR "Vestnik-1"
$COUNTRY 39011
$AVAILABLE 1957 3000
$COST_RUB 1

$MOVEMENT_SPEED 0
$MOVEMENT_EMPTY_WEIGHT 2

$CARGOVEHICLE_MUSTBE_LOADED
$PURCHASE_EXCLUDE
```

### 3D

| | |
|---|---|
| Size | Sphere ~0.6 m on a 3 × 1.5 × 2 m transport jig (the jig is what trucks need to "see") |
| Budget | 4 000 tris, 1024² |
| Origin | Ground, jig centre |
| Silhouette | Sphere + four thin antennas swept back, on a wooden/steel crate. Silver + antenna rods. Scale the jig up so it is readable in traffic; the sphere may be oversized vs history (1:1 58 cm vanishes at game camera) — **game-readable ~1.8 m sphere is allowed** |

### Blender MCP prompt (grey-box)

```text
Metres. Box jig 3 × 1.2 × 2 on ground. Sphere r=0.9 sitting in a recess on the jig.
Four thin cubes as antennas. Material sphere #C0C0C8, jig #D4A574.
Origin ground centre. Export OBJ. Save blender/assets/vehicles/kosm_vestnik_1/
```

---

## 9. Transporter-erector (rail wagon)

| | |
|---|---|
| Folder | `workshop/vehicles/kosm_transporter_erector/` |
| Display | `$NAME_STR "Kosmograd Transporter-Erector"` |
| Phase | P1 |
| Role | Carries Zarya-K1 (and nothing else if `$RESOURCE_ALLOW_ONLY` can name a vehicle — UNVERIFIED). Heavy. Long. |

### Engine

```ini
$TYPE VEHICLETYPE_RAIL_VAGON
$TRAINGROUP_VAGON
$NAME_STR "Kosmograd Transporter-Erector"
$COUNTRY 39011
$AVAILABLE 1957 3000
$COST_RUB 1

$MOVEMENT_SPEED 60
$MOVEMENT_EMPTY_WEIGHT 80
$MOVEMENT_POWER_KW 0

$RESOURCE_TRANSPORT_TYPE RESOURCE_TRANSPORT_VEHICLES
$RESOURCE_CAPACITY 300

$CARGOVEHICLE_VISUALIZATION
min -2.5 1.2 -16
max  2.5 5.5  16
```

The visualization block syntax must be **COPY** from a vanilla vehicle-carrying wagon (car-transport rail if any, or a flatcar that hauls vehicles). If none exists, COPY a road heavy trailer that uses `$CARGOVEHICLE_VISUALIZATION` and match field order from the vehicle guide:

```text
$CARGOVEHICLE_VISUALIZATION min x y z max x y z
```

Rotation: if the rocket mesh is vertical, the wagon viz box must **lay it down**. If the token has no rotation field, author a **second horizontal rocket mesh** as `$JOINT` or accept a standing rocket on the flatcar (ugly, still playable). Record the outcome in DECISIONS.md. Preferred: viz box with rotation from the guide's `$RESOURCE_VISUALIZATION rotation` pattern if it applies to vehicles-as-cargo.

`$PURCHASE_EXCLUDE` should **not** be set — the player buys this wagon.

Wheels: model 4–6 axles per side (two bogies visible). Long wheelbase ~28–32 m over buffers.

### 3D

| | |
|---|---|
| Length over buffers | ~32 m |
| Deck height | ~1.2 m |
| Budget | 6 000 tris, 1024² |
| Origin | Ground (rail height — **COPY** vanilla wagon origin, often at railhead) |
| Silhouette | Heavy flatcar, side beams, many wheels, side stakes or a shallow cradle that reads as "this carries something huge", muted red-brown deck, grey beams |
| Cargo | Do not model the rocket into the wagon mesh |

### Blender MCP prompt (grey-box)

```text
Metres. Deck box 3.2 × 1.0 × 30, origin at rail height (COPY vanilla: start with
origin at world origin, deck top at z=1.2 in Blender).
Eight small cylinders as wheels.
Material #5C6570.
Export OBJ with the same axis conversion as a vanilla wagon test.
Save blender/assets/vehicles/kosm_transporter_erector/
```

---

# P3 sheets (do not model in P1)

Short contracts so the catalog already knows what "done" means. Full token blocks are written when P3 starts, copied from the nearest P1 analogue.

| Folder | Type | Size m | Tris | Silhouette |
|---|---|---|---|---|
| `kosm_memorial_plaza` | `$TYPE_MONUMENT` | 14 × 14 | 2 500 | Obelisk + star, trespass enabled |
| `kosm_rail_terminus` | `$TYPE_CARGO_STATION` | 30 × 14 | 2 500 | Two-track loader, vehicle cargo only |
| `kosm_mission_control` | `$TYPE_UNIVERSITY` `$SUBTYPE_TECHNICAL` or factory with professors | 20 × 28 | 4 000 | Low block, two rooftop dishes, lit window band |
| `kosm_tracking_station` | attraction or factory | 24 × 24 | 5 000 | Six dishes on plinths, dishes **static** |
| `kosm_propellant_storage` | `$TYPE_STORAGE` + `$STORAGE_FUEL` | 16 × 22 | 2 500 | Tank cluster + berm |
| `kosm_research_bureau` | `$TYPE_UNIVERSITY` `$SUBTYPE_TECHNICAL` | 20 × 24 | 4 000 | Institute block |
| `kosm_museum` | `$TYPE_ATTRACTION` + museum tokens | 22 × 26 | 4 000 | Hall + rocket sculpture (static) |
| `kosm_training_center` | factory / sport hybrid COPY | 20 × 26 | 4 000 | Gym + cylinder + pool block |
| `kosm_quarters` | `$TYPE_LIVING` | 18 × 30 | 4 000 | Panel housing, slightly nicer |
| `kosm_recovery_depot` | cargo station | 22 × 30 | 5 000 | Hangar + pad for Chaika |
| `kosm_launch_heavy` | cargo airport | 34 × 34 | 8 000 | Bigger trench, 50 m stand |
| `kosm_stacking_hall` | production line airplane | 24 × 40 | 6 000 | Tall slab doors |
| `kosm_gate` | monument / decorative COPY | 28 × 8 | 2 500 | Checkpoint + fence pieces |
| `kosm_zarya_k2` | airplane | medium | 10 000 | Longer K1 |
| `kosm_bogatyr` | airplane | heavy | 10 000 | Five-engine cluster, parallel boosters, conical fairing; N1-inspired **without copying** |
| `kosm_sfera` / `vektor` / `chaika` | cargo vehicles | — | 4 000 | Family with Vestnik |

`kosm_avionics_line` is **not scheduled**. If a themed electronics hall is wanted, it still outputs vanilla `ecomponents`.

---

## Checklist before an asset is "done"

1. Grey-box footprint matches this file ± 0.1 m.
2. Export OBJ triangulated, transforms applied, origin correct in ModelViewer.
3. `.nmf` + `.mtl` + dds in the workshop folder.
4. `building.ini` / `script.ini` started from vanilla of the same type.
5. All sockets listed here exist and a test vehicle can use them.
6. `imagegui.png` 96×96 (buildings).
7. Tris / texture under budget.
8. No banned names on the mesh.
9. Changelog line.
10. Screenshot dropped in the test-save note (not required in git).
