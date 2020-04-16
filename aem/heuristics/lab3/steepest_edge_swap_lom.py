from aem.heuristics.alter.action_factory import pair_permutations, SwapInnerEdges, SwapInnerOuter
from aem.heuristics.lab3.steepest_heuristic import SteepestHeuristic


class SteepestEdgeSwapListOfMoves(SteepestHeuristic):
    def __init__(self, graph):
        self.l_of_moves = []
        super().__init__(graph)

    def alter_cycle(self, cycle):
        for action in self.generate_action(cycle, self.graph):
            delta = action.get_delta(cycle, self.graph)
            if delta < 0:
                self.l_of_moves.append((action, delta))

        # delete not applicable
        self.l_of_moves = [(action, delta) for (action, delta) in self.l_of_moves if action.is_valid(cycle, self.graph)]

        if len(self.l_of_moves) != 0:
            self.l_of_moves.sort(key=lambda x: -x[1])
            best_action = self.l_of_moves[0][0]
            return best_action.alter(cycle, self.graph, False), True
        else:
            return cycle, False

    @staticmethod
    def generate_action(cycle, graph):
        for (a, b) in pair_permutations(graph.no_of_vertices()):
            action_inner = SwapInnerEdges(a, b)
            action_outer = SwapInnerOuter(a, b)
            if action_inner.is_valid(cycle, graph) and a != b:
                yield action_inner
            elif a < b and action_outer.is_valid(cycle, graph):
                yield action_outer
