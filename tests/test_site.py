"""The interactive page embeds the same timing model as the Python tool and gives the same numbers."""
import json
import re
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import estimate  # noqa: E402

CASES = [dict(minutes=30), dict(minutes=10, shorts=2), dict(minutes=60, shorts=8, encoder="x264", chroma=True, subtitles=True),
         dict(minutes=30, whisper="large-v3", zoom=False, shorts=0)]


class SiteTests(unittest.TestCase):
    def test_inline_model_equals_file(self):
        html = (ROOT / "docs/index.html").read_text(encoding="utf-8")
        m = re.search(r'<script type="application/json" id="model">(.*?)</script>', html, re.S)
        self.assertIsNotNone(m)
        self.assertEqual(json.loads(m.group(1)), json.loads((ROOT / "docs/data/timing-model.json").read_text(encoding="utf-8")))

    def test_every_language_block_has_a_pair_in_the_page(self):
        html = (ROOT / "docs/index.html").read_text(encoding="utf-8")
        self.assertIn('data-set="en"', html)
        self.assertIn('data-set="es"', html)
        for src in re.findall(r'src="assets/([^"]+)"', html):
            self.assertTrue((ROOT / "docs/assets" / src).is_file(), src)

    @unittest.skipUnless(shutil.which("node"), "node not installed")
    def test_js_matches_python(self):
        model = json.loads((ROOT / "docs/data/timing-model.json").read_text(encoding="utf-8"))
        for case in CASES:
            js = ("const {estimate}=require(%r);const m=%s;console.log(JSON.stringify(estimate(m,%s)))"
                  % (str(ROOT / "docs/estimator.js"), json.dumps(model), json.dumps(case)))
            out = json.loads(subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True).stdout)
            py = estimate.estimate(**case)
            for a, b in zip(out["machine_minutes"], py["machine_minutes"]):
                self.assertAlmostEqual(a, b, delta=0.11, msg=str(case))
            for a, b in zip(out["human_minutes"], py["human_minutes"]):
                self.assertAlmostEqual(a, b, delta=0.11, msg=str(case))


if __name__ == "__main__":
    unittest.main()
