from pop.solvers.SingleAgentSolver import SingleAgentSolver
from pop.utils import POP_State
from pop.utils.tools import Perturbation
from pop.utils.tools import DefaultAcceptanceCriterion
from pop.solvers.Solver import Solver
from copy import deepcopy

class ILS(Solver):
  def __init__(self,
               local_search: SingleAgentSolver,
               perturbation: Perturbation,
               acceptance_criterion: DefaultAcceptanceCriterion = DefaultAcceptanceCriterion()):
    
    self.local_search = local_search
    self.perturbation = perturbation
    self.acceptance_criterion = acceptance_criterion

  def solve(self, 
            state,
            **kwargs) -> POP_State:
    
    max_iterations = kwargs.get("max_iterations", 1000)

    current_solution, *_ = self.local_search.solve(state)

    best_solution = deepcopy(current_solution)
    best_solution_cost = best_solution.total_prize
    best_distance = best_solution.calculate_total_distance()

    

    for i in range(max_iterations):
        # Perturb the current solution to escape local optima
        perturbed_solution = self.perturbation(deepcopy(current_solution))

        # Apply local search on the perturbed solution
        local_optimum = self.local_search.solve(perturbed_solution)
        cost = local_optimum.total_prize
        distance = local_optimum.calculate_total_distance()

        # Decide whether to accept the new solution
        if self.acceptance_criterion(best_solution_cost, cost):
            current_solution = deepcopy(local_optimum)
            if distance >= best_distance: continue
            if cost > best_solution_cost:
                best_solution = deepcopy(current_solution)
                best_solution_cost = cost
                best_distance = distance

    return best_solution