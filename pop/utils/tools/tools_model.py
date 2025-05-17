from pop.utils import POP_State
from pop.utils import POP_Instance

def build_global_vector(current_state: POP_State, 
                        final_state: POP_State, 
                        instance: POP_Instance, 
                        max_coord: float):
    total_distance = sum(
        instance.distance_matrix[current_state[i]][current_state[i + 1]]
        for i in range(len(current_state) - 1)
    )
    distance_percentage = float(total_distance / instance.d_max)

    starting_node = instance.clients[current_state[0]]
    final_node = instance.clients[final_state.visited[-1]]

    return [
        distance_percentage,
        starting_node.x / max_coord, starting_node.y / max_coord,
        final_node.x / max_coord, final_node.y / max_coord,
    ]

def build_target_vector(chosen_action, size):
    return [1.0 if i == chosen_action else 0.0 for i in range(size)]

def build_step_features(instance: POP_Instance, 
                        visited: list, 
                        max_coord: float, 
                        max_prize: float):
    features = []
    for node_id, node in instance.clients.items():
        features.append([
            node.x / max_coord,
            node.y / max_coord,
            node.prize / max_prize,
            node.pi,
            1.0 if node_id in visited else 0.0
        ])
    return features