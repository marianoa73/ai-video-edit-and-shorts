/* Browser/Node port of src/estimate.py. Same model file, same maths; tests/test_site.py compares both. */
(function (root) {
  function scale(t, f) { return t.map(function (v) { return Math.round(v * f * 100) / 100; }); }
  function estimate(m, o) {
    var minutes = o.minutes, whisper = o.whisper || 'medium', encoder = o.encoder || 'qsv';
    var zoom = o.zoom !== false, chroma = !!o.chroma, subtitles = !!o.subtitles;
    var shorts = o.shorts === undefined ? 5 : o.shorts, shortSeconds = o.shortSeconds || 45;
    var versions = o.versions || 2, cutRatio = o.cutRatio === undefined ? 0.15 : o.cutRatio;
    var kept = minutes * (1 - cutRatio), outMin = shorts * shortSeconds / 60 * versions, st = [];
    function add(id, label, t, group) { st.push({ id: id, label: label, group: group, min: t }); }
    ['ingest', 'audio_prep'].forEach(function (k) { add(k, m.stages[k].label, scale(m.stages[k].per_min, minutes), 'prepare'); });
    add('transcribe', { en: 'Transcription (faster-whisper ' + whisper + ', CPU)', es: 'Transcripción (faster-whisper ' + whisper + ', CPU)' }, scale(m.whisper[whisper], minutes), 'analyze');
    ['detect_cuts', 'llm_review'].forEach(function (k) { add(k, m.stages[k].label, scale(m.stages[k].per_min, minutes), 'analyze'); });
    if (zoom || shorts) add('face_track', m.stages.face_track.label, scale(m.stages.face_track.per_min, minutes), 'analyze');
    add('render', { en: 'Final render (' + encoder + ')', es: 'Render final (' + encoder + ')' }, scale(m.render[encoder], kept), 'render');
    [['zoom', zoom], ['chroma', chroma], ['subtitles', subtitles]].forEach(function (p) {
      if (p[1]) add(p[0], m.render_extras[p[0]].label, scale(m.render_extras[p[0]].per_min, kept), 'render');
    });
    if (shorts) add('shorts', m.shorts.labels, scale(m.shorts.render_per_output_min[encoder], outMin), 'shorts');
    var total = [0, 1, 2].map(function (i) { return Math.round(st.reduce(function (a, s) { return a + s.min[i]; }, 0) * 10) / 10; });
    var human = [0, 1, 2].map(function (i) { return Math.round((m.human_minutes.cut_review[i] + shorts * m.human_minutes.short_review_each[i]) * 10) / 10; });
    return { stages: st, machine_minutes: total, human_minutes: human };
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = { estimate: estimate };
  else root.estimate = estimate;
})(typeof window !== 'undefined' ? window : this);
