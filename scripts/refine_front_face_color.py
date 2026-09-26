#!/usr/bin/env python3
"""Refine face brightness so the portrait and atlas body share one light source."""

import argparse
from pathlib import Path

import numpy as np
from PIL import Image


def smoothstep(edge0: float, edge1: float, value: np.ndarray) -> np.ndarray:
    t = np.clip((value - edge0) / (edge1 - edge0), 0, 1)
    return t * t * (3 - 2 * t)


def refine(source: Image.Image) -> Image.Image:
    image = np.asarray(source.convert("RGB"), dtype=np.float32)
    height, width = image.shape[:2]
    rows, cols = np.mgrid[:height, :width].astype(np.float32)
    red, green, blue = [image[:, :, channel] for channel in range(3)]
    skin = (
        (red > 125)
        & (red > green * 1.02)
        & (green > blue * 1.02)
        & (red < 252)
    )

    face = (
        smoothstep(335, 360, cols)
        * smoothstep(470, 445, cols)
        * (1 - smoothstep(188, 235, rows))
        * skin
    )
    neck = (
        smoothstep(340, 365, cols)
        * smoothstep(475, 450, cols)
        * smoothstep(185, 285, rows)
        * (1 - smoothstep(265, 315, rows))
        * skin
    )

    luminance = 0.299 * red + 0.587 * green + 0.114 * blue
    for channel in range(3):
        image[:, :, channel] += (luminance - image[:, :, channel]) * 0.16 * face
        image[:, :, channel] += (luminance - image[:, :, channel]) * 0.08 * neck

    image[:, :, 0] += 6.0 * face + 1.0 * neck
    image[:, :, 1] += 5.76 * face + 0.95 * neck
    image[:, :, 2] += 5.58 * face + 0.9 * neck
    return Image.fromarray(np.clip(image, 0, 255).astype(np.uint8), "RGB")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    source = Image.open(args.input).convert("RGB")
    if source.size != (820, 1230):
        raise SystemExit(f"unexpected front image size: {source.size}")
    refine(source).save(args.output, quality=96, subsampling=0)


if __name__ == "__main__":
    main()
