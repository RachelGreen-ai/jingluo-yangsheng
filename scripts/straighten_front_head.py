#!/usr/bin/env python3
"""Straighten the atlas head with a small vertical shear, without redrawing it."""

import argparse
from pathlib import Path

import numpy as np
from PIL import Image


def smoothstep(edge0: float, edge1: float, value: np.ndarray) -> np.ndarray:
    t = np.clip((value - edge0) / (edge1 - edge0), 0, 1)
    return t * t * (3 - 2 * t)


def head_shift(rows: np.ndarray) -> np.ndarray:
    return np.where(
        rows <= 70,
        4.0,
        np.where(
            rows < 210,
            4.0 - 2.5 * smoothstep(70, 210, rows),
            np.where(rows < 250, 1.5 * (1 - smoothstep(210, 250, rows)), 0.0),
        ),
    )


def straighten(source: Image.Image) -> Image.Image:
    image = np.asarray(source.convert("RGB"), dtype=np.float32)
    height, width = image.shape[:2]
    rows, cols = np.mgrid[:height, :width].astype(np.float32)
    source_x = np.clip(cols - head_shift(rows), 0, width - 1)
    x0 = np.floor(source_x).astype(np.int32)
    x1 = np.minimum(x0 + 1, width - 1)
    fraction = source_x - x0
    row_index = np.arange(height)[:, None]
    corrected = (
        image[row_index, x0] * (1 - fraction)[..., None]
        + image[row_index, x1] * fraction[..., None]
    )
    return Image.fromarray(np.clip(corrected, 0, 255).astype(np.uint8), "RGB")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    source = Image.open(args.input).convert("RGB")
    if source.size != (820, 1230):
        raise SystemExit(f"unexpected front image size: {source.size}")
    straighten(source).save(args.output, quality=96, subsampling=0)


if __name__ == "__main__":
    main()
