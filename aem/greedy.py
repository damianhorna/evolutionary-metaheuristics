from aem.experiment_result import ExperimentResult
import numpy as np


class Greedy:
    def __init__(self, graph):
        self.graph = graph

    def build_cycle(self, start_vertex=0) -> list:
        cycle = [start_vertex]
        while len(cycle) < 50:
            next_closest = self.graph.get_closest_neighbor_index(cycle[-1])
            cycle.append(next_closest)
        return cycle

    def run(self) -> ExperimentResult:
        cycles = []
        for i in range(0, self.graph.no_of_vertices()):
            cycle = self.build_cycle(start_vertex=i)
            cycles.append(cycle)

        lengths = []
        for c in cycles:
            c_length = self.graph.compute_cycle_length(c)
            lengths.append(c_length)

        lengths = np.array(lengths)

        return ExperimentResult(np.mean(lengths), np.min(lengths), np.max(lengths), self.__class__.__name__)

