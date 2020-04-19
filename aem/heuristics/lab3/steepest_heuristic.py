import itertools

from aem.heuristics.heuristic import Heuristic
from aem.heuristics.random import Random
from aem.shared.experiment_result import ExperimentResult
import numpy as np
import time

from aem.utils.plot_util import PlotUtil


class SteepestHeuristic(Heuristic):
    def __init__(self, graph):
        super().__init__(graph)

    def alter_cycle(self, cycle, actions):
        pass

    def run(self, seed=None, number_of_experiments=1) -> ExperimentResult:
        if seed:
            np.random.seed(seed)
        start_cycles = []
        for i in range(number_of_experiments):
            start_cycles.append(Random(self.graph).build_cycle(np.random.randint(self.graph.no_of_vertices())))

        cycles = []
        times = []
        for cycle in start_cycles:
            improved = True
            start_time = time.time()
            while improved:
                actions = all_actions(cycle, self.graph)
                cycle, improved = self.alter_cycle(cycle, actions)
                # res = ExperimentResult(0, 0, 0, cycle, "steepest lom")
                # PlotUtil.plot_best_cycle(res, self.graph.coords, "inst")
            cycles.append(cycle)
            times.append(time.time()-start_time)
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
                                method_classname=self.__class__.__name__,
                                time_average=np.mean(times),
                                time_min=np.min(times),
                                time_max=np.max(times)
                                )


def all_actions(cycle, graph):
    cycle_set = set(cycle)
    graph_set = set(range(graph.no_of_vertices()))
    not_in_cycle = graph_set - cycle_set
    actions = []
    for inner, outer in itertools.product(cycle_set, not_in_cycle):
        inner_pos = cycle.index(inner)
        inner_left = cycle[inner_pos - 1]
        inner_right = cycle[(inner_pos + 1) % len(cycle)]
        actions.append(NodeSwap(inner=inner, outer=outer, inner_neighbors={inner_left, inner_right}))

    edges = []
    for i in range(len(cycle)):
        edges.append((cycle[i], cycle[(i+1) % len(cycle)]))

    for e1, e2 in [(edges[i], edges[j]) for i in range(len(edges)) for j in range(i+1, len(edges))]:
        actions.append(EdgeSwap(e1, e2))

    np.random.shuffle(actions)
    return actions


class EdgeSwap:
    def __init__(self, edge1, edge2):
        self.n1, self.succ_n1 = edge1
        self.n2, self.succ_n2 = edge2

    def get_delta(self, graph):
        if self.n1 == self.n2 and self.succ_n1 == self.succ_n2:
            return 0
        return graph.adjacency_matrix[self.n1][self.n2] + graph.adjacency_matrix[self.succ_n1][self.succ_n2] - \
               (graph.adjacency_matrix[self.n1][self.succ_n1] + graph.adjacency_matrix[self.n2][self.succ_n2])

    def alter(self, cycle):
        first_pos = cycle.index(self.succ_n1)
        second_pos = cycle.index(self.n2)
        steps = (second_pos-first_pos)%len(cycle)
        for i in range((steps+1)//2):
            first_iter = (first_pos+i)%len(cycle)
            second_iter = (second_pos-i)%len(cycle)
            cycle[first_iter],cycle[second_iter] = cycle[second_iter],cycle[first_iter]
        return cycle


class NodeSwap:
    def __init__(self, inner, outer, inner_neighbors):
        self.inner = inner
        self.outer = outer
        self.inner_neighbors = inner_neighbors

    def get_delta(self, graph):
        in_neigh = iter(self.inner_neighbors)
        previous = next(in_neigh)
        next_v = next(in_neigh)

        return graph.adjacency_matrix[previous][self.outer] + graph.adjacency_matrix[self.outer][next_v] - \
               graph.adjacency_matrix[previous][self.inner] - graph.adjacency_matrix[self.inner][next_v]

    def alter(self, cycle):
        inside_pos = cycle.index(self.inner)
        cycle[inside_pos] = self.outer
        return cycle
