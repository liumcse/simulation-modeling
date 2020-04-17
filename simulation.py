from libs.event import Event
from libs.input_analysis import InputAnalyzer
from libs.random_number_generator import RandomNumberGenerator as RNG
from libs.output_analysis import OutputAnalyzer
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
import heapq


class Simulator:
    def __init__(self, index: int, no_events_total: int, output_analyzer: OutputAnalyzer, no_reserved: int,
                 warm_up_events: int = 0,
                 stochastic: bool = True):
        """
        Initialize state variables
        """
        # System clock
        self.clock = 0
        # Number of calls
        self.no_call_created = 0
        self.no_dropped_call = 0
        self.no_blocked_call = 0
        self.no_handover_call = 0
        self.no_terminated_call = 0
        # Warm up
        self.warm_up_events = warm_up_events
        # Preserve history
        self.no_dropped_call_list = [0 for _ in range(no_events_total + 1)]
        self.no_blocked_call_list = [0 for _ in range(no_events_total + 1)]
        # Number of events
        self.no_events_total = no_events_total
        # Channels
        self.no_free_channel = [9 for _ in range(21)]  # Index 0 is not used; only [1 ... 20] is used
        self.no_reserved = no_reserved
        self.stochastic = stochastic
        # Event list (a priority queue)
        self.event_list = []
        # Analysis
        self.output_analyzer = output_analyzer
        self.drop_rate_list = [0 for _ in range(no_events_total + 1)]
        self.block_rate_list = [0 for _ in range(no_events_total + 1)]
        self.index = index

    def run(self):
        """
        Run the simulation
        :return:
        """
        if not self.stochastic:
            inter_arrival_time_list, base_station_list, duration_list, speed_list = InputAnalyzer.get_input_from_file()
            total_event_count = len(inter_arrival_time_list)
        else:
            inter_arrival_time_list = [RNG.generate_inter_arrival_time() for _ in range(no_events_total)]
            base_station_list = [RNG.generate_base_station() for _ in range(no_events_total)]
            duration_list = [RNG.generate_duration() for _ in range(no_events_total)]
            speed_list = [RNG.generate_speed() for _ in range(no_events_total)]
            total_event_count = no_events_total
        # Add the first event
        idx = 0
        event = Event(event_type="INITIALIZATION",
                      arrival_time=self.clock + inter_arrival_time_list[idx],
                      station=base_station_list[idx],
                      duration=duration_list[idx],
                      position=RNG.generate_position(),
                      speed=speed_list[idx],
                      direction=RNG.generate_direction())
        heapq.heappush(self.event_list, event)
        while len(self.event_list) > 0:
            idx += 1
            # Deque event from list until it is empty
            front = heapq.heappop(self.event_list)
            self.handle_event(front)
            # Add next initialization event
            if idx < total_event_count:
                # Set system clock to arrival time of the last initialized call
                self.clock = event.arrival_time
                event = Event(event_type="INITIALIZATION",
                              arrival_time=self.clock + inter_arrival_time_list[idx],
                              station=base_station_list[idx],
                              duration=duration_list[idx],
                              position=RNG.generate_position(),
                              speed=speed_list[idx],
                              direction=RNG.generate_direction())
                heapq.heappush(self.event_list, event)
        # Update analyzer
        output_analyzer.update_data(self.index, self.drop_rate_list, self.block_rate_list)
        print("{} blocked, {} dropped, {} terminated".format(self.no_blocked_call, self.no_dropped_call,
                                                             self.no_terminated_call))
        drop_rate = (self.no_dropped_call - self.no_dropped_call_list[self.warm_up_events]) / float(
            self.no_call_created - self.warm_up_events) * 100
        block_rate = (self.no_blocked_call - self.no_blocked_call_list[self.warm_up_events]) / float(
            self.no_call_created - self.warm_up_events) * 100
        return drop_rate, block_rate

    # def should_terminate(self, remaining_time: float, time_to_handover: float, next_station: int):
    #     return remaining_time <= time_to_handover or next_station == 0 or next_station == 21

    def handle_event(self, event: Event):
        # print("Handle event", event.event_type, "arrived at", event.arrival_time)
        if event.event_type == "INITIALIZATION":
            self.handle_initialization(time=event.arrival_time,
                                       speed=event.speed,
                                       station=event.station,
                                       duration=event.duration,
                                       direction=event.direction,
                                       position=event.position)
        elif event.event_type == "HANDOVER":
            self.handle_handover(time=event.arrival_time,
                                 speed=event.speed,
                                 station=event.station,
                                 duration=event.duration,
                                 direction=event.direction)
        else:
            raise Exception("Unknown event type")
        # Update statistics
        self.drop_rate_list[self.no_call_created] = self.no_dropped_call / float(self.no_call_created) * 100
        self.block_rate_list[self.no_call_created] = self.no_blocked_call / float(self.no_call_created) * 100
        self.no_dropped_call_list[self.no_call_created] = self.no_dropped_call
        self.no_blocked_call_list[self.no_call_created] = self.no_blocked_call

    def handle_initialization(self, time: float, speed: float, station: int, position: float, duration: float,
                              direction: str):
        # Update system clock
        self.clock = time
        self.no_call_created += 1
        # Check available channel from current station
        if self.no_free_channel[station] - self.no_reserved <= 0:
            # If no available channel, the call is blocked
            self.no_blocked_call += 1
            return
        # Allocate that channel
        self.no_free_channel[station] -= 1
        if direction == "LEFT":
            time_to_handover = position / speed * 3600  # Hour to second
            next_station = station - 1
        elif direction == "RIGHT":
            time_to_handover = (2 - position) / speed * 3600  # Hour to second
            next_station = station + 1
        else:
            raise Exception("Unknown direction")
        # Decide whether to terminate the call
        if duration <= time_to_handover:
            # Finishing call
            self.no_free_channel[station] += 1
            self.no_terminated_call += 1
            return
        elif next_station == 0 or next_station == 21:
            # Leaving highway
            self.no_free_channel[station] += 1
            self.no_terminated_call += 1
            return
        # Schedule the next handover
        next_event = Event(event_type="HANDOVER",
                           arrival_time=self.clock + time_to_handover,
                           station=next_station,
                           duration=duration - time_to_handover,
                           direction=direction,
                           speed=speed,
                           )
        # self.event_list.append(next_event)
        heapq.heappush(self.event_list, next_event)

    def handle_handover(self, time: float, speed: float, station: int, duration: float, direction: str):
        # Update system clock
        self.clock = time
        if direction == "LEFT":
            last_station = station + 1
            next_station = station - 1
        elif direction == "RIGHT":
            last_station = station - 1
            next_station = station + 1
        else:
            raise Exception("Unknown direction")
        # Free the channel from used station
        self.no_free_channel[last_station] += 1
        if self.no_free_channel[station] == 0:
            # If no free channel, drop the call
            self.no_dropped_call += 1
            return
        if self.no_free_channel[station] < 0:
            raise Exception("Something went wrong")
        # Plan the next handover
        time_to_handover = 2 / speed * 3600  # Hour to second
        # Decide whether to terminate the call
        if duration <= time_to_handover:
            # Leaving highway
            self.no_terminated_call += 1
            return
        elif next_station == 0 or next_station == 21:
            # Finishing call
            self.no_terminated_call += 1
            return
        # Allocate a channel from current station
        self.no_free_channel[station] -= 1
        # Schedule the next handover
        next_event = Event(event_type="HANDOVER",
                           arrival_time=self.clock + time_to_handover,
                           station=next_station,
                           duration=duration - time_to_handover,
                           direction=direction,
                           speed=speed,
                           )
        # self.event_list.append(next_event)
        heapq.heappush(self.event_list, next_event)

    def plot(self):
        plt.plot(self.drop_rate_list, label="Percentage of dropped calls",
                 color="green")
        plt.plot(self.block_rate_list, label="Percentage of blocked calls",
                 color="red")
        plt.title("Summary Measure Of Single Simulation")
        plt.legend()
        plt.show()


def confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), stats.sem(a)
    h = se * stats.t.ppf((1 + confidence) / 2., n - 1)
    return m - h, m + h


if __name__ == "__main__":
    drop_rate_list = []
    block_rate_list = []
    no_events_total = 10000
    no_reserved = 0
    iteration = 100
    output_analyzer = OutputAnalyzer(no_events_total, no_iteration=iteration)
    for i in range(iteration):
        print("Running simulation #" + str(i + 1))
        simulator = Simulator(index=i, no_events_total=no_events_total, output_analyzer=output_analyzer,
                              no_reserved=no_reserved, warm_up_events=2000, stochastic=True)
        drop_rate, block_rate = simulator.run()
        # simulator.plot()
        drop_rate_list.append(drop_rate)
        block_rate_list.append(block_rate)
    mean_drop_rate = np.mean(drop_rate_list)
    mean_block_rate = np.mean(block_rate_list)
    variance_drop_rate = stats.sem(drop_rate_list)
    variance_block_rate = stats.sem(block_rate_list)
    confidence_interval_drop_rate = confidence_interval(data=drop_rate_list)
    confidence_interval_block_rate = confidence_interval(data=block_rate_list)
    print("Mean block rate {:.3f}%, standard deviation {:.3f}, 95% confidence interval [{:.3f}, {:.3f}]".format(
        float(mean_block_rate),
        float(variance_block_rate),
        *confidence_interval_block_rate))
    print("Mean drop rate {:.3f}%, standard deviation {:.3f}, 95% confidence interval [{:.3f}, {:.3f}]".format(
        float(mean_drop_rate),
        float(variance_drop_rate),
        *confidence_interval_drop_rate))
    output_analyzer.plot()
