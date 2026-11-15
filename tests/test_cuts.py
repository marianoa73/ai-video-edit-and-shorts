import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import cuts  # noqa: E402


def words(seq):
    return [{"w": w, "s": s, "e": e} for w, s, e in seq]


class CutTests(unittest.TestCase):
    def test_example_matches_docs(self):
        data = json.loads((ROOT / "examples" / "transcript.example.json").read_text(encoding="utf-8"))
        r = cuts.build(data["words"], "es", duration=data["duration"])
        self.assertEqual([c["reason"] for c in r["cuts"]], ["filler", "repeat", "silence", "filler"])
        self.assertEqual(r["removed"], 2.5)
        self.assertEqual(len(r["keep"]), 5)

    def test_long_silence_keeps_padding(self):
        r = cuts.find_silences(words([("a", 0, 1), ("b", 3, 4)]), 0.6, 0.15)
        self.assertEqual(r, [{"start": 1.15, "end": 2.85, "reason": "silence", "text": ""}])

    def test_short_pause_is_kept(self):
        self.assertEqual(cuts.find_silences(words([("a", 0, 1), ("b", 1.3, 2)])), [])

    def test_filler_languages(self):
        w = words([("um", 0, .2), ("hello", .3, .6), ("you", .7, .8), ("know", .8, .9)])
        reasons = [c["text"] for c in cuts.find_fillers(w, "en")]
        self.assertEqual(reasons, ["um", "you know"])
        self.assertEqual(cuts.find_fillers(w, "es"), [])

    def test_repeat_drops_first_occurrence_only(self):
        w = words([("we", 0, .2), ("we", .3, .5), ("go", .6, .9)])
        r = cuts.find_repeats(w)
        self.assertEqual(len(r), 1)
        self.assertEqual((r[0]["start"], r[0]["end"]), (0, .3))

    def test_merge_joins_overlaps_and_reasons(self):
        m = cuts.merge([{"start": 1, "end": 2, "reason": "filler", "text": "eh"},
                        {"start": 1.5, "end": 3, "reason": "silence", "text": ""}])
        self.assertEqual(len(m), 1)
        self.assertEqual((m[0]["start"], m[0]["end"], m[0]["reason"]), (1, 3, "filler+silence"))

    def test_extra_cuts_from_reviewer(self):
        data = json.loads((ROOT / "examples" / "transcript.example.json").read_text(encoding="utf-8"))
        extra = [{"start": 5.5, "end": 5.9, "reason": "retake", "text": "esto"}]
        r = cuts.build(data["words"], "es", extra_cuts=extra, duration=data["duration"])
        self.assertIn("retake", [c["reason"] for c in r["cuts"]])

    def test_filter_graph_counts_segments(self):
        keep = [(0, 1), (2, 3.5)]
        g = cuts.ffmpeg_filter(keep)
        self.assertIn("concat=n=2:v=1:a=1[v][a]", g)
        self.assertEqual(g.count("trim=start"), 4)

    def test_empty_transcript(self):
        with self.assertRaises(ValueError):
            cuts.build([])


if __name__ == "__main__":
    unittest.main()
