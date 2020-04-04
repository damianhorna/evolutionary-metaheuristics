from aem.heuristics.alter.alter_heuristic import AlterHeuristic


class Greedy(AlterHeuristic):

    def __int__(self, graph, action_factory):
        super().__init__(graph, action_factory)

    def alter_cycle(self, cycle):
        best_action = None
        best_delta = 0
        for action in self.action_factory.generate(cycle, self.graph):
            delta = action.get_delta(cycle, self.graph)
            if delta < best_delta:
                best_action = action
                break
        if best_action is not None:
            return best_action.alter(cycle, self.graph, False), True
        return cycle, False

