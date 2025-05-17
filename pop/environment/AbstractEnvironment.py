from abc import ABC, abstractmethod
from pop.utils import POP_State

class AbstractEnvironment(ABC):

    @abstractmethod
    def gen_actions(self,
                    state: POP_State,
                    shuffle: bool = False) -> list:
        pass

    @abstractmethod
    def state_transition(self,
                         state: POP_State,
                         action: tuple) -> POP_State:
        pass