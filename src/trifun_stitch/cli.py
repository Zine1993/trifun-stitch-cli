"""Explicit local-only command line interface."""

import argparse
import sys
from pathlib import Path

from . import __version__
from .core import convert
from .export import export


def main(argv=None):
    parser = argparse.ArgumentParser(prog="trifun-stitch", description="Offline basic cross-stitch conversion by trifun. No account, model, or API key.")
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)
    cmd = commands.add_parser("convert", help="Convert one local image to PNG, JSON and PDF")
    cmd.add_argument("image", type=Path)
    cmd.add_argument("--output", "-o", type=Path, required=True, help="New output directory; existing directories are refused")
    cmd.add_argument("--size", type=int, default=40, help="Width in stitches (1-300)")
    cmd.add_argument("--colors", type=int, default=8, help="Maximum colors (1-62)")
    cmd.add_argument("--fabric", type=int, default=14, help="Fabric count (6-40)")
    cmd.add_argument("--palette", type=Path, help="Your licensed JSON thread palette; otherwise RGB reference only")
    cmd.add_argument("--title", default="Cross-stitch pattern")
    args = parser.parse_args(argv)
    try:
        if args.output.exists():
            raise ValueError("Output directory already exists; choose a new directory.")
        result = convert(args.image, args.size, args.colors, args.fabric, args.palette, args.title)
        export(result, args.output)
    except (ValueError, OSError, KeyError, TypeError, Warning) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print(f'Created {result["width"]} x {result["height"]} chart: {result["total_stitches"]} stitches, {len(result["legend"])} colors.')
    print(f'Palette: {result["brand"]}. Output: {args.output}')
    return 0
