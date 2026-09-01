"""Generate the disposable Blender/OBJ geometry used by P0 experiments.

Run with Blender, not system Python:

    blender --factory-startup --background --python experiments/p0/build_fixtures.py
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import bpy


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "experiments" / "p0" / "generated"


@dataclass(frozen=True)
class Fixture:
    object_id: str
    kind: str
    dimensions: tuple[float, float, float]
    color: tuple[float, float, float, float]


FIXTURES = (
    Fixture("p0_pipeline_shed", "building", (4.0, 6.0, 3.0), (0.54, 0.60, 0.66, 1.0)),
    Fixture("p0_factory", "building", (34.0, 46.0, 18.0), (0.54, 0.60, 0.66, 1.0)),
    Fixture("p0_pad", "building", (34.0, 34.0, 1.0), (0.72, 0.70, 0.66, 1.0)),
    Fixture("p0_transfer", "building", (30.0, 14.0, 4.0), (0.54, 0.60, 0.66, 1.0)),
    Fixture("p0_airplane_parking", "building", (50.0, 50.0, 0.25), (0.72, 0.70, 0.66, 1.0)),
    Fixture("p0_rocket", "vehicle", (2.0, 2.0, 10.0), (0.79, 0.77, 0.72, 1.0)),
    Fixture("p0_wagon", "vehicle", (3.2, 30.0, 1.2), (0.36, 0.40, 0.44, 1.0)),
    Fixture("p0_road_carrier", "vehicle", (3.0, 8.0, 2.0), (0.36, 0.40, 0.44, 1.0)),
)


def clear_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.materials):
        for datablock in list(datablocks):
            if datablock.users == 0:
                datablocks.remove(datablock)


def material(name: str, color: tuple[float, float, float, float]) -> bpy.types.Material:
    result = bpy.data.materials.new(name)
    result.diffuse_color = color
    return result


def cube(name: str, size: tuple[float, float, float], location: tuple[float, float, float]) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return obj


def build(fixture: Fixture) -> bpy.types.Object:
    width, length, height = fixture.dimensions
    pieces: list[bpy.types.Object] = []
    if fixture.object_id == "p0_rocket":
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=width / 2, depth=height, location=(0, 0, height / 2))
        pieces.append(bpy.context.object)
        bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=width / 2, radius2=0.0, depth=2.0, location=(0, 0, height + 1.0))
        pieces.append(bpy.context.object)
    else:
        pieces.append(cube("body", (width, length, height), (0, 0, height / 2)))

    if fixture.object_id == "p0_pipeline_shed":
        # With the pinned OBJ conversion Blender -Y becomes game +Z.
        # Keep both markers inside the exact 4 x 6 x 3 m envelope.
        pieces.append(cube("door_game_plus_z", (1.5, 0.05, 2.2), (0.0, -length / 2 + 0.025, 1.1)))
        pieces.append(cube("roof_marker_game_plus_z", (0.35, 1.2, 0.04), (0.0, -0.8, height - 0.02)))
    elif fixture.kind == "building" and fixture.object_id != "p0_airplane_parking":
        pieces.append(cube("axis_marker_plus_z", (max(1.0, width * 0.08), 1.0, 0.4), (0.0, length * 0.25, height + 0.2)))
    elif fixture.object_id == "p0_wagon":
        pieces.append(cube("front_marker", (1.0, 1.0, 0.5), (0.0, length * 0.35, height + 0.25)))
    elif fixture.object_id == "p0_road_carrier":
        pieces.append(cube("cab", (width, 2.0, 1.0), (0.0, length * 0.3, height + 0.5)))

    flat = material(f"MAT_{fixture.object_id}", fixture.color)
    for piece in pieces:
        piece.data.materials.append(flat)
        piece.select_set(True)
    bpy.context.view_layer.objects.active = pieces[0]
    bpy.ops.object.join()
    root = bpy.context.object
    root.name = "Main" if fixture.kind == "building" else f"KOSM_{fixture.object_id}_v01"

    bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.quads_convert_to_tris(quad_method="BEAUTY", ngon_method="BEAUTY")
    bpy.ops.mesh.remove_doubles(threshold=0.0001)
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode="OBJECT")
    return root


def save_and_export(fixture: Fixture, root: bpy.types.Object) -> None:
    target = OUTPUT / fixture.object_id
    target.mkdir(parents=True, exist_ok=True)
    blend_path = target / f"{fixture.object_id}.blend"
    obj_name = "model.obj" if fixture.kind == "building" else "main.obj"
    obj_path = target / obj_name

    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
    bpy.ops.object.select_all(action="DESELECT")
    root.select_set(True)
    bpy.context.view_layer.objects.active = root
    bpy.ops.wm.obj_export(
        filepath=str(obj_path),
        export_selected_objects=True,
        export_triangulated_mesh=True,
        export_normals=True,
        export_uv=True,
        export_materials=False,
        forward_axis="NEGATIVE_Z",
        up_axis="Y",
        apply_modifiers=True,
    )
    print(f"generated {fixture.object_id}: {blend_path} -> {obj_path}")


def main() -> None:
    for fixture in FIXTURES:
        clear_scene()
        root = build(fixture)
        save_and_export(fixture, root)


if __name__ == "__main__":
    main()
