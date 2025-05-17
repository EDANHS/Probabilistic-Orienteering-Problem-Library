from abc import ABC, abstractmethod
from pop.utils import POP_State
from pop.environment import AbstractEnvironment

class Agent(ABC):

    @abstractmethod
    def select_action(self, evals: list):
      pass

    @abstractmethod
    def eval_actions(self,
                     state: POP_State,
                     env: AbstractEnvironment,
                     shuffle: bool = False):
      pass

    def action_policy(self, 
                      state: POP_State, 
                      env: AbstractEnvironment):
      evals = self.eval_actions(state, env)
      if len(evals)==0: return None

      # Seleccionar la acción que maximiza su evaluación
      return self.select_action(evals)