<p align="center"><img src="docs/assets/banner.en.png?v=3" alt="AI Video Edit & Shorts" width="100%"></p>

<p align="center">
<a href="README.es.md"><img src="docs/assets/btn-es.svg?v=3" height="44" alt="Ver en Español"></a>
&nbsp;
<a href="https://marianoa73.github.io/ai-video-edit-and-shorts/"><img src="docs/assets/btn-site-en.svg?v=3" height="44" alt="Interactive page (EN / ES)"></a>
</p>

> *Private, local editing: from one raw 4K take to a clean video and its shorts.*

**A reproducible design for cutting silences, filler words and repeats, adding subtitles, zooms and a green-screen background, and extracting shorts — on a small Linux box, with a person approving every step that matters.**

Author: Mariano Araujo · MIT License · [Versión en español](README.es.md)

## In one minute

1. **Problem:** a long talking-head video takes hours to edit by hand, and cloud editors need your face and voice.
2. **Decision:** record once without stopping, process everything locally, and show a *cut list* (what goes and why) before rendering anything.
3. **What it includes:** the pipeline design, a hardware proposal, time estimates with their assumptions, two operating profiles, a cut-list generator (`src/cuts.py`) and a time calculator (`src/estimate.py`).
4. **Status:** design plus two small reference tools. The full pipeline is **not built or measured yet**: every time in this repository is an *estimate* and says so.
5. **Verify the logic without models or media:**
   ```bash
   python3 -m unittest discover -s tests -v
   python3 src/estimate.py 30
   python3 src/cuts.py examples/transcript.example.json
   ```

![From a raw take to published files](docs/assets/01-pipeline.en.svg?v=3)

[High-resolution PNG](docs/assets/01-pipeline.en.png?v=3) · [Versión en español](README.es.md)

## What it does

| Step | What happens | Where it runs |
|---|---|---|
| Cuts | silences, fillers and immediate repeats detected from word timestamps; retakes read by an assistant or a person | CPU |
| Cut list | every cut with reason and time, shown **before** rendering | a person approves |
| Montage | one FFmpeg pass from the original, micro-fades at each join, loudness normalised | iGPU / CPU |
| Look | zoom and pan on the 4K frame, optional green-screen background, optional subtitles | iGPU / CPU |
| Shorts | candidates proposed, a person approves, 9:16 reframe that follows the face; versions with and without subtitles | iGPU / CPU |

![How cuts are decided](docs/assets/05-cuts.en.svg?v=3)

## How long it takes (estimates)

For a 30-minute source on the reference mini PC (4 cores / 8 threads, 32 GB, integrated GPU, no discrete GPU): about **1 h 25 min** of unattended machine time (range 55 min – 2 h 17 min) including five shorts in two versions, plus roughly 15 minutes of human review. Transcription and shorts dominate.

![Estimated machine time](docs/assets/03-timing.en.svg?v=3)

These are **estimates, not measurements**. [How they are built, how to change them and how to measure your own](docs/timing.en.md).

## Hardware proposal

A small x86 Linux machine is enough; a GPU is an optional upgrade only if measurements justify it.

![Hardware and network](docs/assets/02-hardware.en.svg?v=3)

Details, storage sizing and the upgrade path: [docs/hardware.en.md](docs/hardware.en.md).

## Shorts and subtitles

![From the long take to shorts](docs/assets/04-shorts.en.svg?v=3)

![Subtitle placement](docs/assets/06-framing.en.svg?v=3)

## Operating modes

Two profiles share the same pipeline: **polished** (technical content: tight cuts, zooms, graphics) and **casual** (spontaneous: only long silences and stumbles). See [docs/modes.en.md](docs/modes.en.md).

## Software used

FFmpeg (with Quick Sync/VAAPI), faster-whisper, auto-editor or FFmpeg `silencedetect`, MediaPipe/OpenCV for face tracking, Python 3.11+. Versions, roles and licences: [docs/software.en.md](docs/software.en.md) and [NOTICE.md](NOTICE.md).

## Privacy rules

- **Face and voice never leave the machine.** No cloud editor, no cloud transcription, no cloud upload of footage.
- Only the **text** of the transcript may be read by a language-model assistant; a local model is an option.
- No footage, voice sample or face image is included in this repository; the illustrations use a neutral silhouette.
- Originals are never deleted by the pipeline.

## Contributors

The author, with Claude, Codex and OpenRouter/OpenCode as AI assistants under human review. See [CONTRIBUTORS.md](CONTRIBUTORS.md).

## Documentation

| Guide | English | Español |
|---|---|---|
| Architecture | [architecture.en.md](docs/architecture.en.md) | [architecture.md](docs/architecture.md) |
| Hardware | [hardware.en.md](docs/hardware.en.md) | [hardware.md](docs/hardware.md) |
| Time estimates | [timing.en.md](docs/timing.en.md) | [timing.md](docs/timing.md) |
| Operating modes | [modes.en.md](docs/modes.en.md) | [modes.md](docs/modes.md) |
| Software | [software.en.md](docs/software.en.md) | [software.md](docs/software.md) |
| Limitations | [limitations.en.md](docs/limitations.en.md) | [limitations.md](docs/limitations.md) |

Related: [ai-animated-shorts](https://github.com/marianoa73/ai-animated-shorts) (animated dialogue series, a different pipeline) · [ai-split-raspberry-pi](https://github.com/marianoa73/ai-split-raspberry-pi).
