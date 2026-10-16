# Third-party dependencies

This is a Python source distribution. No dependency source, binary, font file, model,
thread database is vendored. The CC0 photograph in `examples/black-cat/`
is separately credited in that folder; it is not covered by the code MIT notice. Exact tested versions and hashes
are in `requirements.lock`. Install dependencies separately from their upstream distributions.

| Package | Tested version | Role | License / official source |
| --- | --- | --- | --- |
| Pillow | 12.1.0 | Raster read/quantization/preview | MIT-CMU/HPND family; https://github.com/python-pillow/Pillow |
| fpdf2 | 2.8.5 | PDF writer | LGPL-3.0; https://github.com/py-pdf/fpdf2 |
| defusedxml | See requirements.lock | fpdf2 dependency | PSF license; https://github.com/tiran/defusedxml |
| fonttools | See requirements.lock | fpdf2 dependency | MIT, plus component notices; https://github.com/fonttools/fonttools |

Verbatim legal files from the installed, tested distributions are stored in `licenses/`.
Pillow's license contains notices for bundled native components. Fonttools' external
component notices and fpdf2's embedded color-profile notice are retained separately.
The GNU GPL v3 text accompanies LGPL v3 because LGPL incorporates it.

fpdf2 is imported unmodified as a replaceable Python library. The source package does
not impose restrictions on modifying/replacing it. If distributing bundled binaries,
Docker images, embedded dependency copies, or modified library code later, reassess
source provision, notices and replacement/relinking obligations for that artifact.
This package does not relabel third-party libraries as MIT.

Build tooling (`setuptools`) is a build dependency, not runtime code. No PyMuPDF/MuPDF,
rembg, ONNX Runtime, OpenAI SDK, React, DMC database or model weights are required.

The XStitchLab source declaration is documented for context in its own file; the candidate
does not claim that the upstream work was authored by trifun. See `PROVENANCE.md`.
