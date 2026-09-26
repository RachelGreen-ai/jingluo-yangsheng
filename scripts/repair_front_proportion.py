#!/usr/bin/env python3
"""Repair the atlas figure's head/neck proportion without redrawing the person."""

import argparse
from pathlib import Path

import numpy as np
from PIL import Image


def remap_front(source: Image.Image) -> Image.Image:
    """Move and slightly narrow the head while extending the neck transition."""
    image = np.asarray(source.convert("RGB"), dtype=np.float32)
    height, width = image.shape[:2]
    center_x = width / 2
    rows, cols = np.mgrid[:height, :width].astype(np.float32)
    source_y = np.empty_like(rows)
    source_x = np.empty_like(cols)

    for row in range(height):
        if row <= 210:
            mapped_y = row + 8
            horizontal_scale = 0.94
        elif row < 250:
            t = (row - 210) / 40
            mapped_y = 218 + (row - 210) * 32 / 40
            horizontal_scale = 0.94 + 0.06 * t
        else:
            mapped_y = row
            horizontal_scale = 1.0
        source_y[row] = mapped_y
        source_x[row] = center_x + (cols[row] - center_x) / horizontal_scale

    source_y = np.clip(source_y, 0, height - 1)
    source_x = np.clip(source_x, 0, width - 1)
    x0 = np.floor(source_x).astype(np.int32)
    y0 = np.floor(source_y).astype(np.int32)
    x1 = np.minimum(x0 + 1, width - 1)
    y1 = np.minimum(y0 + 1, height - 1)
    fx = source_x - x0
    fy = source_y - y0

    remapped = (
        image[y0, x0] * (1 - fx)[..., None] * (1 - fy)[..., None]
        + image[y0, x1] * fx[..., None] * (1 - fy)[..., None]
        + image[y1, x0] * (1 - fx)[..., None] * fy[..., None]
        + image[y1, x1] * fx[..., None] * fy[..., None]
    )

    # Warm the face slightly so it sits in the same skin-color range as the neck.
    skin = (
        (rows < 210)
        & (remapped[:, :, 0] > 130)
        & (remapped[:, :, 0] > remapped[:, :, 1] * 1.03)
        & (remapped[:, :, 1] > remapped[:, :, 2] * 1.03)
        & (remapped[:, :, 0] < 248)
    )
    remapped[skin] = np.clip(remapped[skin] + np.array([1, -4, -7]), 0, 255)
    return Image.fromarray(remapped.astype(np.uint8), "RGB")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    source = Image.open(args.input).convert("RGB")
    if source.size != (820, 1230):
        raise SystemExit(f"unexpected front image size: {source.size}")
    remap_front(source).save(args.output, quality=96, subsampling=0)


if __name__ == "__main__":
    main()
