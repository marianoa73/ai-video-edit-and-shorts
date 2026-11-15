# Software used

[Versión en español](software.md)

| Role | Tool | Notes |
|---|---|---|
| Decode, cut, zoom, key, subtitles, encode | FFmpeg | Quick Sync / VAAPI for H.264 and HEVC; `silencedetect`, `loudnorm`, `afftdn`, `chromakey` are built in |
| Transcription | faster-whisper (CTranslate2) | word timestamps, CPU int8, models small / medium / large-v3 |
| Silence cutting | auto-editor or FFmpeg `silencedetect` | the bundled `src/cuts.py` works from the transcript instead |
| Face tracking | MediaPipe or OpenCV | sampled a few frames per second; drives zoom and the 9:16 crop |
| Orchestration | Python 3.11+, shell | one worker, low priority |
| Reading the transcript | any language-model assistant | text only; a local model through Ollama is possible |
| Hardware access | Intel media driver, libva | provides Quick Sync on Linux |
| Shared folder | Samba or similar, private network | input and output |

## Why these choices

Everything runs offline once models are downloaded, has a permissive or well-understood licence and is scriptable. Editors that upload footage were ruled out because the face and the voice are personal data.

## Licences

This repository is MIT. Third-party tools keep their own licences; see [NOTICE.md](../NOTICE.md). FFmpeg is LGPL or GPL depending on the build, and libx264 brings GPL obligations if you redistribute binaries.
