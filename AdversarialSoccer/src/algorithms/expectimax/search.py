# ==========================
# VERSIÓN Inicial
# ==========================
#
# best_action = None
# best_reply = None
# best_value = float("-inf")
#
# for colombia_action in colombia_actions:
#
#     worst_value = float("inf")
#     worst_reply = None
#     total = 0
#
#     for rival_action in rival_actions:
#
#         successor = step(state, colombia_action, rival_action)
#         value = ply(successor, depth - 1)[2]
#
#         total += value
#
#         if value < worst_value:
#             worst_value = value
#             worst_reply = rival_action
#
#     expected = (1 - prob) * worst_value + prob * total
#
#     if expected > best_value:
#         best_value = expected
#         best_action = colombia_action
#         best_reply = worst_reply
#
# return best_action, best_reply, best_value
#Implementé Expectimax, pero creo que el cálculo del valor esperado está mal.
#Quiero mantener la estructura general del algoritmo.
#¿Puedes revisar únicamente la parte donde calculo el nodo de expectativa y decirme qué errores hay? No cambies el resto del código si no es necesario.

from __future__ import annotations

import random
from collections.abc import Callable

from algorithms.base import EvaluationFunction
from algorithms.base.search import finish_search_root, is_cutoff, legal_actions
from engine.model import Team, TeamAction
from engine.rules import step
from engine.state import GameState


def expectimax_search(
    state: GameState,
    depth: int,
    evaluation_function: EvaluationFunction,
    rng: random.Random,
    *,
    prob: float = 0.0,
    on_expand: Callable[[], None] | None = None,
) -> tuple[TeamAction, TeamAction, float]:

    def ply(
        state: GameState,
        depth: int,
    ) -> tuple[TeamAction | None, TeamAction | None, float]:

        if on_expand is not None:
            on_expand()

        if is_cutoff(state, depth):
            return None, None, evaluation_function(state)

        colombia_actions = legal_actions(state, Team.COLOMBIA)
        rival_actions = legal_actions(state, Team.RIVAL)

        mejor_accion = None
        mejor_respuesta = None
        mejor_valor = float("-inf")

        for colombia_action in colombia_actions:

            suma = 0.0
            peor_valor = float("inf")
            peor_respuesta = None

            for rival_action in rival_actions:

                sucesor = step(state, colombia_action, rival_action)
                valor = ply(sucesor, depth - 1)[2]

                suma += valor

                if valor < peor_valor:
                    peor_valor = valor
                    peor_respuesta = rival_action

            promedio = suma / len(rival_actions)

            esperado = (1 - prob) * peor_valor + prob * promedio

            if esperado > mejor_valor:
                mejor_valor = esperado
                mejor_accion = colombia_action
                mejor_respuesta = peor_respuesta

        return mejor_accion, mejor_respuesta, mejor_valor

    return finish_search_root(*ply(state, depth))