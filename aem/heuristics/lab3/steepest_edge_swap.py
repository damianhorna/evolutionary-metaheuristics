from aem.heuristics.alter.action_factory import pair_permutations, SwapInnerEdges, SwapInnerOuter
from aem.heuristics.lab3.steepest_heuristic import SteepestHeuristic


class SteepestEdgeSwap(SteepestHeuristic):
    def __init__(self, graph):
        super().__init__(graph)

    def alter_cycle(self, cycle):
        moves = self.all_moves(cycle)
        best_move = None
        best_delta = 0
        for move in moves:
            delta = move.get_delta(self.graph)
            if delta < best_delta:
                best_delta = delta
                best_move = move
        if best_move is not None:
            return best_move.alter(cycle), True
        return cycle, False

    def reset(self):
        pass
