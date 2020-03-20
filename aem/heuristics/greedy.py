from aem.heuristics.heuristic import Heuristic


class Greedy(Heuristic):
    def __init__(self, graph):
        super().__init__(graph)

    def build_cycle(self, start_vertex=0) -> list:
        cycle = [start_vertex]
        next_vertex = self.graph.get_closest_unvisited_neighbor_idx(from_vertex=cycle[-1], visited=cycle)
        cycle.append(next_vertex)
        while len(cycle) < 50:
            # for each vertex find two visited that are closest and compute insertion_cost
            min_insertion_cost = float('inf')
            min_cost_vertex = None
            min_insertion_position = None
            for i in range(self.graph.no_of_vertices()):
                if i not in cycle:
                    first_closest = self.graph.get_closest_visited_idx(from_vertex=i, visited=cycle)
                    insertion_cost, insertion_position = self.establish_insertion_cost(cycle, first_closest, i)
                    if insertion_cost < min_insertion_cost:
                        min_insertion_cost = insertion_cost
                        min_cost_vertex = i
                        min_insertion_position = insertion_position
            cycle.insert(min_insertion_position, min_cost_vertex)
        return cycle

    def establish_insertion_cost(self, cycle, first_closest, i):
        """We can insert it either on left or right side -> calculate costs"""
        left_idx = cycle.index(first_closest) - 1
        right_idx = cycle.index(first_closest) + 1
        cost_left, cost_right = float("inf"), float("inf")
        if 0 <= left_idx < len(cycle):
            left = cycle[left_idx]
            cost_left = self.graph.cost(first_closest, i) + self.graph.cost(i, left)

        if 0 <= right_idx < len(cycle):
            right = cycle[right_idx]
            cost_right = self.graph.cost(first_closest, i) + self.graph.cost(i, right)

        if cost_left < cost_right:
            insertion_cost = cost_left
            insertion_position = max(left_idx, cycle.index(first_closest))
        else:
            insertion_cost = cost_right
            insertion_position = max(right_idx, cycle.index(first_closest))

        return insertion_cost, insertion_position
