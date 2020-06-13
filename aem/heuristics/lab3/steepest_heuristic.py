import itertools

from aem.heuristics.heuristic import Heuristic
from aem.heuristics.lab3.moves import NodeSwap, EdgeSwap
from aem.heuristics.random import Random
from aem.shared.experiment_result import ExperimentResult
import numpy as np
import time

from aem.utils.plot_util import PlotUtil


class SteepestHeuristic(Heuristic):
    def __init__(self, graph):
        super().__init__(graph)

    def alter_cycle(self, cycle):
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
            self.reset()
            while improved:
                cycle, improved = self.alter_cycle(cycle)
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

    def all_moves(self, cycle):  # complexity: cycle_len * not_in_cycle_len or ~ (n/2) * (n/2)
        cycle_set = set(cycle)
        graph_set = set(range(self.graph.no_of_vertices()))
        not_in_cycle = graph_set - cycle_set
        actions = []
        for inner, outer in itertools.product(cycle_set, not_in_cycle):
            inner_pos = cycle.index(inner)
            inner_left = cycle[inner_pos - 1]
            inner_right = cycle[(inner_pos + 1) % len(cycle)]
            actions.append(NodeSwap(inner=inner, outer=outer, inner_neighbors=(inner_left, inner_right)))

        edges = []
        for i in range(len(cycle)):
            edges.append((cycle[i], cycle[(i+1) % len(cycle)]))

        for e1, e2 in [(edges[i], edges[j]) for i in range(len(edges)) for j in range(i+1, len(edges))]:
            actions.append(EdgeSwap(e1, e2))

        np.random.shuffle(actions)
        return actions

