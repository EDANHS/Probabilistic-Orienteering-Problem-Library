from pop.agents import Agent
from pop.utils import POP_State
from pop.environment import AbstractEnvironment

class LocalSearchAgent(Agent):
    def __init__(self, first_improvement=True):
        self.first_improvement = first_improvement

    def eval_actions(self, 
                     state: POP_State, 
                     env: AbstractEnvironment):
        current_prize=state.calculate_prize()
        current_distance=state.calculate_total_distance()
        evals = []
        for action in env.gen_actions(state, shuffle=True):
            new_prize, new_distance = env.calculate_cost_after_action(state=state, action=action)
            if new_distance > current_distance: continue
            if new_prize > current_prize:
              evals.append((action, new_prize))
              if self.first_improvement: return evals

        return evals

    def select_action(self, evals):
      #selecciona acción con máxima evaluación
      return max(evals, key=lambda x: x[1])[0]

    def __deepcopy__(self, memo):
        # Crear una nueva instancia de la clase
        new_instance = type(self)(
            action_type=self.action_type,
            first_improvement=self.first_improvement
        )
        return new_instance