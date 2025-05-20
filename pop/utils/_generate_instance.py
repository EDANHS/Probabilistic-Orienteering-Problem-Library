from pop.utils import POP_Instance

import random
import numpy as np

def generate_POP_instance(
    num_nodes=50,
    coord_range_min=0,
    coord_range_max=1000,       # Mayor dispersión espacial
    prize_min=500.0,
    prize_max=1500.0,
    pi_low=0.01,
    pi_high=1.0,
    fraction_low_pi=0.7,        # Mayor mezcla
    d_max_factor=0.4,           # Mucho más restrictivo
    seed=None,
    max_attempts=20
) -> POP_Instance:
    for attempt in range(max_attempts):
        if seed is not None:
            random.seed(seed + attempt)
            np.random.seed(seed + attempt)

        x = np.random.randint(coord_range_min, coord_range_max, size=num_nodes).tolist()
        y = np.random.randint(coord_range_min, coord_range_max, size=num_nodes).tolist()
        prizes = np.random.uniform(prize_min, prize_max, size=num_nodes).tolist()

        pis = [
            round(np.random.uniform(pi_low, pi_high), 2) if random.random() < fraction_low_pi else 1.0
            for _ in range(num_nodes)
        ]

        origin = destination = 0 #sdsd
        #destination = random.randint(0, num_nodes - 1)

        prizes[origin] = 0.0
        pis[origin] = 1.0
        prizes[destination] = 0.0
        pis[destination] = 1.0

        temp_instance = POP_Instance(x=x, y=y, prizes=prizes, pis=pis,
                                     d_max=float('inf'), origin=origin, destination=destination)

        dist_list = [
            temp_instance.distance_matrix[i][j]
            for i in range(num_nodes) for j in range(i + 1, num_nodes)
        ]
        dist_list.sort()

        approx_full_tour = sum(dist_list[:num_nodes])
        d_max = int(approx_full_tour * d_max_factor)

        # Validaciones de instancia difícil
        if d_max <= 0:
            continue

        if pis.count(1.0) < num_nodes * 0.2:  # Al menos 20% de nodos con penalización dura
            continue

        if np.mean(prizes) < (prize_max * 0.6):  # Premios suficientemente atractivos
            continue

        return POP_Instance(x=x, y=y, prizes=prizes, pis=pis,
                            d_max=d_max, origin=origin, destination=destination)

    raise ValueError("No se pudo generar una instancia NP-Hard válida en los intentos permitidos.")