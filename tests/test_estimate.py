import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import estimate  # noqa: E402


class EstimateTests(unittest.TestCase):
    def test_ranges_are_ordered(self):
        r = estimate.estimate(30)
        for s in r["stages"]:
            self.assertLessEqual(s["min"][0], s["min"][1])
            self.assertLessEqual(s["min"][1], s["min"][2])
        lo, ty, hi = r["machine_minutes"]
        self.assertLess(lo, ty)
        self.assertLess(ty, hi)

    def test_longer_video_costs_more(self):
        self.assertGreater(estimate.estimate(60)["machine_minutes"][1], estimate.estimate(30)["machine_minutes"][1])

    def test_options_change_total(self):
        base = estimate.estimate(30, shorts=0, zoom=False)["machine_minutes"][1]
        self.assertGreater(estimate.estimate(30, shorts=0, zoom=False, chroma=True)["machine_minutes"][1], base)
        self.assertGreater(estimate.estimate(30, shorts=0, zoom=False, subtitles=True)["machine_minutes"][1], base)
        self.assertGreater(estimate.estimate(30, shorts=0, zoom=False, whisper="large-v3")["machine_minutes"][1], base)
        self.assertGreater(estimate.estimate(30, shorts=0, zoom=False, encoder="x264")["machine_minutes"][1], base)
        self.assertGreater(estimate.estimate(30, shorts=3, zoom=False)["machine_minutes"][1], base)

    def test_documented_default_scenario(self):
        t = estimate.estimate(30)["machine_minutes"]
        self.assertEqual([round(v) for v in t], [55, 85, 137])

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            estimate.estimate(0)
        with self.assertRaises(ValueError):
            estimate.estimate(10, whisper="huge")
        with self.assertRaises(ValueError):
            estimate.estimate(10, encoder="nvenc")
        with self.assertRaises(ValueError):
            estimate.estimate(10, cut_ratio=1)


if __name__ == "__main__":
    unittest.main()
