from aem.experiment_result import ExperimentResult


class Greedy:
    def __init__(self, graph):
        self.graph = graph

    def run(self) -> ExperimentResult:
        cycle = []
        start_vertex = 0
        cycle.append(start_vertex)
        closest_neighbor_idx = self.graph.get_closest_neighbor_index(start_vertex)
        cycle.append(closest_neighbor_idx)

        # now expand the cycle as long as len(cycle) < 50

        

        return ExperimentResult(0, 0, 0)

