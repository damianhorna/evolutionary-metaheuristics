from aem.heuristics.alter.action_factory import pair_permutations, SwapInnerEdges, SwapInnerOuter
from aem.heuristics.lab3.steepest_heuristic import SteepestHeuristic


class SteepestEdgeSwap(SteepestHeuristic):
    def __init__(self, graph):
        super().__init__(graph)

    def alter_cycle(self, cycle, actions):
        best_action = None
        best_delta = 0
        for action in actions:
            delta = action.get_delta(self.graph)
            if delta < best_delta:
                best_delta = delta
                best_action = action
        if best_action is not None:
            return best_action.alter(cycle), True
        return cycle, False
