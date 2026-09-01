#!/usr/bin/env python3
"""Build P0 Blender sources plus flat preview/texture assets."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[2]
P0 = ROOT / "experiments" / "p0"
ASSETS = P0 / "assets"
BLENDER_SCRIPT = P0 / "build_fixtures.py"

COLORS = {
    "p0_pipeline_shed": "#8A9AA8",
    "p0_factory": "#8A9AA8",
    "p0_pad": "#B7B3A8",
    "p0_transfer": "#8A9AA8",
    "p0_airplane_parking": "#B7B3A8",
    "p0_rocket": "#C9C4B8",
    "p0_wagon": "#5C6570",
    "p0_road_carrier": "#5C6570",
}


def build_images() -> None:
    magick = shutil.which("magick")
    if not magick:
        raise RuntimeError("ImageMagick 'magick' is required to encode DXT1 DDS")
    for object_id, color in COLORS.items():
        target = ASSETS / object_id
        target.mkdir(parents=True, exist_ok=True)
        diffuse_png = target / "diffuse.png"
        image = Image.new("RGB", (256, 256), color)
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, 255, 16), fill="#A02C2C")
        draw.polygon(((128, 36), (116, 58), (140, 58)), fill="#202428")
        image.save(diffuse_png)
        subprocess.run(
            [magick, str(diffuse_png), "-define", "dds:compression=dxt1", str(target / "diffuse.dds")],
            check=True,
        )
        if (target / "building.ini").is_file():
            icon = Image.new("RGB", (96, 96), "#D6D2C8")
            icon_draw = ImageDraw.Draw(icon)
            icon_draw.rectangle((18, 38, 78, 76), fill=color, outline="#202428", width=3)
            icon_draw.polygon(((18, 38), (48, 16), (78, 38)), fill="#5C6570", outline="#202428")
            icon.save(target / "imagegui.png")


def main() -> int:
    blender_env = os.environ.copy()
    blender_env.setdefault("ALSOFT_DRIVERS", "null")
    subprocess.run(
        ["blender", "--factory-startup", "--background", "--python", str(BLENDER_SCRIPT)],
        cwd=ROOT,
        env=blender_env,
        check=True,
    )
    build_images()
    print("P0 source geometry and flat image assets generated.")
    print("ModelViewer conversion is still required for model.nmf/main.nmf and material.mtl.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
