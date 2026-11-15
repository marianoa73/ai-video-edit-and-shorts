# Software utilizado

[English version](software.en.md)

| Función | Herramienta | Notas |
|---|---|---|
| Decodificar, cortar, zoom, croma, subtítulos, codificar | FFmpeg | Quick Sync / VAAPI para H.264 y HEVC; `silencedetect`, `loudnorm`, `afftdn` y `chromakey` vienen incluidos |
| Transcripción | faster-whisper (CTranslate2) | tiempo por palabra, int8 en CPU, modelos small / medium / large-v3 |
| Corte de silencios | auto-editor o `silencedetect` de FFmpeg | el `src/cuts.py` incluido trabaja desde la transcripción |
| Seguimiento de cara | MediaPipe u OpenCV | muestreado a pocos cuadros por segundo; guía el zoom y el recorte 9:16 |
| Orquestación | Python 3.11+, shell | un trabajador, baja prioridad |
| Lectura de la transcripción | cualquier asistente de lenguaje | sólo texto; es posible un modelo local con Ollama |
| Acceso al hardware | driver de medios de Intel, libva | da Quick Sync en Linux |
| Carpeta compartida | Samba o similar, red privada | entrada y salida |

## Por qué estas elecciones

Todo corre sin conexión una vez descargados los modelos, tiene una licencia permisiva o bien conocida y se puede automatizar. Se descartaron los editores que suben el material porque la cara y la voz son datos personales.

## Licencias

Este repositorio es MIT. Las herramientas de terceros conservan sus licencias; ver [NOTICE.md](../NOTICE.md). FFmpeg es LGPL o GPL según la compilación, y libx264 trae obligaciones GPL si redistribuís binarios.
