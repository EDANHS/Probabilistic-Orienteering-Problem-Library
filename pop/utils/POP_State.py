from pop.utils import POP_Instance

class POP_State():
    def __init__(self,
                  instance: POP_Instance,
                  visited: list[int],
                  destination: int):
        self.instance = instance
        self.visited = visited
        self.total_prize = self.calculate_prize()

        self.not_visited = set(range(len(self.instance.distance_matrix))) - set(self.visited)
        self.not_visited.add(self.visited[0])
        self.d_left = self.calculate_d_left()
        self.destination = destination
        self.is_complete = self.visited[:-1] == destination

    def calculate_prize(self):
        total_prize = 0
        for node in self.visited:
            prize = self.instance.clients[node].prize
            probability = self.instance.clients[node].pi
            total_prize += prize * probability
        return total_prize - self.instance.C * self.calculate_total_distance()

    def calculate_total_distance(self):
        return sum(
            self.instance.distance_matrix[self.visited[i]][self.visited[i + 1]]
            for i in range(len(self.visited) - 1)
        )

    def calculate_d_left(self):
        return self.instance.d_max - sum([self.instance.distance_matrix[client][client - 1] for client in range(len(self.visited) - 1)])

    def update_prize(self):
        self.total_prize = self.calculate_prize()

    def __str__(self):
        tour_str = "->".join(map(str, self.visited))
        return f"\nTour actual: {tour_str}\nPremio total: {self.calculate_prize()}\nDistancia total: {self.calculate_total_distance()}"