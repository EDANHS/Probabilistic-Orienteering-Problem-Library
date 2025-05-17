from pop.utils import POP_State

import numpy as np
import matplotlib.pyplot as plt

def plot_points_with_connections(points: np.ndarray, 
                                 indices: list, 
                                 non_crossing_indices: list, 
                                 solution: POP_State, 
                                 show_index=True):
    points = np.column_stack(points)  # Asegurar que sea un array de NumPy

    # Extraer coordenadas de los puntos en el orden indicado por indices
    x_coords = points[indices, 0]
    y_coords = points[indices, 1]

    plt.figure(figsize=(8, 6))

    # Dibujar todos los puntos de indices con marcador
    plt.scatter(x_coords, y_coords, color='blue', s=50, label='Puntos en Índices')

    # Dibujar las conexiones entre los puntos en indices
    plt.plot(x_coords, y_coords, marker='o', linestyle='-', color='b', markersize=5, label='Conexión principal')

    # Resaltar el primer y último punto
    plt.scatter(x_coords[0], y_coords[0], color='red', s=100, label='Inicio')
    plt.scatter(x_coords[-1], y_coords[-1], color='green', s=100, label='Fin')

    # Dibujar los puntos de non_crossing_indices en otro color
    if len(non_crossing_indices) > 0:
        non_crossing_coords = points[non_crossing_indices]
        plt.scatter(non_crossing_coords[:, 0], non_crossing_coords[:, 1], color='orange', s=80, label='Clientes no cruzados')

    if show_index:
      # Agregar los números de los puntos en indices encima de cada punto
      for i, idx in enumerate(indices):
          plt.text(x_coords[i], y_coords[i] + 0.2, str(idx), fontsize=10, ha='center', color='black')

    plt.text(0.01, 0.99, f"Distancia total: {solution.calculate_total_distance():.2f}",
                 transform=plt.gca().transAxes, fontsize=12,
                 verticalalignment='top', color='black')
    
    plt.text(0.01, 0.95, f"Recompensa total: {solution.calculate_prize():.2f}",
                 transform=plt.gca().transAxes, fontsize=12,
                 verticalalignment='top', color='black')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Solución encontrada del POP')
    plt.legend()
    plt.grid(True)
    plt.show()

