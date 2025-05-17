from pop.utils.environments import AbstractEnvironment
from pop.utils import POP_State

class Perturbation:
    def __init__(self, 
                 env: AbstractEnvironment, 
                 pert_size: int = 3):
        self.pert_size = pert_size
        self.env = env

    def __call__(self, state: POP_State):
        for _ in range(self.pert_size):
          action = next(self.env.gen_actions(state, shuffle=True))
          self.env.state_transition(state,action)
        return state