#!/usr/bin/env python3
"""Clean the front atlas image without changing its canvas or body geometry."""

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def subject_mask(source: Image.Image) -> Image.Image:
    """Turn the generated portrait's white studio background into a soft mask."""
    rgb = np.asarray(source.convert("RGB"), dtype=np.int16)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    mask = ((rgb.min(axis=2) < 245) | (chroma > 6)).astype(np.uint8) * 255
    return Image.fromarray(mask, "L").filter(ImageFilter.MinFilter(7)).filter(ImageFilter.GaussianBlur(0.45))


def paste_clean_head(base: Image.Image, portrait: Image.Image, body_reference: Image.Image | None = None) -> Image.Image:
    source = portrait.convert("RGB")
    source_mask = subject_mask(source)
    source_rgb = np.asarray(source)
    source_mask_np = np.asarray(source_mask)
    ys, xs = np.where(source_mask_np > 40)
    sx0, sy0, sx1, sy1 = xs.min(), ys.min(), xs.max(), ys.max()

    target_subject_width = 148
    scale = target_subject_width / (sx1 - sx0)
    target_size = (round(source.width * scale), round(source.height * scale))
    resized = source.resize(target_size, Image.Resampling.LANCZOS)
    resized_mask = source_mask.resize(target_size, Image.Resampling.LANCZOS)

    # Align the same clean portrait to the existing head position.
    target_left = 333 - round(sx0 * scale)
    target_top = 40 - round(sy0 * scale)

    cleaned = base.copy()
    if body_reference is not None:
        # Restore the unchanged neck/shoulders below the face before compositing.
        cleaned.paste(body_reference.crop((0, 198, base.width, 310)), (0, 198))
    white = Image.new("RGB", cleaned.size, "white")
    cleanup = Image.new("L", cleaned.size, 0)
    ImageDraw.Draw(cleanup).rectangle((318, 28, 500, 180), fill=255)
    cleaned = Image.composite(white, cleaned, cleanup)

    layer = Image.new("RGB", cleaned.size, "white")
    layer_mask = Image.new("L", cleaned.size, 0)
    layer.paste(resized, (target_left, target_top))
    layer_mask.paste(resized_mask, (target_left, target_top))
    return Image.composite(layer, cleaned, layer_mask)


def remove_leg_hair(image: Image.Image) -> Image.Image:
    rgb = np.asarray(image.convert("RGB"), dtype=np.uint8)
    gray = np.asarray(image.convert("L"), dtype=np.float32)
    local = np.asarray(image.convert("L").filter(ImageFilter.GaussianBlur(3.0)), dtype=np.float32)

    body = (rgb.min(axis=2) < 246).astype(np.uint8) * 255
    body = np.asarray(Image.fromarray(body, "L").filter(ImageFilter.MinFilter(7))) > 0
    leg_roi = np.zeros(body.shape, dtype=bool)
    leg_roi[680:1125, 285:410] = True
    leg_roi[680:1125, 420:545] = True

    # Hair is narrow, dark, and locally darker than the surrounding skin.
    hair = body & leg_roi & (gray < 222) & ((local - gray) > 2.5)
    hair_mask = Image.fromarray((hair.astype(np.uint8) * 255), "L")
    hair_mask = hair_mask.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(0.8))

    # A small median neighborhood removes the dark strands while retaining knees and edges.
    replacement = image.convert("RGB").filter(ImageFilter.MedianFilter(9))
    return Image.composite(replacement, image.convert("RGB"), hair_mask)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--front", type=Path, required=True)
    parser.add_argument("--portrait", type=Path, required=True)
    parser.add_argument("--body-reference", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    base = Image.open(args.front).convert("RGB")
    portrait = Image.open(args.portrait).convert("RGB")
    if base.size != (820, 1230):
        raise SystemExit(f"unexpected front image size: {base.size}")
    body_reference = Image.open(args.body_reference).convert("RGB") if args.body_reference else None
    result = paste_clean_head(base, portrait, body_reference)
    result = remove_leg_hair(result)
    result.save(args.out, quality=96, subsampling=0)


if __name__ == "__main__":
    main()
