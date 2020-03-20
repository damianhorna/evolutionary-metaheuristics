class ExperimentResult:
    def __init__(self, average_len, min_len, max_len, best_cycle, method_classname):
        self.average = average_len
        self.min = min_len
        self.max = max_len
        self.method_classname = method_classname
        self.best_cycle = best_cycle

    def print(self):
        print(f"{self.method_classname} result:")
        print(f"Average: {self.average}")
        print(f"Min: {self.min}")
        print(f"Max: {self.max}")
