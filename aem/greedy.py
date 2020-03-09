from aem.experiment_result import ExperimentResult


class Greedy:
    def __init__(self, graph):
        self.graph = graph

    def run(self) -> ExperimentResult:
        return ExperimentResult(0, 0, 0)

