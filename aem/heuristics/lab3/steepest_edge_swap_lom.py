from aem.heuristics.alter.action_factory import pair_permutations, SwapInnerEdges, SwapInnerOuter
from aem.heuristics.lab3.steepest_heuristic import SteepestHeuristic


class SteepestEdgeSwapListOfMoves(SteepestHeuristic):
    def __init__(self, graph):
        self.l_of_moves = []
        super().__init__(graph)
        self.old_actions = set()

    def alter_cycle(self, cycle):
        for action in self.generate_action(cycle, self.graph):
            if (action.first, action.second) not in self.old_actions:
                delta = action.get_delta(cycle, self.graph)
                if delta < 0:
                    self.old_actions.add((action.first, action.second))
                    self.l_of_moves.append((action, delta))

        if len(self.l_of_moves) != 0:
            self.l_of_moves.sort(key=lambda x: x[1])
            best_action, best_delta = self.l_of_moves[0]
            if isinstance(best_action, SwapInnerOuter):
                self.filter_invalid_inner_outer(best_action, cycle)
            else:
                self.filter_invalid_inner_edges(best_action, cycle)
            self.old_actions = {(action.first, action.second) for (action, _) in self.l_of_moves}
            return best_action.alter(cycle, self.graph, True), True
        else:
            return cycle, False

    def filter_invalid_inner_edges(self, best_action, cycle):
        first_pos = cycle.index(best_action.first)
        second_pos = cycle.index(best_action.second)

        first_previous = cycle[first_pos - 1]
        second_next = cycle[(second_pos + 1) % len(cycle)]

        first_next = cycle[(first_pos + 1) % len(cycle)]
        second_previous = cycle[second_pos - 1]

        banned = {first_previous, first_next, second_previous, second_next}
        steps = (second_pos - first_pos) % len(cycle)
        for i in range((steps + 1) // 2):
            first_iter = (first_pos + i) % len(cycle)
            second_iter = (second_pos - i) % len(cycle)
            banned.add(cycle[first_iter])
            banned.add(cycle[second_iter])
        self.l_of_moves = [(action, delta) for (action, delta) in self.l_of_moves if
                           action.first not in banned and action.second not in banned]

    def filter_invalid_inner_outer(self, best_action, cycle):
        first_previous, first_next, second_previous, second_next = None, None, None, None
        if best_action.first in cycle:
            first_pos = cycle.index(best_action.first)
            first_previous = cycle[first_pos - 1]
            first_next = cycle[(first_pos + 1) % len(cycle)]

        if best_action.second in cycle:
            second_pos = cycle.index(best_action.second)
            second_next = cycle[(second_pos + 1) % len(cycle)]
            second_previous = cycle[second_pos - 1]
        banned = {first_previous, first_next, second_previous, second_next, best_action.first, best_action.second}
        self.l_of_moves = [(action, delta) for (action, delta) in self.l_of_moves if
                           action.first not in banned and action.second not in banned]

    @staticmethod
    def generate_action(cycle, graph):
        for (a, b) in pair_permutations(graph.no_of_vertices()):
            action_inner = SwapInnerEdges(a, b)
            action_outer = SwapInnerOuter(a, b)
            if action_inner.is_valid(cycle, graph) and a != b:
                yield action_inner
            elif a < b and action_outer.is_valid(cycle, graph):
                yield action_outer
