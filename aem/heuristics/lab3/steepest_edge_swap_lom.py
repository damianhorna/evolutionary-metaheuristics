from aem.heuristics.lab3.moves import EdgeSwap, NodeSwap
from aem.heuristics.lab3.steepest_heuristic import SteepestHeuristic

import heapq

class SteepestEdgeSwapListOfMoves(SteepestHeuristic):
    def __init__(self, graph):
        self.LM = []
        super().__init__(graph)
        self.new_moves = None


    def alter_cycle(self, cycle):
        if self.new_moves is None:  # first iteration new_moves = all_moves
            self.LM = list(map(lambda x: (x.get_delta(self.graph), x), self.all_moves(cycle)))
            heapq.heapify(self.LM)
        else:
            self.new_moves = map(lambda x: (x.get_delta(self.graph), x), self.new_moves)
            self.new_moves = filter(lambda x: x[0] < 0, self.new_moves)

            for move in self.new_moves:
                heapq.heappush(self.LM, move)

        move = None
        delta = 0
        if len(self.LM) > 0:
            delta, move = heapq.heappop(self.LM)
            while not move.is_applicable(cycle) or delta != move.get_delta(self.graph):
                if len(self.LM) == 0:
                    break
                delta, move = heapq.heappop(self.LM)

        if move is None or delta >= 0 or move.get_delta(self.graph) != delta or not move.is_applicable(cycle):
            return cycle, False
        altered_cycle = move.alter(cycle)
        self.add_new_moves(move, cycle)
        return altered_cycle, True

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
                self.new_moves.append(EdgeSwap((best_move.n1, best_move.n2), edge))
                self.new_moves.append(EdgeSwap((best_move.succ_n1, best_move.succ_n2), edge))

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
