# Taller 2 — Simulador Adversario para la Copa Mundial de Fútbol

En este README encontrará **dónde está cada parte del proyecto**, qué carpetas debe modificar y cómo ejecutar el simulador. No es necesario revisar todo el código del motor: concéntrese en `src/algorithms/` y en los escenarios YAML que cree o edite en `assets/scenarios/`.

El desempeño de los agentes depende mucho de su `evaluation_function`. Pruebe varias combinaciones de agente, profundidad e iteraciones; lo importante es poder explicar por qué un algoritmo rinde mejor o peor en cada situación.

## Estructura del proyecto

```
T2_AdversarialSoccer/
├── requirements.txt             # Dependencias Python
├── assets/
│   ├── scenarios/               # Escenarios YAML (incluidos y propios)
│   └── ui/
│       └── replay_template.html # Plantilla HTML del replay
└── src/
    ├── main.py                  # Punto de entrada CLI
    ├── paths.py                 # Rutas a assets y al proyecto
    ├── algorithms/              # ★ Su entrega — implemente aquí
    ├── engine/                  # Motor del juego (no modificar)
    └── ui/                      # Consola y replay (no modificar)
```

## Dónde encontrar cada cosa

### `assets/scenarios/` — Configuración de partidos

Archivos YAML con la formación inicial, tamaño del campo, posesión y límites de turnos. El motor carga escenarios por nombre de archivo (sin extensión `.yaml`). Puede crear escenarios propios en esta carpeta para sus experimentos.

Claves habituales de un YAML:

| Clave | Descripción |
|-------|-------------|
| `size` | `[ancho, alto]` del campo |
| `max_shot_distance` | Distancia Manhattan máxima para tiro o pase |
| `max_turns` | Límite de turnos (opcional) |
| `colombia` / `rival` | Listas de posiciones `[x, y]` |
| `possession` | `colombia` o `rival` — equipo con el balón al inicio |
| `ball_owner` | Índice del jugador con balón en esa lista |

### `src/algorithms/` — Código a implementar

Organizado por algoritmo. Los agentes (`*/agent.py`) ya están conectados al motor; implemente la lógica de búsqueda en los archivos indicados.

| Ruta | Punto del taller | Qué implementar |
|------|------------------|-----------------|
| `base/evaluation.py` | Punto 1 | `evaluation_function(state)` |
| `minimax/search.py` | Punto 2a | `minimax_search` |
| `alphabeta/search.py` | Punto 2b | `alphabeta_search` |
| `expectimax/search.py` | Punto 3 | `expectimax_search` |
| `mcts/uct.py` | Punto 4a | `uct_score` |
| `mcts/search.py` | Punto 4b | `mcts_search` |

Código compartido (de consulta, no es el foco de la entrega):

| Ruta | Contenido |
|------|-----------|
| `base/search.py` | Helpers de búsqueda (`legal_actions`, `is_cutoff`, `pick_rival_action`, …) |
| `base/agent.py` | Clases base de agentes y contrato `decide_turn` |
| `base/metrics.py` | Métricas de nodos expandidos |
| `__init__.py` | Registro de agentes y `create_agent` |

Agentes disponibles en CLI: `MinimaxAgent`, `AlphaBetaAgent`, `ExpectimaxAgent`, `MCTSAgent`, `RandomAgent`.

### `src/engine/` — Motor del juego (solo lectura)

| Carpeta / archivo | Contenido |
|-------------------|-----------|
| `model/` | Tipos base: posiciones, equipos, direcciones, acciones joint |
| `scenario/` | Carga y validación de YAML desde `assets/scenarios/` |
| `geometry/` | Distancias, movimiento en grilla, líneas de tiro |
| `state/` | `GameState` — snapshot del partido en un turno |
| `agent/` | Contrato del agente (`Agent`, `TurnDecision`) |
| `rules/` | Reglas: movimiento, tiros, acciones legales, `step(...)` |
| `runner.py` | Bucle del partido; llama al agente cada turno |

### `src/ui/` — Visualización (solo lectura)

| Archivo | Contenido |
|---------|-----------|
| `console.py` | Progreso, métricas y resumen en terminal |
| `replay.py` | Genera `soccer_replay.html` al terminar el partido |

La plantilla del replay está en `assets/ui/replay_template.html`.

### `src/main.py` — Ejecución

Punto de entrada. Parsea argumentos, carga el escenario, instancia el agente y corre un partido.

## Ejecución

Desde la carpeta del proyecto:

```bash
python src/main.py -a AGENTE -s ESCENARIO [OPCIONES]
```

| Opción | Descripción | Ejemplo |
|--------|-------------|---------|
| `-a` / `--agent` | Agente tomador de decisión | `-a MinimaxAgent` |
| `-s` / `--scenario` | Escenario YAML (sin `.yaml`) | `-s 1v1_anticipation_block` |
| `-d` / `--depth` | Profundidad (Minimax, AlphaBeta, Expectimax) | `-d 3` |
| `-p` / `--probability` | Prob. de acción aleatoria del rival (`0` = greedy) | `-p 0.2` |
| `-i` / `--iterations` | Iteraciones MCTS (no usa `-d`) | `-i 300` |
| `-r` / `--random-seed` | Semilla para reproducibilidad | `-r 42` |
| `--help` | Ayuda completa | `--help` |

Verificación rápida:

```bash
python src/main.py -a RandomAgent -s 1v1_anticipation_block
```

Ejemplos por algoritmo (sustituya `ESCENARIO` por cualquier YAML en `assets/scenarios/`):

```bash
# Punto 1 + 2 — evaluación + Minimax / Alpha-Beta
python src/main.py -a MinimaxAgent -s ESCENARIO -d 2
python src/main.py -a AlphaBetaAgent -s ESCENARIO -d 2

# Punto 3 — Expectimax
python src/main.py -a ExpectimaxAgent -s ESCENARIO -d 1 -p 0.3

# Punto 4 — MCTS
python src/main.py -a MCTSAgent -s ESCENARIO -i 300
python src/main.py -a MCTSAgent -s ESCENARIO -i 400 -p 0.2
```

Al finalizar, se genera `soccer_replay.html` en el directorio desde el que ejecutó el comando.

## Dependencias

```bash
pip install -r requirements.txt
```

