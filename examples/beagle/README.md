# Beagle demonstration — trifun

## Input provenance

This is an **AI-generated beagle example**, not a real animal photograph, customer
photo, testimonial, or completed embroidery project. It was generated for trifun
on 2026-09-22 with the built-in image generation tool. The recorded request used a
text prompt only; it supplied no referenced photograph or reference-image count.
The prompt requested one generic front-facing adult beagle with transparent
background, complete body, natural fur and a visible tongue, without accessories,
text, logos, or watermarks.

The retained original output and its first project copy have identical SHA256:
`aa699c3b21e8dbe9c5f05b3d71548486ba5d445dca423c7cb136dc080ebac333`.
The original alpha bounds were cropped, scaled to 1080 pixels high with Lanczos,
and centered on a transparent 900 x 1200 canvas. That reconstruction is pixel
identical to the retained project source.

For this head example, we cropped that canvas to `(198, 0, 702, 624)`, composited
the existing alpha onto white, and saved JPEG at quality 95 with no embedded EXIF.
Both tools received exactly the included `input.jpg`:
`f2d36162595854df1ec59e391ff15ac6ef3c9a48f82a486d70a003017cc7efca`.
No generated chart was hand edited.

## Asset permissions

The input and generated images/JSON in this directory are offered by trifun under
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/), to the extent trifun
holds rights in them. This is an asset-specific permission; the CLI code remains
MIT. No exclusive copyright in AI output, third-party rights clearance guarantee,
or provider endorsement is claimed.

The generation service's [output ownership terms](https://openai.com/policies/terms-of-use/#content)
assign its interest in output to the user to the extent permitted by law.
[Sharing guidance](https://openai.com/policies/sharing-publication-policy/)
calls for review and clear AI disclosure. This example is attributed to trifun
and labeled AI-generated beside the README image.

## Actual output and reproduction

Run from the repository root after the documented installation:

```sh
.venv/bin/trifun-stitch convert examples/beagle/input.jpg \
  --size 80 --colors 16 --output beagle-pattern
```

Expected CLI: 80 x 99 grid, 7,920 visible stitches, 16 RGB reference colors, no
manufacturer palette. White background cells are stitched. Output directory must
not already exist. `cli-pattern.json` records the actual generated grid/legend.

`website-balanced.png` was freshly generated with the local website engine on
2026-10-16, using the exact same JPEG and background removal: 3,152 stitches and
12 DMC colors. It is a preview asset only; no website source, DMC database, model
weights, paid pattern package, or API access is included. The local website-engine
workflow cannot be reproduced with this CLI alone. Use the hosted website to try
your own image and inspect its free previews before paying for downloads.

The CLI and website use different palettes, grids, and background handling. This
is a worked workflow example, not an equal-settings quality benchmark. All images
are digital previews, not stitched samples.
