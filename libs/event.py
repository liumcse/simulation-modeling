class Event:
    def __init__(self, event_type: str, arrival_time: float, station: int, duration: float,
                 direction: str, speed: float, position: float = 0):
        self.event_type = event_type
        self.arrival_time = arrival_time
        self.station = station
        self.duration = duration
        self.position = position
        self.direction = direction
        self.speed = speed

    def __gt__(self, other):
        return self.arrival_time > other.arrival_time

    def __ge__(self, other):
        return self.arrival_time >= other.arrival_time

    def __le__(self, other):
        return self.arrival_time <= other.arrival_time

    def __lt__(self, other):
        return self.arrival_time < other.arrival_time

    def __eq__(self, other):
        return self.arrival_time == other.arrival_time