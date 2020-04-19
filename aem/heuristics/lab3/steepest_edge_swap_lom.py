from aem.heuristics.lab3.steepest_heuristic import SteepestHeuristic


class SteepestEdgeSwapListOfMoves(SteepestHeuristic):
    def __init__(self, graph):
        self.LM = []
        super().__init__(graph)
        self.new_moves = None
        self.LM_lookup = set()

    def alter_cycle(self, cycle):
        if self.new_moves is None: # first iteration
            self.new_moves = self.all_moves(cycle)
        else:
            # TODO: how to generate new moves smarter?
            self.new_moves = [move for move in self.all_moves(cycle) if move not in self.LM_lookup]
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
            return best_move.alter(cycle), True
        else:
            return cycle, False
