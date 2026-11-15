#!/usr/bin/env python3
"""Build a cut list (EDL) from a word-level transcript. No models, no media: pure logic.

Input JSON: {"words": [{"w": "hello", "s": 0.00, "e": 0.40}, ...]} (seconds).
Output: cuts with a reason each, the segments to keep, and an FFmpeg filter graph.
Retakes (a sentence said again, better) are NOT decided here: an assistant or a person reads the
transcript and adds them with --extra-cuts. Nothing is rendered until the list is approved.
"""
import argparse
import json
import re
import sys
from pathlib import Path

FILLERS = {
    "es": {"eh", "ehh", "em", "mm", "mmm", "este", "o sea", "bueno", "digamos", "ehm"},
    "en": {"uh", "um", "uhm", "er", "erm", "like", "you know", "i mean"},
}


def norm(word):
    return re.sub(r"[^\w']", "", word.lower())


def find_silences(words, min_silence=0.6, keep=0.15, start=0.0, end=None):
    cuts = []
    prev_end = start
    for w in words:
        gap = w["s"] - prev_end
        if gap >= min_silence:
            cuts.append({"start": round(prev_end + keep, 3), "end": round(w["s"] - keep, 3), "reason": "silence",
                         "text": ""})
        prev_end = max(prev_end, w["e"])
    if end is not None and end - prev_end >= min_silence:
        cuts.append({"start": round(prev_end + keep, 3), "end": round(end, 3), "reason": "silence", "text": ""})
    return [c for c in cuts if c["end"] - c["start"] > 0.05]


def find_fillers(words, lang="es", extra=()):
    table = set(FILLERS.get(lang, set())) | {norm(x) for x in extra}
    single = {f for f in table if " " not in f}
    multi = sorted((f for f in table if " " in f), key=lambda f: -len(f.split()))
    cuts, i = [], 0
    while i < len(words):
        hit = None
        for phrase in multi:
            n = len(phrase.split())
            if i + n <= len(words) and " ".join(norm(w["w"]) for w in words[i:i + n]) == phrase:
                hit = n
                break
        if hit is None and norm(words[i]["w"]) in single:
            hit = 1
        if hit:
            seg = words[i:i + hit]
            cuts.append({"start": seg[0]["s"], "end": seg[-1]["e"], "reason": "filler",
                         "text": " ".join(w["w"] for w in seg)})
            i += hit
        else:
            i += 1
    return cuts


def find_repeats(words, max_len=4):
    """An immediate repetition of the same 1-4 word phrase: drop the first occurrence, keep the last."""
    cuts, i = [], 0
    toks = [norm(w["w"]) for w in words]
    while i < len(words):
        found = False
        for n in range(max_len, 0, -1):
            if i + 2 * n <= len(words) and toks[i:i + n] == toks[i + n:i + 2 * n] and all(toks[i:i + n]):
                cuts.append({"start": words[i]["s"], "end": words[i + n]["s"], "reason": "repeat",
                             "text": " ".join(w["w"] for w in words[i:i + n])})
                i += n
                found = True
                break
        if not found:
            i += 1
    return cuts


def merge(cuts, join_gap=0.05):
    out = []
    for c in sorted(cuts, key=lambda c: (c["start"], c["end"])):
        if out and c["start"] <= out[-1]["end"] + join_gap:
            last = out[-1]
            last["end"] = max(last["end"], c["end"])
            if c["reason"] not in last["reason"].split("+"):
                last["reason"] += "+" + c["reason"]
            last["text"] = (last["text"] + " " + c["text"]).strip()
        else:
            out.append(dict(c))
    return out


def keep_segments(cuts, duration):
    keep, pos = [], 0.0
    for c in cuts:
        if c["start"] > pos:
            keep.append((round(pos, 3), round(c["start"], 3)))
        pos = max(pos, c["end"])
    if duration > pos:
        keep.append((round(pos, 3), round(duration, 3)))
    return [(a, b) for a, b in keep if b - a > 0.05]


def ffmpeg_filter(keep, fade=0.02):
    """Filter graph that trims video and audio to the kept segments, with a tiny audio fade at each join."""
    parts, labels = [], []
    for i, (a, b) in enumerate(keep):
        parts.append(f"[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS[v{i}]")
        d = round(b - a, 3)
        parts.append(f"[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,"
                     f"afade=t=in:d={fade},afade=t=out:st={max(d - fade, 0)}:d={fade}[a{i}]")
        labels.append(f"[v{i}][a{i}]")
    parts.append("".join(labels) + f"concat=n={len(keep)}:v=1:a=1[v][a]")
    return ";".join(parts)


def build(words, lang="es", min_silence=0.6, keep=0.15, extra_cuts=(), extra_fillers=(), duration=None):
    if not words:
        raise ValueError("empty transcript")
    duration = duration if duration is not None else words[-1]["e"] + keep
    cuts = (find_silences(words, min_silence, keep, 0.0, duration) + find_fillers(words, lang, extra_fillers)
            + find_repeats(words) + list(extra_cuts))
    cuts = merge(cuts)
    kept = keep_segments(cuts, duration)
    removed = round(duration - sum(b - a for a, b in kept), 3)
    return {"duration": round(duration, 3), "removed": removed, "removed_ratio": round(removed / duration, 3),
            "cuts": cuts, "keep": kept}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("transcript")
    ap.add_argument("--lang", default="es", choices=sorted(FILLERS))
    ap.add_argument("--min-silence", type=float, default=0.6)
    ap.add_argument("--keep", type=float, default=0.15, help="seconds of pause kept on each side of a silence cut")
    ap.add_argument("--extra-cuts", help="JSON list of {start,end,reason,text} added by a reviewer")
    ap.add_argument("--filter", action="store_true", help="print the FFmpeg filter graph instead of the list")
    a = ap.parse_args()
    data = json.loads(Path(a.transcript).read_text(encoding="utf-8"))
    extra = json.loads(Path(a.extra_cuts).read_text(encoding="utf-8")) if a.extra_cuts else []
    r = build(data["words"], a.lang, a.min_silence, a.keep, extra, duration=data.get("duration"))
    if a.filter:
        print(ffmpeg_filter(r["keep"]))
    else:
        print(json.dumps(r, indent=2, ensure_ascii=False))
        print(f"# {len(r['cuts'])} cuts, {r['removed']} s removed ({r['removed_ratio']:.0%}). Review before rendering.", file=sys.stderr)


if __name__ == "__main__":
    main()
