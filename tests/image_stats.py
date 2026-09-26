"""L* statistics and paper-white percentage of an image.

Usage:
    python tests\\image_stats.py path\\to\\image.jpg [--l-min 90] [--chroma-max 10]

A pixel counts as paper white when L* >= --l-min and C*ab <= --chroma-max.
Both thresholds are provisional and meant to be tuned.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from skimage.color import rgb2lab


def image_stats(path, l_min, chroma_max):
    # Pillow loads RGB (not BGR); rgb2lab linearizes sRGB and uses D65
    rgb = np.asarray(Image.open(path).convert("RGB"), dtype=np.float64) / 255.0
    lab = rgb2lab(rgb, illuminant="D65")
    L, a, b = lab[..., 0], lab[..., 1], lab[..., 2]
    chroma = np.hypot(a, b)
    paper = (L >= l_min) & (chroma <= chroma_max)
    p = np.percentile(L, [0, 5, 50, 95, 100])
    return {
        "width_px": rgb.shape[1],
        "height_px": rgb.shape[0],
        "L_min": p[0],
        "L_p05": p[1],
        "L_median": p[2],
        "L_p95": p[3],
        "L_max": p[4],
        "L_mean": L.mean(),
        "L_range_p05_p95": p[3] - p[1],
        "paper_white_pct": 100.0 * paper.mean(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("image", type=Path, help="path to the image")
    parser.add_argument("--l-min", type=float, default=90.0,
                        help="minimum L* for paper white (default 90)")
    parser.add_argument("--chroma-max", type=float, default=10.0,
                        help="maximum chroma C*ab for paper white (default 10)")
    args = parser.parse_args()

    if not args.image.is_file():
        sys.exit(f"File not found: {args.image}")

    stats = image_stats(args.image, args.l_min, args.chroma_max)
    print(f"image: {args.image}")
    for key, value in stats.items():
        print(f"  {key}: {value:.2f}" if isinstance(value, float) else f"  {key}: {value}")


if __name__ == "__main__":
    main()
