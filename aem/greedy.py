from aem.experiment_result import ExperimentResult
import numpy as np


class Greedy:
    def __init__(self, graph):
        self.graph = graph

    def build_cycle(self, start_vertex=0) -> list:
        cycle = [start_vertex]
        while len(cycle) < 50:
            next_closest = self.graph.get_closest_unvisited_neighbor_index(cycle)
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
        best_cycle_idx = int(np.argmin(lengths))

        return ExperimentResult(average_len=np.mean(lengths),
                                min_len=np.min(lengths),
                                max_len=np.max(lengths),
                                best_cycle=cycles[best_cycle_idx],
                                method_classname=self.__class__.__name__)

