from abc import ABC, abstractmethod
from pop.utils import POP_State

class Solver(ABC):
    @abstractmethod
    def solve(self, 
              state: POP_State,
              **kwargs) -> POP_State:
        pass