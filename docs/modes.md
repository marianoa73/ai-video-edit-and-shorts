# Modos de trabajo

[English version](modes.en.md)

## Dos perfiles, un pipeline

| | **Prolijo** | **Casual** |
|---|---|---|
| Uso típico | charlas técnicas, explicaciones | videos espontáneos, caseros |
| Silencios | se cortan desde 0,6 s (el valor por defecto de la herramienta) | sólo desde 1,2 s |
| Muletillas y repeticiones | se sacan | sólo tropiezos evidentes |
| Tomas falladas | se queda la mejor | se queda la mejor |
| Zoom / paneo | énfasis en frases clave, nunca dos seguidos | ninguno o un zoom lento |
| Subtítulos en el video largo | sólo si se piden | no |
| Fondo | fondo verde o liso, si se grabó para eso | el original |

Los perfiles son simples ajustes (umbrales e interruptores), no código distinto. Se afinan con el primer video real de cada tipo.

## Reglas de salida

- Video largo: 1080p, sin subtítulos impresos salvo pedido.
- Shorts: dos archivos del mismo corte, **sin** subtítulos (plataformas que ponen los suyos) y **con** subtítulos.
- Subtítulos: a la altura del pecho, 2 líneas como máximo, negrita con contorno, la palabra activa en el color de acento, dentro de las zonas seguras de cada plataforma.

## Ritmo

Un video largo por semana y uno o dos shorts por día sacados de él. Con las estimaciones de [tiempos](timing.md) alcanza con una noche de fin de semana de máquina; el límite es el tiempo que necesita una persona para aprobar.

## Una sesión, paso a paso

```bash
python3 src/estimate.py 30 --shorts 5      # saber el costo antes de empezar
python3 src/cuts.py transcript.json > cuts.json
# revisar cuts.json, editarlo, aprobar y recién ahí renderizar
```
