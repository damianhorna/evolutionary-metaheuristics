from aem.heuristics.alter.action_factory import pair_permutations, SwapInnerEdges, SwapInnerOuter
from aem.heuristics.lab3.steepest_heuristic import SteepestHeuristic


class SteepestEdgeSwap(SteepestHeuristic):
    def __int__(self, graph):
        super().__init__(graph)

    def alter_cycle(self, cycle):
        best_action = None
        best_delta = 0
        for action in self.generate_action(cycle, self.graph):
            delta = action.get_delta(cycle, self.graph)
            if delta < best_delta:
                best_delta = delta
                best_action = action
        if best_action is not None:
            return best_action.alter(cycle, self.graph, False), True
        return cycle, False

    def generate_action(self, cycle, graph):
        for (a, b) in pair_permutations(graph.no_of_vertices()):
            action_inner = SwapInnerEdges(a, b)
            action_outer = SwapInnerOuter(a, b)
            if action_inner.is_valid(cycle, graph) and a != b:
                yield action_inner
            elif a < b and action_outer.is_valid(cycle, graph):
                yield action_outer
