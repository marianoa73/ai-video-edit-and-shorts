# Limitaciones

[English version](limitations.en.md)

- **Todavía no hay nada medido.** Cada tiempo es una estimación; el primer prototipo con un clip real de 2–3 minutos las reemplaza.
- **Las tomas falladas requieren criterio.** La herramienta corta silencios, muletillas y repeticiones inmediatas. Elegir la mejor de varias tomas lo hace un asistente o una persona leyendo la transcripción.
- **El video HDR del celular** debe pasarse a SDR con un mapeo de tonos correcto o los colores salen lavados. El mapeo de tonos por software es lento y no está en la estimación base.
- **El fondo verde** necesita luz pareja y nada verde en la ropa. Sin él, quitar el fondo por segmentación queda peor.
- **El seguimiento de cara** puede perder a la persona si sale del cuadro o gira; el recorte mantiene entonces su última posición.
- **La precisión de Whisper** depende de la calidad del audio, el acento y el vocabulario técnico; revisá la transcripción en nombres y términos.
- **Sin GPU**, la transcripción y la codificación son lo lento en esta clase de hardware.
- **Una persona, una cámara.** La edición multicámara y varias voces quedan fuera de alcance.
- **Las reglas de las plataformas cambian.** Las zonas seguras y los largos de los shorts son recomendaciones; verificá las reglas vigentes.
