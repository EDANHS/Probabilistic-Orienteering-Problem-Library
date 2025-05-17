from pop.environment import AbstractEnvironment
from pop.utils import POP_State
from Solver import Solver
from copy import deepcopy

class TabuSearchAgent(Solver):
  def __init__(self, 
               environment: AbstractEnvironment, 
               tabu_maxsize: int = 10, 
               neighborhood_size: int = 30, 
               max_iter: int = 100, 
               iter: int = 0):
    # Inicializa los parámetros del agente
    self.environment = environment  
    self.tabu_maxsize = tabu_maxsize  
    self.iter = iter  
    self.max_iter = max_iter  
    self.neighborhood_size = neighborhood_size 
    self.tabu_list = [] 

  def __reset(self):
    # Reinicia la búsqueda (vacía la lista tabú y el contador de iteraciones)
    self.tabu_list.clear()
    self.iter = 0

  def __action_policy(self, 
                    state: POP_State, environment):
    # Política de selección de la mejor acción (movimiento) en la vecindad actual
    best_score = float('-inf') 
    best_action = None 
    actions = list(self.environment.gen_actions(state, shuffle=True)) 

    # Explora los primeros N vecinos
    for action in actions[:self.neighborhood_size]:
      if action in self.tabu_list: continue  # Ignora si el movimiento está en la lista tabú

      # Simula el estado resultante de aplicar la acción
      state_copy = deepcopy(state)
      new_state = self.environment.state_transition(state_copy, action)

      # Verifica que la distancia no exceda el límite máximo
      if new_state.calculate_total_distance() > state.instance.d_max: continue

      # Evalúa el nuevo estado basado en el premio total (ya incluye penalización por distancia)
      score = new_state.total_prize
      if score > best_score:
        best_score = score
        best_action = action

    return best_action

  def solve(self, 
            initial_state: POP_State,
            **kwargs) -> POP_State:
    current_state = initial_state
    best_state = deepcopy(initial_state)

    self.__reset()

    while self.iter < self.max_iter:
        action = self.__action_policy(current_state, self.environment)
        if action is None:
            break

        new_state = self.environment.state_transition(current_state, action)

        if new_state.total_prize > best_state.total_prize:
            best_state = deepcopy(new_state)

        self.tabu_list.append(action)
        self.tabu_list = self.tabu_list[-self.tabu_maxsize:]

        current_state = new_state
        self.iter += 1

    return best_state
