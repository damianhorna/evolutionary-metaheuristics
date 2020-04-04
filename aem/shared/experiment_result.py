class ExperimentResult:
    def __init__(self, average_len, min_len, max_len, best_cycle, method_classname, time_average=None, time_min=None, time_max=None):
        self.average = average_len
        self.min = min_len
        self.max = max_len
        self.method_classname = method_classname
        self.best_cycle = best_cycle
        self.time_min = time_min
        self.time_max = time_max
        self.time_average = time_average

    def print(self):
        print(f"{self.method_classname} result:")
        print(f"Average: {self.average}")
        print(f"Min: {self.min}")
        print(f"Max: {self.max}")
        if self.time_average is not None:
            print(f"Time Average: {self.time_average}")
            print(f"Time Min: {self.time_min}")
            print(f"Time Max: {self.time_max}")

