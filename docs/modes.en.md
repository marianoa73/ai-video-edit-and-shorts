# Operating modes

[Versión en español](modes.md)

## Two profiles, one pipeline

| | **Polished** | **Casual** |
|---|---|---|
| Typical use | technical talks, explanations | spontaneous, home-made videos |
| Silences | cut from 0.6 s (the tool default) | cut only from 1.2 s |
| Fillers and repeats | removed | only obvious stumbles |
| Retakes | best take kept | best take kept |
| Zoom / pan | emphasis on key phrases, no two in a row | none or one slow zoom |
| Subtitles on the long video | only if requested | no |
| Background | green screen or plain, if shot for it | as recorded |

Profiles are plain settings (thresholds and switches), not different code. Tune them with the first real video of each kind.

## Output rules

- Long video: 1080p, no burned-in subtitles unless asked.
- Shorts: two files from the same cut, **without** subtitles (platforms that add their own) and **with** subtitles.
- Subtitles: chest height, 2 lines at most, bold with an outline, the active word in the accent colour, inside the platform safe zones.

## Rhythm

One long video per week and one or two shorts per day taken from it. With the estimates in [timing](timing.en.md) one weekend night of machine time is enough; the limit is the time a person needs to approve.

## A session, step by step

```bash
python3 src/estimate.py 30 --shorts 5      # know the cost before starting
python3 src/cuts.py transcript.json > cuts.json
# review cuts.json, edit it, approve, then render
```
