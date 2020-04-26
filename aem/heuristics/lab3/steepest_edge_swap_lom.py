from aem.heuristics.lab3.moves import EdgeSwap, NodeSwap
from aem.heuristics.lab3.steepest_heuristic import SteepestHeuristic


class SteepestEdgeSwapListOfMoves(SteepestHeuristic):
    def __init__(self, graph):
        self.LM = []
        super().__init__(graph)
        self.new_moves = None

    def alter_cycle(self, cycle):
        if self.new_moves is None:  # first iteration new_moves = all_moves
            self.new_moves = self.all_moves(cycle)
        for move in self.new_moves:
            delta = move.get_delta(self.graph)
            move.delta = delta
            if delta < 0:
                self.LM.append(move)

        self.LM = [move for move in self.LM if move.is_applicable(cycle)]
        self.LM.sort(key=lambda m: m.delta)

        if len(self.LM) > 0:
            best_move = self.LM[0]
            altered_cycle = best_move.alter(cycle)
            self.add_new_moves(best_move, altered_cycle)
            return altered_cycle, True
        else:
            return cycle, False

    def add_new_moves(self, best_move, altered_cycle):
        self.new_moves = []
        outer_vertices = set(range(self.graph.no_of_vertices())) - set(altered_cycle)
        edges = []
        for i in range(len(altered_cycle)):
            edges.append((altered_cycle[i], altered_cycle[(i + 1) % len(altered_cycle)]))

        if isinstance(best_move, EdgeSwap):
            new_n1_prev = altered_cycle[altered_cycle.index(best_move.n1) - 1]
            new_n2_succ = altered_cycle[(altered_cycle.index(best_move.n2) + 1) % len(altered_cycle)]
            new_succ_n1_prev = altered_cycle[altered_cycle.index(best_move.succ_n1) - 1]
            new_succ_n2_succ = altered_cycle[(altered_cycle.index(best_move.succ_n2) + 1) % len(altered_cycle)]
            for v in outer_vertices:
                self.new_moves.append(NodeSwap(best_move.n1, v, (new_n1_prev, best_move.n2)))
                self.new_moves.append(NodeSwap(best_move.n2, v, (best_move.n1, new_n2_succ)))
                self.new_moves.append(NodeSwap(best_move.succ_n1, v, (new_succ_n1_prev, best_move.succ_n2)))
                self.new_moves.append(NodeSwap(best_move.succ_n2, v, (best_move.succ_n1, new_succ_n2_succ)))

            first_pos = altered_cycle.index(best_move.n1)
            second_pos = altered_cycle.index(best_move.succ_n2)
            steps = (second_pos - first_pos) % len(altered_cycle)
            for edge in edges:
                for i in range(steps):
                    n3 = altered_cycle[(first_pos + i) % len(altered_cycle)]
                    succ_n3 = altered_cycle[(first_pos + i + 1) % len(altered_cycle)]
                    self.new_moves.append(EdgeSwap((n3, succ_n3), edge))

        elif isinstance(best_move, NodeSwap):
            new_inner_pos = altered_cycle.index(best_move.outer)
            neigh_left = altered_cycle[new_inner_pos - 1]
            neigh_right = altered_cycle[(new_inner_pos + 1) % len(altered_cycle)]
            neigh_left_prev = altered_cycle[new_inner_pos - 2]
            neigh_right_succ = altered_cycle[(new_inner_pos + 2) % len(altered_cycle)]
            for v in outer_vertices:
                self.new_moves.append(NodeSwap(best_move.outer,v,(neigh_left, neigh_right)))
                self.new_moves.append(NodeSwap(neigh_left,v,(neigh_left_prev, best_move.outer)))
                self.new_moves.append(NodeSwap(neigh_right,v,(best_move.outer, neigh_right_succ)))
            added_edge1 = (neigh_left, best_move.outer)
            added_edge2 = (best_move.outer, neigh_right)
            for edge in edges:
                self.new_moves.append(EdgeSwap(added_edge1, edge))
                self.new_moves.append(EdgeSwap(added_edge2, edge))

    def reset(self):
        self.LM = []
        self.new_moves = None
