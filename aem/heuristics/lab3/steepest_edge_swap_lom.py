import itertools

from aem.heuristics.alter.action_factory import pair_permutations, SwapInnerEdges, SwapInnerOuter
from aem.heuristics.lab3.steepest_heuristic import SteepestHeuristic


class SteepestEdgeSwapListOfMoves(SteepestHeuristic):
    def __init__(self, graph):
        self.l_of_moves = []
        super().__init__(graph)
        self.old_actions = set()

    def alter_cycle(self, cycle):
        for action in self.generate_action(cycle, self.graph):
            if action not in self.old_actions:
                delta = action.get_delta(cycle, self.graph)
                if delta < 0:
                    self.old_actions.add(action)
                    self.l_of_moves.append((action, delta))



        if len(self.l_of_moves) != 0:
            self.l_of_moves.sort(key=lambda x: x[1])
            best_action, best_delta = self.l_of_moves[0]
            self.old_actions = {action for (action, _) in self.l_of_moves}
            return best_action.alter(cycle, self.graph, True), True
        else:
            return cycle, False