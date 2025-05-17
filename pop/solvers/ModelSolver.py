from copy import deepcopy
from pop.utils import POP_State
from pop.utils.tools import build_global_vector, build_step_features
from Solver import Solver
from keras.api.models import Model
import numpy as np
import tensorflow as tf

class ModelSolver(Solver):
    def __init__(self, 
                 model: Model, 
                 max_coord: float, 
                 max_prize: float):
        self.model = model
        self.max_coord = max_coord
        self.max_prize = max_prize

    def solve(self, 
              state: POP_State,
              **kwargs) -> POP_State:
        current_state = deepcopy(state)

        # Asegurar que el tour empiece por el nodo origen
        if not current_state.visited:
            current_state.visited.append(current_state.instance.origin)

        while True:
            if current_state.calculate_total_distance() > current_state.instance.d_max:
                print("Excedió d_max. Fin del recorrido.")
                break

            global_vector = build_global_vector(
                current_state.visited,
                current_state,
                current_state.instance,
                self.max_coord
            )

            step_features = build_step_features(
                current_state.instance,
                set(current_state.visited),
                self.max_coord,
                self.max_prize
            )

            input_seq = tf.convert_to_tensor([step_features], dtype=tf.float32)
            input_ctx = tf.convert_to_tensor([global_vector], dtype=tf.float32)

            probs = self.model([input_seq, input_ctx], training=False).numpy()[0]

            candidates = [
                i for i in np.argsort(probs)[::-1]
                if i not in current_state.visited and i != current_state.instance.origin
            ]

            added = False
            for node in candidates:
                simulated = deepcopy(current_state)
                simulated.visited.append(node)
                simulated.visited.append(current_state.instance.destination)

                total_d = simulated.calculate_total_distance()

                if total_d <= current_state.instance.d_max:
                    current_state.visited.append(node)
                    added = True
                    break

            if not added:
                current_state.visited.append(current_state.instance.destination)
                break

        return current_state