from aem.heuristics.lab3.moves import EdgeSwap, NodeSwap
from aem.heuristics.lab3.steepest_heuristic import SteepestHeuristic


class SteepestEdgeSwapListOfMoves(SteepestHeuristic):
    def __init__(self, graph):
        self.LM = []
        super().__init__(graph)
        self.new_moves = None
        self.LM_lookup = set()

    def alter_cycle(self, cycle):
        if self.new_moves is None:  # first iteration
            self.new_moves = self.all_moves(cycle)
        # else:
        #     # TODO: how to generate new moves smarter?
        #     self.new_moves = [move for move in self.all_moves(cycle) if move not in self.LM_lookup]
        for move in self.new_moves:
            delta = move.get_delta(self.graph)
            move.delta = delta
            if delta < 0:
                self.LM.append(move)

        self.LM = [move for move in self.LM if move.is_applicable(cycle)]
        self.LM.sort(key=lambda m: m.delta)
        self.LM_lookup = set(self.LM)

        if len(self.LM) > 0:
            best_move = self.LM[0]
            altered_cycle = best_move.alter(cycle)
            self.add_new_moves(best_move, cycle)
            return altered_cycle, True
        else:
            return cycle, False

    def add_new_moves(self, best_move, cycle):
        self.new_moves = []
        if isinstance(best_move, EdgeSwap):
            added_edge1 = (best_move.succ_n2, best_move.succ_n1)
            added_edge2 = (best_move.n2, best_move.n1)
            edges = []
            for i in range(len(cycle)):
                edges.append((cycle[i], cycle[(i + 1) % len(cycle)]))

            for edge in edges:
                self.new_moves.append(EdgeSwap(added_edge1, edge))
                self.new_moves.append(EdgeSwap(added_edge2, edge))
        elif isinstance(best_move, NodeSwap):
            new_inner_pos = cycle.index(best_move.outer)
            not_in_cycle = set(range(self.graph.no_of_vertices())) - set(cycle)
            for v in not_in_cycle:
                new_node_swap = NodeSwap(best_move.outer,
                                         v,
                                         (cycle[new_inner_pos - 1], cycle[(new_inner_pos + 1) % len(cycle)]))
                self.new_moves.append(new_node_swap)
            edges = []
            for i in range(len(cycle)):
                edges.append((cycle[i], cycle[(i + 1) % len(cycle)]))
            added_edge1 = (best_move.inner_neighbors[0], best_move.outer)
            added_edge2 = (best_move.outer, best_move.inner_neighbors[1])
            for edge in edges:
                self.new_moves.append(EdgeSwap(added_edge1, edge))
                self.new_moves.append(EdgeSwap(added_edge2, edge))
