from concurrent.futures import ProcessPoolExecutor
from collections import namedtuple
from typing import Tuple, List
from typing import Callable
from pop.utils import POP_Instance, POP_State
from pop.utils import generate_POP_instance
from pop.utils.tools import build_global_vector, build_step_features, build_target_vector

POP_SolverType = Callable[['POP_Instance'], 'POP_State']
Args = namedtuple("Args", ["size", "max_coord", "max_prize", "solver_func"])

def process_solution(instance, final_state, max_coord, max_prize):
    X_data = []
    Y_data = []
    solution = final_state.visited

    for step in range(1, len(solution)):
        current_state = solution[:step]
        current_node = current_state[-1]
        visited = set(current_state)

        # Filtrar acciones posibles
        possible_actions = [
            node for node in instance.clients.keys()
            if node not in visited and node != instance.origin
        ]
        if not possible_actions:
            continue

        global_vector = build_global_vector(current_state, final_state, instance, max_coord)
        step_features = build_step_features(instance, visited, max_coord, max_prize)
        target = build_target_vector(solution[step], len(instance.clients))

        X_data.append((step_features, global_vector))
        Y_data.append(target)

    return X_data, Y_data

def generate_one_instance(args: Args) -> Tuple[List, List]:
    size, max_coord, max_prize, solver_func = args
    instance = generate_POP_instance(num_nodes=size,
                                     coord_range_max=max_coord,
                                     prize_max=max_prize)
    final_state = solver_func(instance)
    return process_solution(instance, final_state, max_coord, max_prize)

def generate_data_parallel(
    max_prize: int,
    max_coord: int,
    solver_func: POP_SolverType,
    size: int = 30,
    n_instances: int = 10,
    max_workers: int = None
) -> Tuple[List, List]:
    X_data = []
    Y_data = []

    args_list = [Args(size, max_coord, max_prize, solver_func) for _ in range(n_instances)]

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(generate_one_instance, args_list)

        for X_inst, Y_inst in results:
            X_data.extend(X_inst)
            Y_data.extend(Y_inst)

    return X_data, Y_data