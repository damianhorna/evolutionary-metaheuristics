from aem.heuristics.heuristic import Heuristic
from aem.heuristics.lab3.steepest_edge_swap_lom import SteepestEdgeSwapListOfMoves
from aem.shared.experiment_result import ExperimentResult
import numpy as np


class MultipleStartLocalSearch(SteepestEdgeSwapListOfMoves):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, seed=None, number_of_experiments=1) -> ExperimentResult:
        if seed is not None:
            np.random.seed(seed)

        results = []

        seeds = [np.random.randint(2**10) for _ in range(number_of_experiments)]
        for seed in seeds:
            self.reset()
            er = super().run(seed, 100)

            results.append(er)
        scores = list(map(lambda x: x.min, results))
        times = list(map(lambda x: x.time_average * 100, results))

        min_poz = np.argmin(scores)

        return ExperimentResult(
            average_len=np.mean(scores),
            min_len=np.min(scores),
            max_len=np.max(scores),
            best_cycle=results[min_poz].best_cycle,
            method_classname=self.__class__.__name__,
            time_average=np.mean(times),
            time_min=np.min(times),
            time_max=np.max(times)
        )
