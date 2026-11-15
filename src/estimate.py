#!/usr/bin/env python3
"""Time estimator for the editing pipeline. Reads docs/data/timing-model.json.

The numbers are ESTIMATES for the reference hardware, not measurements. Replace the
model values with your own after running the measurement protocol in docs/timing.md.
"""
import argparse
import json
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parents[1] / "docs" / "data" / "timing-model.json"


def load_model(path=MODEL_PATH):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _scale(triple, factor):
    return [round(v * factor, 2) for v in triple]


def estimate(minutes, whisper="medium", encoder="qsv", zoom=True, chroma=False, subtitles=False,
             shorts=5, short_seconds=45, versions=2, cut_ratio=0.15, model=None):
    """Return stages and totals as [low, typical, high] minutes."""
    m = model or load_model()
    if minutes <= 0:
        raise ValueError("minutes must be positive")
    if whisper not in m["whisper"]:
        raise ValueError(f"whisper must be one of {sorted(m['whisper'])}")
    if encoder not in m["render"]:
        raise ValueError(f"encoder must be one of {sorted(m['render'])}")
    if not 0 <= cut_ratio < 1:
        raise ValueError("cut_ratio must be in [0, 1)")
    kept = minutes * (1 - cut_ratio)
    out_minutes = shorts * short_seconds / 60 * versions
    stages = []

    def add(key, label, triple, group):
        stages.append({"id": key, "label": label, "group": group, "min": _scale(triple, 1)})

    add("ingest", m["stages"]["ingest"]["label"], _scale(m["stages"]["ingest"]["per_min"], minutes), "prepare")
    add("audio_prep", m["stages"]["audio_prep"]["label"], _scale(m["stages"]["audio_prep"]["per_min"], minutes), "prepare")
    add("transcribe", {"en": f"Transcription (faster-whisper {whisper}, CPU)", "es": f"Transcripción (faster-whisper {whisper}, CPU)"},
        _scale(m["whisper"][whisper], minutes), "analyze")
    add("detect_cuts", m["stages"]["detect_cuts"]["label"], _scale(m["stages"]["detect_cuts"]["per_min"], minutes), "analyze")
    add("llm_review", m["stages"]["llm_review"]["label"], _scale(m["stages"]["llm_review"]["per_min"], minutes), "analyze")
    if zoom or shorts:
        add("face_track", m["stages"]["face_track"]["label"], _scale(m["stages"]["face_track"]["per_min"], minutes), "analyze")
    add("render", {"en": f"Final render ({encoder})", "es": f"Render final ({encoder})"}, _scale(m["render"][encoder], kept), "render")
    for key, enabled in (("zoom", zoom), ("chroma", chroma), ("subtitles", subtitles)):
        if enabled:
            extra = m["render_extras"][key]
            add(key, extra["label"], _scale(extra["per_min"], kept), "render")
    if shorts:
        add("shorts", m["shorts"]["labels"], _scale(m["shorts"]["render_per_output_min"][encoder], out_minutes), "shorts")
    total = [round(sum(s["min"][i] for s in stages), 1) for i in range(3)]
    human = [round(m["human_minutes"]["cut_review"][i] + shorts * m["human_minutes"]["short_review_each"][i], 1) for i in range(3)]
    return {"input": {"minutes": minutes, "whisper": whisper, "encoder": encoder, "zoom": zoom, "chroma": chroma,
                      "subtitles": subtitles, "shorts": shorts, "short_seconds": short_seconds, "versions": versions,
                      "cut_ratio": cut_ratio},
            "stages": stages, "machine_minutes": total, "human_minutes": human, "status": m["status"]}


def fmt(minutes):
    h, mm = divmod(int(round(minutes)), 60)
    return f"{h} h {mm:02d} min" if h else f"{mm} min"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("minutes", type=float, help="length of the source video in minutes")
    ap.add_argument("--whisper", default="medium")
    ap.add_argument("--encoder", default="qsv", choices=["qsv", "x264"])
    ap.add_argument("--no-zoom", action="store_true")
    ap.add_argument("--chroma", action="store_true")
    ap.add_argument("--subtitles", action="store_true")
    ap.add_argument("--shorts", type=int, default=5)
    ap.add_argument("--short-seconds", type=int, default=45)
    ap.add_argument("--versions", type=int, default=2)
    ap.add_argument("--cut-ratio", type=float, default=0.15)
    ap.add_argument("--model", default=str(MODEL_PATH))
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    r = estimate(a.minutes, a.whisper, a.encoder, not a.no_zoom, a.chroma, a.subtitles, a.shorts, a.short_seconds,
                 a.versions, a.cut_ratio, load_model(a.model))
    if a.json:
        print(json.dumps(r, indent=2, ensure_ascii=False))
        return
    print(f"ESTIMATE ({r['status']}, not measured) for a {a.minutes:g} min source")
    print(f"{'stage':<46}{'low':>9}{'typical':>9}{'high':>9}")
    for s in r["stages"]:
        print(f"{s['label']['en']:<46}" + "".join(f"{v:>9.1f}" for v in s["min"]))
    print(f"{'TOTAL machine time (min)':<46}" + "".join(f"{v:>9.1f}" for v in r["machine_minutes"]))
    print("= " + " / ".join(fmt(v) for v in r["machine_minutes"]) + "   (unattended)")
    print("+ human review: " + " / ".join(fmt(v) for v in r["human_minutes"]))


if __name__ == "__main__":
    main()
