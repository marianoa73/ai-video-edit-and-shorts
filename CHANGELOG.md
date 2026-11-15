# Changelog

## 0.1.0

- Design of the local editing pipeline: cut list first, single render pass, shorts proposed and approved by a person.
- Hardware proposal, time-estimate model (one JSON file) and calculator (`src/estimate.py`).
- Cut-list generator from a word-level transcript (`src/cuts.py`) with an FFmpeg filter output.
- Bilingual documentation (English and Spanish), diagrams in both languages and an interactive page with an EN / ES switch.
- Tests that need no models or media: estimator, cuts, language parity, site and privacy audit.
