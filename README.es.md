<p align="center"><img src="docs/assets/banner.es.png?v=3" alt="AI Video Edit & Shorts" width="100%"></p>

<p align="center">
<a href="README.md"><img src="docs/assets/btn-en.svg?v=3" height="44" alt="View in English"></a>
&nbsp;
<a href="https://marianoa73.github.io/ai-video-edit-and-shorts/?lang=es"><img src="docs/assets/btn-site-es.svg?v=3" height="44" alt="Página interactiva (ES / EN)"></a>
</p>

> *Edición privada y local: de una toma 4K cruda a un video limpio y sus shorts.*

**Un diseño reproducible para cortar silencios, muletillas y repeticiones, sumar subtítulos, zooms y fondo verde, y sacar shorts — en una caja Linux chica, con una persona aprobando cada paso importante.**

Autor: Mariano Araujo · Licencia MIT · [English version](README.md)

## En un minuto

1. **Problema:** un video largo hablado a cámara lleva horas de edición a mano, y los editores en la nube piden tu cara y tu voz.
2. **Decisión:** grabar una vez sin cortar, procesar todo en local y mostrar una *lista de cortes* (qué se saca y por qué) antes de renderizar nada.
3. **Qué incluye:** el diseño del pipeline, una propuesta de hardware, estimaciones de tiempo con sus supuestos, dos perfiles de trabajo, un generador de listas de cortes (`src/cuts.py`) y una calculadora de tiempos (`src/estimate.py`).
4. **Estado:** diseño más dos herramientas de referencia chicas. El pipeline completo **todavía no está construido ni medido**: cada tiempo de este repositorio es una *estimación* y lo dice.
5. **Verificar la lógica sin modelos ni videos:**
   ```bash
   python3 -m unittest discover -s tests -v
   python3 src/estimate.py 30
   python3 src/cuts.py examples/transcript.example.json
   ```

![De una toma cruda a los archivos finales](docs/assets/01-pipeline.es.svg?v=3)

[PNG en alta resolución](docs/assets/01-pipeline.es.png?v=3) · [English version](README.md)

## Qué hace

| Paso | Qué pasa | Dónde corre |
|---|---|---|
| Cortes | silencios, muletillas y repeticiones inmediatas detectados con el tiempo de cada palabra; las tomas falladas las lee un asistente o una persona | CPU |
| Lista de cortes | cada corte con su motivo y tiempo, mostrada **antes** de renderizar | la aprueba una persona |
| Montaje | una sola pasada de FFmpeg desde el original, micro-fundidos en cada unión, volumen normalizado | GPU integrada / CPU |
| Aspecto | zoom y paneo sobre el cuadro 4K, fondo verde opcional, subtítulos opcionales | GPU integrada / CPU |
| Shorts | candidatos propuestos, una persona aprueba, reencuadre 9:16 que sigue la cara; versiones con y sin subtítulos | GPU integrada / CPU |

![Cómo se deciden los cortes](docs/assets/05-cuts.es.svg?v=3)

## Cuánto tarda (estimaciones)

Para un video de 30 minutos en el mini PC de referencia (4 núcleos / 8 hilos, 32 GB, GPU integrada, sin GPU dedicada): unas **1 h 25 min** de máquina sin supervisión (rango 55 min – 2 h 17 min) incluyendo cinco shorts en dos versiones, más unos 15 minutos de revisión humana. La transcripción y los shorts son lo que más pesa.

![Tiempo de máquina estimado](docs/assets/03-timing.es.svg?v=3)

Son **estimaciones, no mediciones**. [Cómo se arman, cómo cambiarlas y cómo medir las tuyas](docs/timing.md).

## Propuesta de hardware

Alcanza con una máquina Linux x86 chica; la GPU es una mejora opcional sólo si las mediciones la justifican.

![Hardware y red](docs/assets/02-hardware.es.svg?v=3)

Detalle, dimensionado de almacenamiento y camino de mejora: [docs/hardware.md](docs/hardware.md).

## Shorts y subtítulos

![Del video largo a los shorts](docs/assets/04-shorts.es.svg?v=3)

![Ubicación de los subtítulos](docs/assets/06-framing.es.svg?v=3)

## Modos de trabajo

Dos perfiles comparten el mismo pipeline: **prolijo** (contenido técnico: cortes ajustados, zooms, gráficos) y **casual** (espontáneo: sólo silencios largos y tropiezos). Ver [docs/modes.md](docs/modes.md).

## Software utilizado

FFmpeg (con Quick Sync/VAAPI), faster-whisper, auto-editor o `silencedetect` de FFmpeg, MediaPipe/OpenCV para el seguimiento de cara, Python 3.11+. Versiones, función y licencias: [docs/software.md](docs/software.md) y [NOTICE.md](NOTICE.md).

## Reglas de privacidad

- **La cara y la voz no salen de la máquina.** Nada de editores en la nube, transcripción en la nube ni subir videos a la nube.
- Sólo el **texto** de la transcripción puede leerlo un asistente de lenguaje; un modelo local es una opción.
- Este repositorio no incluye videos, muestras de voz ni imágenes de caras; las ilustraciones usan una silueta neutra.
- El pipeline nunca borra los originales.

## Colaboradores

El autor, con Claude, Codex y OpenRouter/OpenCode como asistentes de IA bajo revisión humana. Ver [CONTRIBUTORS.md](CONTRIBUTORS.md).

## Documentación

| Guía | English | Español |
|---|---|---|
| Arquitectura | [architecture.en.md](docs/architecture.en.md) | [architecture.md](docs/architecture.md) |
| Hardware | [hardware.en.md](docs/hardware.en.md) | [hardware.md](docs/hardware.md) |
| Estimaciones de tiempo | [timing.en.md](docs/timing.en.md) | [timing.md](docs/timing.md) |
| Modos de trabajo | [modes.en.md](docs/modes.en.md) | [modes.md](docs/modes.md) |
| Software | [software.en.md](docs/software.en.md) | [software.md](docs/software.md) |
| Limitaciones | [limitations.en.md](docs/limitations.en.md) | [limitations.md](docs/limitations.md) |

Relacionados: [ai-animated-shorts](https://github.com/marianoa73/ai-animated-shorts) (serie de diálogos animados, otro pipeline) · [ai-split-raspberry-pi](https://github.com/marianoa73/ai-split-raspberry-pi).
