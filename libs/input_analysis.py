import matplotlib.pyplot as plt
import math


class InputAnalyzer:
    def __init__(self):
        self.inter_arrival_time_list = []
        self.base_station_list = []
        self.duration_list = []
        self.speed_list = []
        self.count = 0
        self.read_from_file()

    def read_from_file(self):
        # Read data from file
        with open("./data.csv") as f:
            lines = f.readlines()
            last_arrival_time = 0
            for line in lines:
                line = line.rstrip().split(",")
                arrival_time = float(line[1])
                station = int(line[2])
                duration = float(line[3])
                speed = float(line[4])
                inter_arrival_time = arrival_time - last_arrival_time
                last_arrival_time = arrival_time
                # Add to list
                self.inter_arrival_time_list.append(inter_arrival_time)
                self.base_station_list.append(station)
                self.duration_list.append(duration)
                self.speed_list.append(speed)
                self.count += 1

    def draw_histogram_iat(self):
        plt.hist(x=self.inter_arrival_time_list)
        plt.title("Inter-Arrival Time")
        plt.xlabel("Seconds")
        plt.ylabel("Occurrences")
        plt.show()

    def draw_histogram_base_station(self):
        plt.hist(x=self.base_station_list)
        plt.title("Base Station")
        plt.xlabel("Station")
        plt.ylabel("Occurrences")
        plt.show()

    def draw_histogram_duration(self):
        plt.hist(x=self.duration_list)
        plt.title("Call Duration")
        plt.xlabel("Seconds")
        plt.ylabel("Occurrences")
        plt.show()

    def draw_histogram_speed(self):
        plt.hist(x=self.speed_list)
        plt.title("Speed")
        plt.xlabel("km/h")
        plt.ylabel("Occurrences")
        plt.show()

    def calculate_parameters_iat(self):
        return sum(self.inter_arrival_time_list) / float(self.count)

    def calculate_parameters_base_station(self):
        return min(self.base_station_list), max(self.base_station_list)

    def calculate_parameters_duration(self):
        return sum(self.duration_list) / float(self.count)

    def calculate_parameters_speed(self):
        u = sum(self.speed_list) / float(self.count)
        sigma = sum((x - u) ** 2 for x in self.speed_list) / float(self.count)
        return u, sigma

    def chi_square_test_iat(self):
        k = 100
        pj = 0.01
        n = 10000
        beta = 1.3696799000000002
        # Calculate intervals
        endpoints = [beta * math.log(1 / (1 - i * pj)) for i in range(k)]
        endpoints.append(float("inf"))
        # Calculate Nj
        N = [sum(1 for x in self.inter_arrival_time_list if endpoints[j] <= x < endpoints[j + 1]) for j in
             range(k)]
        for i in range(k):
            N.append(sum(1 for x in self.inter_arrival_time_list if endpoints[i] <= x < endpoints[i + 1]))
        chi_square = 0
        for i in range(k):
            chi_square += math.pow(N[i] - n * pj, 2) / float(n * pj)
        return chi_square

    def chi_square_test_duration(self):
        k = 100
        pj = 0.01
        n = 10000
        beta = 109.83589730000018
        min_duration = min(self.duration_list)
        self.duration_list = [x - min_duration for x in self.duration_list]
        # Calculate intervals
        endpoints = [beta * math.log(1 / (1 - i * pj)) for i in range(k)]
        endpoints.append(float("inf"))
        # Calculate Nj
        N = [sum(1 for x in self.duration_list if endpoints[j] <= x < endpoints[j + 1]) for j in
             range(k)]
        for i in range(k):
            N.append(sum(1 for x in self.duration_list if endpoints[i] <= x < endpoints[i + 1]))
        chi_square = 0
        for i in range(k):
            chi_square += math.pow(N[i] - n * pj, 2) / float(n * pj)
        return chi_square

    # def chi_square_test_speed(self):
    #     k = 100
    #     pj = 0.01
    #     n = 10000
    #     mu = 120.07209489999991
    #     sigma_square = 81.33522998709363
    #     print("min_duration", min_duration)
    #     self.duration_list = [x - min_duration for x in self.duration_list]
    #     # Calculate intervals
    #     endpoints = [beta * math.log(1 / (1 - i * pj)) for i in range(k)]
    #     endpoints.append(float("inf"))
    #     # Calculate Nj
    #     N = [sum(1 for x in self.duration_list if endpoints[j] <= x < endpoints[j + 1]) for j in
    #          range(k)]
    #     for i in range(k):
    #         N.append(sum(1 for x in self.duration_list if endpoints[i] <= x < endpoints[i + 1]))
    #     chi_square = 0
    #     for i in range(k):
    #         chi_square += math.pow(N[i] - n * pj, 2) / float(n * pj)
    #     return chi_square

    @staticmethod
    def get_input_from_file():
        ia = InputAnalyzer()
        return [
            ia.inter_arrival_time_list,
            ia.base_station_list,
            ia.duration_list,
            ia.speed_list
        ]


if __name__ == "__main__":
    input_analyzer = InputAnalyzer()
    input_analyzer.draw_histogram_iat()
    input_analyzer.draw_histogram_duration()
    input_analyzer.draw_histogram_speed()
    input_analyzer.draw_histogram_base_station()

    input_analyzer.chi_square_test_iat()

    print("Parameter of inter arrival time: beta = {}".format(input_analyzer.calculate_parameters_iat()))
    print("Chi-square of inter arrival time: {}".format(input_analyzer.chi_square_test_iat()))
    print("Parameter of base station: a = {}, b = {}".format(*input_analyzer.calculate_parameters_base_station()))
    print("Parameter of duration: beta = {}".format(input_analyzer.calculate_parameters_duration()))
    print("Chi-square of duration: {}".format(input_analyzer.chi_square_test_duration()))
    print("Parameter of speed: mu = {}, sigma = {}".format(*input_analyzer.calculate_parameters_speed()))
