from pop.environment import AbstractEnvironment
from pop.utils import POP_State
from copy import deepcopy
import random

class POP_Replacement_Swap_Environment(AbstractEnvironment):
    def __init__(self):
        super().__init__()

    def gen_actions(self, state: POP_State, shuffle: bool = False):

        n = len(state.visited)
        m = len(state.not_visited)
        actions = [(i, j) for i in range(1, n-1) for j in range(m)]
        if shuffle:
            random.shuffle(actions)

        for action in actions:
            yield action

    def state_transition(self, state: POP_State, action: tuple) -> POP_State:

        i, j = action
        # Obtener el elemento de not_visited convirtiéndolo en lista temporalmente
        not_visited_list = list(state.not_visited)
        elem_j = not_visited_list[j]  # Obtener el elemento en la posición j

        # Hacer el intercambio correctamente
        state.not_visited.remove(elem_j)  # Eliminar el elemento del set
        state.not_visited.add(state.visited[i])  # Mover el elemento de visited a not_visited

        state.visited[i] = elem_j  # Mover el elemento de not_visited a visited

        state.update_prize()
        return state

    def calculate_cost_after_action(self, state: POP_State, action: tuple):
        state_copy = deepcopy(state)

        i, j = action
        # Obtener el elemento de not_visited convirtiéndolo en lista temporalmente
        not_visited_list = list(state_copy.not_visited)
        elem_j = not_visited_list[j]  # Obtener el elemento en la posición j

        # Hacer el intercambio correctamente
        state_copy.not_visited.remove(elem_j)  # Eliminar el elemento del set
        state_copy.not_visited.add(state_copy.visited[i])  # Mover el elemento de visited a not_visited

        state_copy.visited[i] = elem_j  # Mover el elemento de not_visited a visited

        new_prize = state_copy.calculate_prize()
        new_distance = state_copy.calculate_total_distance()
        return new_prize, new_distance
