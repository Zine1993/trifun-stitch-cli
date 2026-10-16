import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image
from trifun_stitch.core import convert, load_palette, validate
from trifun_stitch.export import export


class ConversionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.image = self.root / "private-photo-name.png"
        Image.new("RGB", (40, 30), "white").save(self.image)

    def tearDown(self):
        self.temp.cleanup()

    def test_white_is_a_real_stitch_and_no_network_needed(self):
        with patch("socket.socket", side_effect=AssertionError("Network forbidden")):
            pattern = convert(self.image, width=8, colors=4)
            validate(pattern)
            export(pattern, self.root / "output")
        self.assertEqual(pattern["total_stitches"], 48)
        self.assertEqual(sum(e["stitches"] for e in pattern["legend"]), 48)
        text = (self.root/"output"/"pattern.json").read_text()
        self.assertNotIn(str(self.root), text)
        self.assertNotIn(self.image.name, text)
        self.assertEqual((self.root/"output"/"pattern.pdf").read_bytes()[:5], b"%PDF-")

    def test_alpha_excludes_cells_but_preserves_white(self):
        img = Image.new("RGBA", (2, 2), "white")
        img.putpixel((0, 0), (0, 0, 0, 0))
        img.save(self.image)
        pattern = convert(self.image, width=2)
        validate(pattern)
        self.assertEqual(pattern["empty_cells"], 1)
        self.assertEqual(pattern["total_stitches"], 3)

    def test_mapping_merges_same_thread_and_preserves_counts(self):
        img = Image.new("RGB", (2, 1))
        img.putdata([(50, 0, 0), (60, 0, 0)])
        img.save(self.image)
        palette = self.root/"palette.json"
        palette.write_text(json.dumps({"brand": "Test", "colors": [{"code": "one", "name": "One", "rgb": [55,0,0]}]}))
        pattern = convert(self.image, width=2, colors=2, palette_path=palette)
        validate(pattern)
        self.assertEqual(len(pattern["legend"]), 1)
        self.assertEqual(pattern["legend"][0]["stitches"], 2)

    def test_invalid_palette_and_duplicate_codes_rejected(self):
        path = self.root/"palette.json"
        for colors in [[], [None], [{"code": "a", "name": "A", "rgb": [True,0,0]}],
                       [{"code": "a", "name": "A", "rgb": [0,0,0]}]*2]:
            path.write_text(json.dumps({"colors": colors}))
            with self.assertRaises(ValueError):
                load_palette(path)

    def test_existing_output_never_overwritten(self):
        target = self.root/"output"
        target.mkdir()
        sentinel = target/"keep.txt"
        sentinel.write_text("keep")
        result = subprocess.run([sys.executable, "-m", "trifun_stitch", "convert", str(self.image), "--output", str(target)], capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(list(target.iterdir()), [sentinel])
        self.assertEqual(sentinel.read_text(), "keep")

    def test_limits_fully_transparent_and_corrupt_inputs(self):
        for width, colors, fabric in [(0,8,14), (301,8,14), (20,63,14), (20,8,0)]:
            with self.assertRaises(ValueError):
                convert(self.image, width, colors, fabric)
        Image.new("RGBA", (2, 2), (0,0,0,0)).save(self.image)
        with self.assertRaisesRegex(ValueError, "no visible"):
            convert(self.image)
        self.image.write_bytes(b"not an image")
        with self.assertRaises(OSError):
            convert(self.image)

    def test_exif_orientation_and_extreme_aspect_ratio(self):
        img = Image.new("RGB", (10, 20), "red")
        exif = Image.Exif()
        exif[274] = 6
        img.save(self.image, exif=exif)
        pattern = convert(self.image, width=20)
        self.assertEqual((pattern["width"], pattern["height"]), (20,10))
        Image.new("RGB", (1, 1000), "red").save(self.image)
        with self.assertRaisesRegex(ValueError, "200,000"):
            convert(self.image, width=300)

    def test_tiled_pdf_unicode_and_metadata_stripping(self):
        img = Image.new("RGB", (80, 120), "blue")
        exif = Image.Exif()
        exif[315] = "PRIVATE CAMERA OWNER"
        img.save(self.image, exif=exif)
        pattern = convert(self.image, width=80, title="测试宠物")
        export(pattern, self.root/"tiles")
        self.assertEqual(json.loads((self.root/"tiles"/"pattern.json").read_text())["title"], "测试宠物")
        with Image.open(self.root/"tiles"/"grid.png") as output:
            self.assertFalse(output.getexif())
            self.assertNotIn("exif", output.info)

    def test_validation_rejects_wrong_counts(self):
        pattern = convert(self.image)
        pattern["total_stitches"] -= 1
        with self.assertRaises(ValueError):
            validate(pattern)


if __name__ == "__main__":
    unittest.main()
