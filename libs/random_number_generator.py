import random
import math


class RandomNumberGenerator:
    @classmethod
    def generate_direction(cls):
        x = random.randint(0, 1)
        if x == 0:
            return "LEFT"
        else:
            return "RIGHT"

    @classmethod
    def generate_position(cls):
        return random.uniform(0, 2)

    @classmethod
    def generate_inter_arrival_time(cls):
        return random.expovariate(1 / 1.3696799000000002)

    @classmethod
    def generate_base_station(cls):
        return random.randint(1, 20)

    @classmethod
    def generate_duration(cls):
        return random.expovariate(1 / 109.83589730000018) + 10.004  # TODO: verify the shift

    @classmethod
    def generate_speed(cls):
        return random.normalvariate(120.07209489999991, math.sqrt(81.33522998709363))


if __name__ == "__main__":
    iteration = 100
    direction_list = [RandomNumberGenerator.generate_direction() for i in range(iteration)]
    position_list = [RandomNumberGenerator.generate_position() for i in range(iteration)]
    inter_arrival_time_list = [RandomNumberGenerator.generate_inter_arrival_time() for i in range(iteration)]
    base_station_list = [RandomNumberGenerator.generate_base_station() for i in range(iteration)]
    duration_list = [RandomNumberGenerator.generate_duration() for i in range(iteration)]
    speed_list = [RandomNumberGenerator.generate_speed() for i in range(iteration)]
    print("direction", direction_list)
    print("position", position_list)
    print("inter_arrival_time", inter_arrival_time_list)
    print("base_station", base_station_list)
    print("duration", duration_list)
    print("speed", speed_list)
