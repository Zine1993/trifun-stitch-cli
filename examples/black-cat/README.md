# Real black cat photo example

Photo: [Black cat in the wild.jpg](https://commons.wikimedia.org/wiki/File:Black_cat_in_the_wild.jpg)
by **IrazuLibertad**, dedicated under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).
The author describes the cat as Xavier Alejandro. License checked on 2026-10-16.

The project's previously downloaded 960 × 1,280 image was cropped once at pixel
coordinates `(left=160, top=700, right=600, bottom=1280)`, producing **440 × 580** pixels.
The crop is exported as `source.jpg` with source EXIF/GPS metadata removed. No retouching
or AI image generation was used. Original downloaded-file SHA256:
`a3848bf71603ec8b76cdac4ec215b8afa732ce07bc38d513b722a7ac4764ea38`.

Both workflows use the **same byte-identical `source.jpg`**. The website uses
`background_mode=preserve`; neither example claims automatic background removal.

## Reproduce the basic CLI output

From the repository root after installation:

```sh
.venv/bin/trifun-stitch convert examples/black-cat/source.jpg \
  --size 80 --colors 16 --title "Black cat - basic CLI" \
  --output black-cat-pattern
```

Expected: **80 × 105 cells, 8,400 stitches, 16 RGB reference colors**.
`cli-preview.png` and `cli-pattern.json` are copied from that actual CLI run.
The RGB output is not a manufacturer thread shopping list.

## Website output

`website-easy.png`, `website-balanced.png`, and `website-detailed.png` are the
previews returned by the production PetCrossStitch `/api/mvp/options` endpoint on
2026-10-16. The run used a new anonymous internal QA session, created no order,
performed no payment, and did not contribute browser analytics events.
Only this QA session's generated temporary patterns were deleted after checking.

| Tier | Stitches | DMC colors | Stitched size at 14-count |
| --- | ---: | ---: | --- |
| Easy | 6,767 | 12 | 13.1 × 17.1 cm |
| Balanced | 16,461 | 25 | 20.3 × 26.7 cm |
| Detailed | 29,203 | 33 | 27.2 × 35.7 cm |

These are digital previews, not finished embroidery. Both tools receive the same
input, but their output sizes, palettes and color budgets differ. This example
does not establish a controlled quality comparison or a success rate. Dark facial
features can disappear at low detail. The higher-detail website preview requires
more stitches and colors; it is not a promise of better results for every photo.

The website processing modules and manufacturer palette data are not distributed
in this repository; rerunning the website requires using the hosted service.

## Files and license

`metrics.json` records the input hash, crop coordinates, command settings and
measured results. No private session cookies, pattern identifiers, credentials,
customer photos or website source code are included.

The source photo remains CC0. Generated image previews and example JSON in this
folder are also offered under CC0 by trifun to the extent trifun holds rights in
them. This does not change the MIT license for CLI source code or the separate
licenses of its dependencies. DMC is a third-party trademark; no endorsement is implied.
