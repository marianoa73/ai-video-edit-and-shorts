---
name: ai-video-edit-and-shorts
description: Set up and run the local editing procedure of this repository (cut list, single render, shorts) for talking-head videos. Use when someone asks to edit, cut, subtitle or extract shorts from their own video on their own machine.
---

# AI Video Edit & Shorts: guide for an assistant

1. **Check the machine first**: Linux x86_64, FFmpeg with Quick Sync/VAAPI (`ffmpeg -hwaccels`), Python 3.11+, free disk and RAM (32 GB recommended, 16 GB with precautions; see docs/hardware.en.md).
2. **Run the arithmetic before work**: `python3 src/estimate.py <minutes>`; tell the person the range and that it is an estimate.
3. **Everything local.** Never upload footage, audio or faces. Only transcript text may be read by you.
4. **Build the cut list** with `src/cuts.py` from a word-level transcript, add retakes you find by reading the text (`--extra-cuts`), and **show the list**: reason and time for each cut. Wait for approval.
5. **Render once** from the original after approval. Do not chain re-encodes. Never delete the original.
6. **Shorts: propose, do not publish.** Candidates of 20–60 s that start with a hook and end on a complete idea; render only the approved ones, with and without subtitles.
7. Subtitles only for shorts (or when asked for the long video): chest height, two lines at most, bold with outline, active word in the accent colour.
