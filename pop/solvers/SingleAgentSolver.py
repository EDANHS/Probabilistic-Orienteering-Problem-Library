from copy import deepcopy
from pop.solvers.Solver import Solver
from pop.utils import POP_State

class SingleAgentSolver(Solver):
    def __init__(self, env, agent):
        self.env = env
        self.agent = agent

    def solve(self, state, **kwargs) -> POP_State:
        track_best_state = kwargs.get("track_best_state", True)
        max_iterations = kwargs.get("max_iterations", 1000)

        best_state = None
        if track_best_state:
            best_state = deepcopy(state)

        n_actions = 0
        while n_actions < max_iterations:
            action = self.agent.action_policy(state, self.env)
            if action is None:
                break
            state = self.env.state_transition(state, action)
            n_actions += 1

            if track_best_state and state.total_prize < best_state.total_prize:
                best_state = deepcopy(state)

        return best_state if track_best_state else state
