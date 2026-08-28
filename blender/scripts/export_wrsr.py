"""WR:SR OBJ export helper for Kosmograd.

Run inside Blender (Scripting workspace or blender --background --python):

    blender kosm_launch_pad.blend --background --python export_wrsr.py -- --out export/model.obj

Does not create .nmf. ModelViewer is a separate step.

Axis: Blender Z-up → OBJ Y-up, forward -Z. If P0 cube test fails, change
axis_forward / axis_up once and document in docs/BLENDER.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

import bpy


def _argv_after_double_dash() -> list[str]:
    if "--" in sys.argv:
        return sys.argv[sys.argv.index("--") + 1 :]
    return []


def triangulate_and_merge() -> None:
    for obj in bpy.context.scene.objects:
        if obj.type != "MESH":
            continue
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.quads_convert_to_tris(quad_method="BEAUTY", ngon_method="BEAUTY")
        bpy.ops.mesh.remove_doubles(threshold=0.0001)
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        obj.select_set(False)


def export_obj(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.obj_export(
        filepath=str(path),
        export_selected_objects=False,
        export_triangulated_mesh=True,
        export_normals=True,
        export_uv=True,
        export_materials=False,
        forward_axis="NEGATIVE_Z",
        up_axis="Y",
        apply_modifiers=True,
    )


def main() -> None:
    args = _argv_after_double_dash()
    out = Path("export/model.obj")
    if "--out" in args:
        out = Path(args[args.index("--out") + 1])
    triangulate_and_merge()
    export_obj(out)
    print(f"exported {out.resolve()}")


if __name__ == "__main__":
    main()
