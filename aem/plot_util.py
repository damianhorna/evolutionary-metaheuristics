import matplotlib.pyplot as plt
from aem.experiment_result import ExperimentResult


class PlotUtil:

    @staticmethod
    def plot_best_cycle(res: ExperimentResult, coords: dict, instance):
        cycle_coords_x = [coords[v][0] for v in res.best_cycle]
        cycle_coords_y = [coords[v][1] for v in res.best_cycle]

        all_x, all_y = zip(*list(coords.values()))
        plt.figure()
        plt.title(f"{res.method_classname} best cycle ({instance[8:-4]})")
        plt.scatter(all_x, all_y)
        plt.plot(cycle_coords_x + [cycle_coords_x[0]], cycle_coords_y + [cycle_coords_y[0]], c='r')
        plt.savefig(f"plots/{res.method_classname}-{instance[8:-4]}-best.png")
        plt.close()
