#!/usr/bin/env python3
"""Balance the atlas figure's face and neck color without changing its geometry."""

import argparse
from pathlib import Path

import numpy as np
from PIL import Image


def smoothstep(edge0: float, edge1: float, value: np.ndarray) -> np.ndarray:
    t = np.clip((value - edge0) / (edge1 - edge0), 0, 1)
    return t * t * (3 - 2 * t)


def correct_color(source: Image.Image) -> Image.Image:
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
    # Keep the correction strongest over the face and neck, fading into the chest.
    alpha = smoothstep(40, 90, cols - 300) * smoothstep(40, 90, 520 - cols)
    alpha *= 1 - smoothstep(205, 315, rows)
    alpha *= skin

    luminance = 0.299 * red + 0.587 * green + 0.114 * blue
    saturation_scale = 0.82
    for channel in range(3):
        image[:, :, channel] += (
            luminance - image[:, :, channel]
        ) * (1 - saturation_scale) * alpha

    image[:, :, 0] += 3.0 * alpha
    image[:, :, 1] += 2.55 * alpha
    image[:, :, 2] += 2.1 * alpha
    image[:, :, 0] += 0.5 * alpha
    image[:, :, 2] -= 0.5 * alpha
    return Image.fromarray(np.clip(image, 0, 255).astype(np.uint8), "RGB")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    source = Image.open(args.input).convert("RGB")
    if source.size != (820, 1230):
        raise SystemExit(f"unexpected front image size: {source.size}")
    correct_color(source).save(args.output, quality=96, subsampling=0)


if __name__ == "__main__":
    main()
