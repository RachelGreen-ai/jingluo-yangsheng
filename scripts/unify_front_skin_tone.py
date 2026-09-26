#!/usr/bin/env python3
"""Unify the figure's skin chroma while preserving lighting and geometry."""

import argparse
from pathlib import Path

import numpy as np
from PIL import Image


def unify(source: Image.Image) -> Image.Image:
    image = np.asarray(source.convert("RGB"), dtype=np.float32)
    red, green, blue = [image[:, :, channel] for channel in range(3)]
    skin = (
        (red > 125)
        & (red > green * 1.02)
        & (green > blue * 1.02)
        & (red < 252)
    )

    luminance = 0.299 * red + 0.587 * green + 0.114 * blue
    red_chroma = red - luminance
    blue_chroma = blue - luminance
    blend = 0.40
    target_red_chroma = 26.0
    target_blue_chroma = -25.0
    red_chroma = red_chroma * (1 - blend) + target_red_chroma * blend
    blue_chroma = blue_chroma * (1 - blend) + target_blue_chroma * blend
    corrected = [
        luminance + red_chroma,
        (luminance - 0.299 * (luminance + red_chroma) - 0.114 * (luminance + blue_chroma)) / 0.587,
        luminance + blue_chroma,
    ]
    for channel, values in enumerate(corrected):
        image[:, :, channel][skin] = values[skin]
    return Image.fromarray(np.clip(image, 0, 255).astype(np.uint8), "RGB")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    source = Image.open(args.input).convert("RGB")
    if source.size != (820, 1230):
        raise SystemExit(f"unexpected front image size: {source.size}")
    unify(source).save(args.output, quality=96, subsampling=0)


if __name__ == "__main__":
    main()
