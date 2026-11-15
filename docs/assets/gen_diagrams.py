#!/usr/bin/env python3
"""Rebuild every diagram in English (*.en) and Spanish (*.es) as SVG + PNG. Needs Pillow (PNG only)
and src/estimate.py for the timing chart. Run: python3 docs/assets/gen_diagrams.py"""
import math
import sys
from html import escape
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parents[1] / "src"))
import estimate  # noqa: E402

BG, BOX, FG, MUTED, ACCENT, LINE = '#0F1115', '#202630', '#EDF0F4', '#BBC5D4', '#FD5A02', '#596778'


class D:
    def __init__(self, title, subtitle, h=840, w=1400):
        self.w, self.h = w, h
        self.svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title><rect width="{w}" height="{h}" fill="{BG}"/>']
        self.im = Image.new('RGB', (w, h), BG)
        self.d = ImageDraw.Draw(self.im)
        if title:
            self.text(50, 48, title, 34, FG, True)
            self.text(50, 95, subtitle, 20, MUTED)

    def text(self, x, y, t, size=21, color=FG, bold=False, anchor='left'):
        f = ImageFont.truetype('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf', size)
        self.d.text((x, y), t, font=f, fill=color, anchor='mm' if anchor == 'middle' else ('rm' if anchor == 'right' else 'lm'))
        a = {'middle': 'middle', 'right': 'end'}.get(anchor, 'start')
        self.svg.append(f'<text x="{x}" y="{y}" dominant-baseline="middle" text-anchor="{a}" font-family="DejaVu Sans,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{escape(t)}</text>')

    def rect(self, x, y, w, h, fill=BOX, stroke=LINE, r=16, sw=3):
        self.d.rounded_rectangle((x, y, x + w, y + h), radius=r, fill=fill, outline=None if stroke == 'none' else stroke, width=sw)
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def box(self, x, y, w, h, title, lines=(), accent=False, fs=23):
        self.rect(x, y, w, h, BOX, ACCENT if accent else LINE)
        start = y + h / 2 - (len(lines) * 30) / 2
        self.text(x + w / 2, start, title, fs, FG, True, 'middle')
        for i, t in enumerate(lines):
            self.text(x + w / 2, start + (i + 1) * 30, t, 19, MUTED, False, 'middle')

    def line(self, pts):
        self.d.line(pts, fill=ACCENT, width=4)
        self.svg.append('<polyline points="' + ' '.join(f'{a},{b}' for a, b in pts) + f'" fill="none" stroke="{ACCENT}" stroke-width="4"/>')

    def arrow(self, pts, label=None):
        self.d.line(pts, fill=ACCENT, width=4, joint='curve')
        x, y = pts[-1]; px, py = pts[-2]; a = math.atan2(y - py, x - px)
        tri = [(x, y), (x - 14 * math.cos(a - .5), y - 14 * math.sin(a - .5)), (x - 14 * math.cos(a + .5), y - 14 * math.sin(a + .5))]
        self.d.polygon(tri, fill=ACCENT)
        self.svg.append('<polyline points="' + ' '.join(f'{a},{b}' for a, b in pts) + f'" fill="none" stroke="{ACCENT}" stroke-width="4"/>')
        self.svg.append('<polygon points="' + ' '.join(f'{a},{b}' for a, b in tri) + f'" fill="{ACCENT}"/>')
        if label:
            self.text(*label, 18, FG)

    def save(self, name):
        (OUT / (name + '.svg')).write_text(''.join(self.svg) + '</svg>\n')
        self.im.save(OUT / (name + '.png'))


def pipeline(L, T):
    s = D(T['t1'], T['s1'], 900)
    steps = T['steps']
    for i, (a, b) in enumerate(steps):
        col, row = i % 4, i // 4
        s.box(50 + col * 335, 170 + row * 250, 290, 150, a, b, i == 4)
        if col < 3:
            s.arrow([(340 + col * 335, 245 + row * 250), (385 + col * 335, 245 + row * 250)])
    s.arrow([(1200, 320), (1200, 360), (195, 360), (195, 420)])
    s.box(50, 690, 1290, 130, T['shorts_t'], T['shorts_l'], True)
    s.arrow([(1200, 570), (1200, 690)])
    s.save(f'01-pipeline.{L}')


def hardware(L, T):
    s = D(T['t2'], T['s2'], 900)
    s.box(50, 190, 220, 130, T['phone'][0], T['phone'][1])
    s.box(330, 190, 220, 130, T['share'][0], T['share'][1])
    s.arrow([(270, 255), (330, 255)]); s.arrow([(550, 255), (620, 255)])
    s.rect(620, 150, 520, 560, '#171C24', ACCENT, 20)
    s.text(880, 185, T['pc'], 24, FG, True, 'middle')
    for i, (a, b) in enumerate(T['parts']):
        s.box(650 + (i % 2) * 240, 225 + (i // 2) * 135, 220, 115, a, b)
    s.text(880, 515, T['pc_note'][0], 19, MUTED, False, 'middle'); s.text(880, 545, T['pc_note'][1], 19, MUTED, False, 'middle')
    s.box(650, 590, 460, 90, T['vol'][0], T['vol'][1])
    s.box(1190, 190, 170, 130, T['rev'][0], T['rev'][1])
    s.arrow([(1140, 255), (1190, 255)])
    s.box(50, 430, 400, 140, T['llm'][0], T['llm'][1], fs=21)
    s.arrow([(620, 500), (450, 500)])
    s.text(535, 470, T['textonly'][0], 17, FG, False, 'middle'); s.text(535, 532, T['textonly'][1], 17, FG, False, 'middle')
    s.box(50, 620, 500, 150, T['up'][0], T['up'][1])
    s.text(50, 850, T['hw_foot'], 20, MUTED)
    s.save(f'02-hardware.{L}')


def timing(L, T):
    r = estimate.estimate(30, 'medium', 'qsv', True, False, False, 5, 45, 2)
    s = D(T['t3'], T['s3'], 830)
    x0, scale, top = 520, 14.5, 150  # px per minute
    for g in range(0, 51, 10):
        x = x0 + g * scale
        s.d.line((x, top - 20, x, top + len(r['stages']) * 62 - 10), fill='#2b3340', width=1)
        s.svg.append(f'<line x1="{x}" y1="{top-20}" x2="{x}" y2="{top+len(r["stages"])*62-10}" stroke="#2b3340"/>')
        s.text(x, top + len(r['stages']) * 62 + 12, f'{g} min', 17, MUTED, False, 'middle')
    for i, st in enumerate(r['stages']):
        y = top + i * 62
        lo, ty, hi = st['min']
        s.text(50, y + 18, T['stage'].get(st['id'], st['label'][L]), 19, FG)
        s.rect(x0, y + 4, ty * scale, 28, ACCENT if st['id'] in ('transcribe', 'shorts') else '#8a95a8', 'none', 6, 0)
        s.d.line((x0 + lo * scale, y + 18, x0 + hi * scale, y + 18), fill=FG, width=3)
        s.svg.append(f'<line x1="{x0+lo*scale}" y1="{y+18}" x2="{x0+hi*scale}" y2="{y+18}" stroke="{FG}" stroke-width="3"/>')
        s.text(x0 + hi * scale + 12, y + 18, f'{ty:.1f} ({lo:.1f}–{hi:.1f})', 17, MUTED)
    t = r['machine_minutes']
    s.text(50, 790, T['total'].format(a=estimate.fmt(t[1]), b=estimate.fmt(t[0]), c=estimate.fmt(t[2])), 23, FG, True)
    s.save(f'03-timing.{L}')


def shorts(L, T):
    s = D(T['t4'], T['s4'], 800)
    for i, (a, b) in enumerate(T['sh']):
        col, row = i % 4, i // 4
        s.box(50 + col * 335, 170 + row * 240, 290, 150, a, b, i == 4)
        if col < 3:
            s.arrow([(340 + col * 335, 245 + row * 240), (385 + col * 335, 245 + row * 240)])
    s.arrow([(1200, 320), (1200, 360), (195, 360), (195, 410)])
    s.box(430, 410, 400, 150, T['va'][0], T['va'][1]); s.box(900, 410, 440, 150, T['vb'][0], T['vb'][1], True)
    s.arrow([(340, 485), (430, 485)])
    s.arrow([(195, 560), (195, 620), (1120, 620), (1120, 560)])
    s.text(50, 710, T['sh_foot'], 21)
    s.save(f'04-shorts.{L}')


def cuts(L, T):
    s = D(T['t5'], T['s5'], 800)
    s.box(50, 170, 300, 150, T['in'][0], T['in'][1])
    for i, (a, b) in enumerate(T['det']):
        s.box(470, 150 + i * 85, 400, 72, a, b, fs=20)
        s.arrow([(350, 245), (420, 245), (420, 186 + i * 85), (470, 186 + i * 85)])
        s.arrow([(870, 186 + i * 85), (930, 186 + i * 85), (930, 245), (990, 245)]) if i == 0 else s.line([(870, 186 + i * 85), (930, 186 + i * 85), (930, 245)])
    s.box(990, 170, 350, 150, T['merge'][0], T['merge'][1])
    s.arrow([(1165, 320), (1165, 540)])
    s.box(990, 540, 350, 130, T['list'][0], T['list'][1], True)
    s.box(520, 540, 350, 130, T['ok'][0], T['ok'][1])
    s.arrow([(990, 605), (870, 605)])
    s.box(50, 540, 400, 130, T['render'][0], T['render'][1])
    s.arrow([(520, 605), (450, 605)], (485, 575, T['yes']))
    s.arrow([(695, 670), (695, 725), (1165, 725), (1165, 670)], (930, 750, T['adjust']))
    s.save(f'05-cuts.{L}')


def framing(L, T):
    s = D(T['t6'], T['s6'], 1080)
    fx, fy, fw, fh = 70, 130, 506, 900  # 9:16 frame
    s.rect(fx, fy, fw, fh, '#10141B', LINE, 10, 3)
    s.d.rectangle((fx + 3, fy + 3, fx + fw - 3, fy + 150), fill='#2a2230'); s.svg.append(f'<rect x="{fx+3}" y="{fy+3}" width="{fw-6}" height="147" fill="#2a2230"/>')
    s.d.rectangle((fx + 3, fy + fh - 250, fx + fw - 3, fy + fh - 3), fill='#2a2230'); s.svg.append(f'<rect x="{fx+3}" y="{fy+fh-250}" width="{fw-6}" height="247" fill="#2a2230"/>')
    s.text(fx + fw / 2, fy + 75, T['ui_top'], 18, '#d9b8c8', False, 'middle'); s.text(fx + fw / 2, fy + fh - 125, T['ui_bot'], 18, '#d9b8c8', False, 'middle')
    cx, hy = fx + fw / 2, fy + 290  # silhouette
    s.d.ellipse((cx - 62, hy - 78, cx + 62, hy + 78), fill='#3a4455'); s.svg.append(f'<ellipse cx="{cx}" cy="{hy}" rx="62" ry="78" fill="#3a4455"/>')
    s.d.rounded_rectangle((cx - 170, hy + 100, cx + 170, hy + 340), radius=70, fill='#3a4455'); s.svg.append(f'<rect x="{cx-170}" y="{hy+100}" width="340" height="240" rx="70" fill="#3a4455"/>')
    s.d.rectangle((cx - 90, hy - 98, cx + 90, hy + 98), outline=ACCENT, width=2); s.svg.append(f'<rect x="{cx-90}" y="{hy-98}" width="180" height="196" fill="none" stroke="{ACCENT}" stroke-width="2"/>')
    sy = hy + 215
    s.d.rounded_rectangle((fx + 50, sy - 52, fx + fw - 50, sy + 52), radius=14, outline='#8a95a8', width=2); s.svg.append(f'<rect x="{fx+50}" y="{sy-52}" width="{fw-100}" height="104" rx="14" fill="none" stroke="#8a95a8" stroke-width="2"/>')
    s.text(cx, sy - 24, T['sub1'], 34, '#FFFFFF', True, 'middle'); s.text(cx, sy + 24, T['sub2'], 34, ACCENT, True, 'middle')
    ax = fx + fw + 50
    notes = T['notes']
    ys = [fy + 75, hy, sy, fy + fh - 125]
    for (a, b), y in zip(notes, ys):
        s.d.line((fx + fw, y, ax - 10, y), fill=ACCENT, width=2); s.svg.append(f'<line x1="{fx+fw}" y1="{y}" x2="{ax-10}" y2="{y}" stroke="{ACCENT}" stroke-width="2"/>')
        s.text(ax + 10, y - 14, a, 22, FG, True); s.text(ax + 10, y + 18, b, 19, MUTED)
    s.save(f'06-framing.{L}')


def banner(L, T):
    s = D('', '', 420)
    s.d.rectangle((0, 0, 1400, 12), fill=ACCENT); s.svg.append(f'<rect width="1400" height="12" fill="{ACCENT}"/>')
    s.text(70, 150, 'AI Video Edit & Shorts', 66, FG, True)
    s.text(70, 235, T['tag'], 25, MUTED)
    s.text(70, 300, T['tag2'], 24, ACCENT, True)
    for i in range(5):  # tiny timeline motif
        w = [150, 90, 230, 120, 180][i]; x = 70 + sum([150, 90, 230, 120, 180][:i]) + i * 14
        s.rect(x, 345, w, 34, BOX, ACCENT if i in (1, 3) else LINE, 8, 2)
    s.save(f'banner.{L}')


EN = dict(
    t1='01 · From a raw 4K take to published files', s1='Local processing · one job at a time · nothing is published without a person',
    steps=[('Raw 4K take', ['one continuous recording', 'in a shared folder']), ('Prepare', ['probe, HDR to SDR', 'proxy + clean audio']),
           ('Transcribe', ['faster-whisper on CPU', 'timestamp for every word']), ('Detect cuts', ['silences and fillers', 'repeats and retakes']),
           ('Cut list', ['what goes and why', 'a person approves it']), ('Montage', ['FFmpeg trim + join', 'micro-fades, loudness']),
           ('Look', ['zoom/pan, green screen', 'subtitles only if wanted']), ('Final file', ['1080p H.264, CRF 18', 'originals untouched'])],
    shorts_t='Shorts from the same take', shorts_l=['candidates proposed from the transcript → person approves → 9:16 reframe with face tracking', 'two versions per short: without and with subtitles'],
    t2='02 · Hardware and network (generic)', s2='A small x86 Linux box is enough; a GPU is an optional upgrade, not a requirement',
    phone=('Phone', ['4K30 recording']), share=('Shared folder', ['private LAN only']),
    pc='Mini PC · Ubuntu 24.04 · x86_64', parts=[('CPU', ['4 cores / 8 threads']), ('iGPU', ['Quick Sync: decode', 'and encode video']), ('RAM', ['32 GB']), ('NVMe SSD', ['1 TB'])],
    pc_note=('Whisper and face tracking run on the CPU;', 'FFmpeg uses the iGPU for H.264/HEVC.'), vol=('Dedicated video volume', ['≈ 200 GB, separate from the system']),
    rev=('Reviewer', ['browser, LAN']), llm=('Language-model assistant', ['reads transcript text only', 'a local model is possible']), textonly=('text only', 'no audio/video'),
    up=('Optional upgrade', ['workstation + NVIDIA GPU', 'faster Whisper and NVENC, if measured']), hw_foot='A UPS protects long renders; keep originals on a second disk until published.',
    t3='03 · Estimated machine time for a 30 min source', s3='ESTIMATES, not measurements · bar = typical, whisker = low–high · 5 shorts × 2 versions',
    stage={'ingest': 'Prepare (probe, HDR→SDR, proxy)', 'audio_prep': 'Audio extraction + denoise', 'transcribe': 'Transcription (medium, CPU)', 'detect_cuts': 'Cut detection',
           'llm_review': 'Assistant reads transcript', 'face_track': 'Face tracking (sampled)', 'render': 'Final render (Quick Sync)', 'zoom': 'Zoom and pan', 'shorts': 'Shorts rendering'},
    total='Total unattended: typically {a} (range {b} – {c}) + about 15 min of human review',
    t4='04 · From the long take to shorts', s4='The system proposes; a person chooses; only approved shorts are rendered',
    sh=[('Transcript', ['words + timestamps']), ('Idea blocks', ['complete thoughts only', 'never cut mid-idea']), ('Score', ['hook in first sentence', '20–60 s, clear close']), ('Rank', ['assistant orders the best', 'with title and reason']),
        ('Approve', ['a person picks', 'which ones to render'])],
    va=('Version A', ['no subtitles', 'for platforms that add their own']), vb=('Version B', ['burned-in subtitles', 'chest height, word in color']), sh_foot='Reframe 16:9 → 9:16 follows the face; every short is a crop of the 4K frame, so it stays sharp.',
    t5='05 · How cuts are decided', s5='Every cut has a reason and a timestamp; nothing is rendered before approval',
    **{'in': ('Transcript', ['word timestamps', 'audio levels'])}, det=[('Silences', ['≥ 0.6 s, keep 0.15 s each side']), ('Fillers', ['configurable list per language']), ('Repeats', ['same phrase said twice in a row']), ('Retakes', ['read by assistant or person'])],
    merge=('Merge', ['overlaps joined', 'keep list built']), list=('Cut list', ['reason + time for each', 'saved as JSON']), ok=('Approved?', ['person confirms', 'or edits the list']), adjust='adjust', yes='yes', render=('Render', ['one pass from the original', 'no chain of re-encodes']),
    t6='06 · Subtitle placement and 9:16 safe zones', s6='Illustration with a neutral silhouette · no real footage is published in this repository',
    ui_top='platform UI (top)', ui_bot='caption + buttons (bottom)', sub1='THE ACTIVE WORD', sub2='IN COLOR',
    notes=[('Top zone', 'keep it free of text'), ('Face', 'tracked; zoom keeps it centered'), ('Subtitles at chest height', 'max 2 lines, bold with outline'), ('Bottom zone', 'covered by the app interface')],
    tag='Local, private editing of long talking-head videos and the shorts that come out of them.', tag2='Cuts · subtitles · zooms · green screen · shorts — with a person in charge',
)
ES = dict(
    t1='01 · De una toma 4K cruda a los archivos finales', s1='Procesamiento local · un trabajo a la vez · nada se publica sin una persona',
    steps=[('Toma 4K cruda', ['una grabación continua', 'en carpeta compartida']), ('Preparar', ['análisis, HDR a SDR', 'proxy + audio limpio']),
           ('Transcribir', ['faster-whisper en CPU', 'tiempo de cada palabra']), ('Detectar cortes', ['silencios y muletillas', 'repeticiones y retomas']),
           ('Lista de cortes', ['qué se saca y por qué', 'la aprueba una persona']), ('Montaje', ['FFmpeg: cortar y unir', 'micro-fundidos, volumen']),
           ('Aspecto', ['zoom/paneo, fondo verde', 'subtítulos sólo si se piden']), ('Archivo final', ['1080p H.264, CRF 18', 'originales intactos'])],
    shorts_t='Shorts de la misma toma', shorts_l=['candidatos propuestos desde la transcripción → una persona aprueba → reencuadre 9:16 con seguimiento de cara', 'dos versiones por short: sin y con subtítulos'],
    t2='02 · Hardware y red (genérico)', s2='Alcanza con una caja Linux x86 chica; la GPU es una mejora opcional, no un requisito',
    phone=('Celular', ['grabación 4K30']), share=('Carpeta común', ['sólo LAN privada']),
    pc='Mini PC · Ubuntu 24.04 · x86_64', parts=[('CPU', ['4 núcleos / 8 hilos']), ('GPU integrada', ['Quick Sync:', 'decodifica y codifica']), ('RAM', ['32 GB']), ('SSD NVMe', ['1 TB'])],
    pc_note=('Whisper y seguimiento de cara van en la CPU;', 'FFmpeg usa la GPU integrada para H.264/HEVC.'), vol=('Volumen de video dedicado', ['≈ 200 GB, separado del sistema']),
    rev=('Revisor', ['navegador, LAN']), llm=('Asistente de lenguaje', ['lee sólo el texto', 'puede ser un modelo local']), textonly=('sólo texto', 'sin audio/video'),
    up=('Mejora opcional', ['estación + GPU NVIDIA', 'Whisper y NVENC más rápidos, si se mide']), hw_foot='Un UPS protege los renders largos; conservá los originales en un segundo disco hasta publicar.',
    t3='03 · Tiempo de máquina estimado para un video de 30 min', s3='ESTIMACIONES, no mediciones · barra = típico, línea = mínimo–máximo · 5 shorts × 2 versiones',
    stage={'ingest': 'Preparar (análisis, HDR→SDR, proxy)', 'audio_prep': 'Extracción y limpieza de audio', 'transcribe': 'Transcripción (medium, CPU)', 'detect_cuts': 'Detección de cortes',
           'llm_review': 'El asistente lee la transcripción', 'face_track': 'Seguimiento de cara (muestreado)', 'render': 'Render final (Quick Sync)', 'zoom': 'Zoom y paneo', 'shorts': 'Render de shorts'},
    total='Total sin supervisión: típico {a} (rango {b} – {c}) + unos 15 min de revisión humana',
    t4='04 · Del video largo a los shorts', s4='El sistema propone; una persona elige; sólo se renderizan los shorts aprobados',
    sh=[('Transcripción', ['palabras + tiempos']), ('Bloques de idea', ['sólo ideas completas', 'nunca cortar a la mitad']), ('Puntaje', ['gancho en la 1.ª frase', '20–60 s, cierre claro']), ('Ranking', ['el asistente ordena', 'con título y motivo']),
        ('Aprobar', ['una persona elige', 'cuáles renderizar'])],
    va=('Versión A', ['sin subtítulos', 'para plataformas que ponen los suyos']), vb=('Versión B', ['subtítulos impresos', 'altura del pecho, palabra en color']), sh_foot='El reencuadre 16:9 → 9:16 sigue la cara; cada short es un recorte del cuadro 4K, así que mantiene la nitidez.',
    t5='05 · Cómo se deciden los cortes', s5='Cada corte tiene un motivo y un tiempo; nada se renderiza antes de la aprobación',
    **{'in': ('Transcripción', ['tiempo por palabra', 'niveles de audio'])}, det=[('Silencios', ['≥ 0,6 s, conserva 0,15 s a cada lado']), ('Muletillas', ['lista configurable por idioma']), ('Repeticiones', ['misma frase dicha dos veces seguidas']), ('Tomas falladas', ['las lee un asistente o una persona'])],
    merge=('Unir', ['se juntan los solapes', 'se arma lo que queda']), list=('Lista de cortes', ['motivo + tiempo de cada uno', 'guardada como JSON']), ok=('¿Aprobada?', ['una persona confirma', 'o edita la lista']), adjust='ajustar', yes='sí', render=('Render', ['una pasada desde el original', 'sin cadena de recompresiones']),
    t6='06 · Ubicación de subtítulos y zonas seguras 9:16', s6='Ilustración con silueta neutra · en este repositorio no se publica material real',
    ui_top='interfaz de la plataforma (arriba)', ui_bot='descripción + botones (abajo)', sub1='LA PALABRA ACTIVA', sub2='EN COLOR',
    notes=[('Zona superior', 'dejarla libre de texto'), ('Cara', 'con seguimiento; el zoom la mantiene centrada'), ('Subtítulos a la altura del pecho', 'máx. 2 líneas, negrita con contorno'), ('Zona inferior', 'la tapa la interfaz de la app')],
    tag='Edición local y privada de videos largos hablados a cámara y de los shorts que salen de ellos.', tag2='Cortes · subtítulos · zooms · fondo verde · shorts — con una persona al mando',
)

if __name__ == '__main__':
    for L, T in (('en', EN), ('es', ES)):
        for f in (pipeline, hardware, timing, shorts, cuts, framing, banner):
            f(L, T)
    print('OK', len(list(OUT.glob('*.png'))), 'PNG')
