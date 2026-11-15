# Limitations

[Versión en español](limitations.md)

- **Nothing is measured yet.** Every time is an estimate; the first prototype with a real 2–3 minute clip replaces them.
- **Retakes need judgment.** The tool cuts silences, fillers and immediate repeats. Choosing the best of several takes is done by an assistant or a person reading the transcript.
- **HDR phone video** must be converted to SDR with proper tone mapping or colours look washed out. Software tone mapping is slow and is not in the base estimate.
- **Green screen** needs even lighting and no green clothing. Without it, background removal by segmentation looks worse.
- **Face tracking** can lose the speaker if they leave the frame or turn away; the crop then holds its last position.
- **Whisper accuracy** depends on audio quality, accent and technical vocabulary; review the transcript for names and terms.
- **No GPU** means transcription and encoding are the slow parts on this hardware class.
- **One speaker, one camera.** Multi-camera editing and several voices are out of scope.
- **Platform rules change.** Safe zones and length limits for shorts are recommendations; check the current rules.
