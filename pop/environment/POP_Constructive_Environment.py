from pop.environment import AbstractEnvironment
from pop.utils import POP_State

import random

class POP_Constructive_Environment(AbstractEnvironment):

    def gen_actions(self,
                    state: POP_State,
                    shuffle: bool = False):
        actions = [(not_visited, not_visited) for not_visited in state.not_visited]

        if shuffle:
            random.shuffle(actions)

        for action in actions:
            yield action


    def state_transition(self,
                         state: POP_State,
                         action: tuple) -> POP_State:

        if action is None or action[1] == state.destination:
            state.visited.append(state.destination)
            state.not_visited.discard(state.destination)
            state.is_complete = True
            return state

        if not state.is_complete:
            state.visited.append(action[1])
            state.not_visited.remove(action[1])
            state.update_prize()

        return state