from pop.utils import Node
import numpy as np
import math

class POP_Instance():
    def __init__(self,
                x: list[int],
                y: list[int],
                prizes: list[float],
                pis: list[float],
                d_max: float,
                origin: int,
                destination: int,
                C = 1.0):
        
        self.coord_x = x
        self.coord_y = y

        #Estructura para almacenar los nodos
        self.clients: dict[int, Node] = {
            client: Node(x=x[client], y=y[client], prize=prizes[client], pi=pis[client])
            for client in range(len(x))
        }
        self.d_max = d_max
        self.origin = origin
        self.destination = destination
        self.distance_matrix = self.compute_distance_matrix()
        self.C = C

    def compute_distance_matrix(self) -> np.ndarray:
        #Calcula la matriz de distancias entre cada par de clientes.
        num_clients = len(self.clients)
        distance_matrix = np.zeros((num_clients, num_clients))

        for i in range(num_clients):
            for j in range(num_clients):
                if i != j:
                    node_i = self.clients[i]
                    node_j = self.clients[j]
                    #Verificar luego si la distancia debe aproximarse o dejarse decimal
                    distance_matrix[i][j] = int(math.sqrt((node_i.x - node_j.x) ** 2 + (node_i.y - node_j.y) ** 2))

        return distance_matrix