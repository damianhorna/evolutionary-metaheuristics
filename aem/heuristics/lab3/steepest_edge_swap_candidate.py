from aem.heuristics.lab3.moves import NodeSwap, EdgeSwap
from aem.heuristics.lab3.steepest_heuristic import SteepestHeuristic


class SteepestEdgeSwapCandidate(SteepestHeuristic):
    def __init__(self, graph, k=5):
        super().__init__(graph)
        self.k = k

    def alter_cycle(self, cycle):
        moves = self.candidate_moves(cycle)
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

    def candidate_moves(self, cycle):
        for n1 in cycle:
            for n2 in self.graph.nearest_neighbors(v=n1, k=self.k):
                if n2 in cycle: # EdgeSwap
                    n1_prev = cycle[cycle.index(n1) - 1]
                    n2_prev = cycle[cycle.index(n2) - 1]
                    n1_next = cycle[(cycle.index(n1) + 1) % len(cycle)]
                    n2_next = cycle[(cycle.index(n2) + 1) % len(cycle)]

                    es1 = EdgeSwap((n1, n1_next), (n2, n2_next))
                    es2 = EdgeSwap((n1_prev, n1), (n2_prev, n2))
                    if es1.get_delta(self.graph) < es2.get_delta(self.graph):
                        yield es1
                    else:
                        yield es2
                else: # NodeSwap
                    n1_prev = cycle[cycle.index(n1) - 1]
                    n1_next = cycle[(cycle.index(n1) + 1) % len(cycle)]
                    ns1 = NodeSwap(n1_prev, n2, (cycle[cycle.index(n1_prev) - 1], n1))
                    ns2 = NodeSwap(n1_next, n2, (n1, cycle[(cycle.index(n1_next) + 1) % len(cycle)]))
                    if ns1.get_delta(self.graph) < ns2.get_delta(self.graph):
                        yield ns1
                    else:
                        yield ns2

    def reset(self):
        pass