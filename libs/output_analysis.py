import matplotlib.pyplot as plt
import numpy


class OutputAnalyzer:
    def __init__(self, no_event_per_simulation: int, no_iteration: int):
        self.no_event_total = no_event_per_simulation
        self.no_iteration = no_iteration
        self.drop_rate_list_2d = [0.0 for _ in range(no_iteration)]
        self.block_rate_list_2d = [0.0 for _ in range(no_iteration)]

    def update_data(self, iteration_index: int, drop_rate_list: [float], block_rate_list: [float]):
        self.drop_rate_list_2d[iteration_index] = drop_rate_list
        self.block_rate_list_2d[iteration_index] = block_rate_list

    def plot(self):
        # dropped_rate_list = []
        # blocked_rate_list = []
        # for i in range(self.no_event_total):
        #     dropped_rate_list.append(
        #         sum(self.drop_rate_list_2d[iteration_index][i] for iteration_index in
        #             range(self.no_iteration)) / float(self.no_iteration))
        # for j in range(self.no_event_total):
        #     blocked_rate_list.append(
        #         sum(self.block_rate_list_2d[iteration_index][j] for iteration_index in
        #             range(self.no_iteration)) / float(self.no_iteration))
        dropped_rate_list = numpy.mean(self.drop_rate_list_2d, axis=0)
        blocked_rate_list = numpy.mean(self.block_rate_list_2d, axis=0)

        # [x / float(self.no_event_total) * 100 for x in self.no_dropped_call_list]
        # blocked_rate_list = [x / float(self.no_event_total) * 100 for x in self.no_blocked_call_list]
        plt.plot(dropped_rate_list, label="Percentage of dropped calls",
                 color="green")
        plt.plot(blocked_rate_list, label="Percentage of blocked calls",
                 color="red")
        plt.title("Mean Summary Measures Of {} Simulations".format(self.no_iteration))
        plt.legend()
        plt.show()
