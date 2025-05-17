from pop.environment import AbstractEnvironment
from pop.utils import POP_State
from itertools import combinations
from copy import deepcopy
import random

class POP_2_OPT_Environment(AbstractEnvironment):
    def __init__(self):
      super().__init__()

    def gen_actions(self,
                    state: POP_State,
                    shuffle: bool = False):
      n = len(state.visited)
      actions = [(i,j) for i, j in combinations(range(1, n - 1), 2)]

      if shuffle:
        random.shuffle(actions)

      for action in actions:
         yield action

    def state_transition(self,
                         state: POP_State,
                         action: tuple) -> POP_State:

      if state.is_complete:
        i, j = action
        state.visited[i:j] = reversed(state.visited[i:j])
      return state

    def calculate_cost_after_action(self, state: POP_State, action: tuple):

      state_copy = deepcopy(state)
      i, j = action
      state_copy.visited[i:j] = reversed(state.visited[i:j])

      new_cost = state_copy.calculate_prize()
      new_distance = state_copy.calculate_total_distance()

      return new_cost, new_distance