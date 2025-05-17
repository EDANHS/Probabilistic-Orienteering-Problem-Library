import random

from pop.utils import POP_State
from pop.environment import AbstractEnvironment
from pop.agents import Agent

class GreedyStochasticAgent(Agent):
    def __init__(self, k: int = 3, seed: int = None):
        self.k = k
        self.seed = seed
        if seed is not None:
            random.seed(seed)

    def eval_actions(self,
                     state: POP_State,
                     env: AbstractEnvironment,
                     shuffle: bool = False):
        evals = []
        ultima_ciudad = state.visited[-1] if state.visited else state.instance.origin
        d_actual = state.calculate_total_distance()
        d_max = state.instance.d_max

        for action in env.gen_actions(state, shuffle):
            cliente = action[1]

            if cliente in state.visited:
                continue

            d_cliente = state.instance.distance_matrix[ultima_ciudad][cliente]
            d_destino = state.instance.distance_matrix[cliente][state.destination]
            total_d = d_actual + d_cliente + d_destino

            if total_d <= d_max:
                nodo = state.instance.clients[cliente]
                score = (nodo.prize * nodo.pi) / d_cliente if d_cliente > 0 else 0
                evals.append((action, score))

        return evals

    def select_action(self, evals):
        if not evals:
            return None

        # Ordenar por score descendente y tomar los k mejores
        evals.sort(key=lambda x: x[1], reverse=True)
        top_k = evals[:min(self.k, len(evals))]

        # Selección estocástica ponderada por el score
        scores = [e[1] for e in top_k]
        total_score = sum(scores)

        if total_score == 0:
            return random.choice(top_k)[0]

        probabilidades = [s / total_score for s in scores]
        seleccion_idx = random.choices(range(len(top_k)), weights=probabilidades, k=1)[0]

        return top_k[seleccion_idx][0]
