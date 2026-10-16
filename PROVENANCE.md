# Source and scope

Prepared 2026-10-16 for local review. Public-facing author/brand: **trifun**.

## Project context

PetCrossStitch originated from [tomekhotdog/XStitchLab](https://github.com/tomekhotdog/XStitchLab).
The retained history bundle identifies upstream baseline
`c3d9c3f5252084dfd541f5eef72bad0607829f5a`. The public main branch and its README
were verified at that exact commit on 2026-10-16. README declares MIT; that tree
has no LICENSE file. `licenses/XStitchLab-PROVENANCE.txt` records the actual
source declaration and permanent link. The private fork's later 2024 copyright
line is not treated as an authenticated upstream notice. No upstream license
is issued or changed by this candidate.

## Candidate file origins

- `src/trifun_stitch/*`: newly assembled generic CLI implementation for this candidate.
  No current website Python/JavaScript modules or upstream files were copied into it.
  Uses the general image -> quantize -> palette -> grid -> export workflow; preserves
  compatibility with the upstream palette JSON field names.
- `tests/*`: candidate-specific behavioral tests; no website billing or account fixtures.
- `examples/geometric.png`: synthetic geometry generated for this candidate by trifun;
  no user photos or source-photo metadata. Covered by the candidate MIT license.
- `examples/custom-palette.json`: invented reference RGB values, not DMC data. MIT.
- `licenses/*`: verbatim dependency legal material under its respective terms, plus
  `XStitchLab-PROVENANCE.txt`, a factual source-declaration note assembled by trifun.
- `README.md`, `THIRD_PARTY.md`, packaging files: candidate documentation/configuration.

## Excluded

No website generation pipeline, pet protection/cleanup/recomposition strategy, tier
planner, production frontend, account/payment code, cloud configuration, database,
session key, environment file, Git history, customer photo, marketing asset, DMC table,
ML weights, or private regression result is included.

## Historical grants and release boundary

The full website working copy is outside this candidate license scope. The retained
2026-09-20 fork includes an MIT declaration covering its snapshot and pre-existing
pet optimization modules. Current GitHub and available delivery-record checks do
not establish that the fork was ever publicly released, and do not establish that
no private source delivery ever occurred. No attempt is made to revoke grants
received by any recipient of a historical MIT copy. Later unpublished website
changes are not automatically granted to the public by publishing this candidate.

Historical recipient uncertainty concerns claims about exclusive control of old
website code; this candidate does not depend on such a claim. It does not include
those modules or change the website's license files, service behavior, or grants.
The public MIT scope is exactly this candidate and its included first-party files;
third-party materials retain their own terms. No clean-room authorship process or
upstream endorsement is asserted.

No new third-party DMC data or model permission is claimed. Adding either later requires
its own source, exact version/hash, license and distribution review.
