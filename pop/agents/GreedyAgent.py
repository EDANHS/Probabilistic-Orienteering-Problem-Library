from pop.utils import POP_State
from pop.environment import AbstractEnvironment
from pop.agents import Agent

class GreedyAgent(Agent):
    def eval_actions(self, 
                     state: POP_State, 
                     env: AbstractEnvironment, shuffle: bool = False):
        evals = []
        for action in env.gen_actions(state, shuffle):
            ultima_ciudad = state.visited[-1] if state.visited else 0
            # Exclusión de acción en caso de que el destino exceda la distancia máxima
            if action[1] == state.destination:
                if state.calculate_total_distance() + state.instance.distance_matrix[ultima_ciudad][action[1]] >= state.instance.d_max: continue
            elif state.calculate_total_distance() + state.instance.distance_matrix[ultima_ciudad][action[1]] + state.instance.distance_matrix[action[1]][state.instance.destination] >= state.instance.d_max: continue

            eval = state.instance.clients[action[1]].pi * state.instance.clients[action[1]].prize
            evals.append((action,eval))

        return evals

    def select_action(self, evals):
        #selecciona acción con máxima evaluación
        return max(evals, key=lambda x: x[1])[0]