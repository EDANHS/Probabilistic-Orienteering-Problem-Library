from itertools import combinations
from pop.utils import POP_State
from pop.environment import AbstractEnvironment
from copy import deepcopy
import random

class POP_3_OPT_Environment(AbstractEnvironment):

    def gen_actions(self, state: POP_State, shuffle: bool = False):
        n = len(state.visited)
        # Generar todas las combinaciones posibles de 3 índices
        actions = [(i, j, k) for i, j, k in combinations(range(1, n - 1), 3) if i < j < k]

        if shuffle:
            random.shuffle(actions)

        for action in actions:
            yield action

    def state_transition(self, state: POP_State, action: tuple) -> POP_State:
        if state.is_complete:
            i, j, k = action
            state.visited = self._best_3opt_variant(state, i, j, k)
        return state

    def calculate_cost_after_action(self, state: POP_State, action: tuple):
        state_copy = deepcopy(state)
        i, j, k = action
        state_copy.visited = self._best_3opt_variant(state, i, j, k)

        new_cost = state_copy.calculate_prize()
        new_distance = state_copy.calculate_total_distance()
        return new_cost, new_distance

    def _best_3opt_variant(self, state, i, j, k):
        A, B, C, D = state.visited[:i], state.visited[i:j], state.visited[j:k], state.visited[k:]
        variants = [
            A + B + C + D,                # No change
            A + B[::-1] + C + D,          # Reverse B
            A + B + C[::-1] + D,          # Reverse C
            A + B[::-1] + C[::-1] + D,    # Reverse B and C
            A + C + B + D,                # Swap B and C
            A + C[::-1] + B + D,          # Reverse C then swap
            A + C + B[::-1] + D,          # Reverse B then swap
            A + C[::-1] + B[::-1] + D,    # Reverse both then swap
        ]

        # Filtramos los que cambian origen o destino
        valid_variants = [r for r in variants if r[0] == state.visited[0] and r[-1] == state.visited[-1]]

        # Elegimos el que dé mejor recompensa (mayor prize)
        best_variant = max(valid_variants, key=lambda r: self._temp_eval(r, state.instance, state.destination))
        return best_variant

    def _temp_eval(self, route, instance, destination):
        temp_state = POP_State(instance=instance, visited=route, destination=destination)
        return temp_state.calculate_prize()