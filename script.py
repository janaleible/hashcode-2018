file_name = 'a_example.in'

class Grid:
    def __init__(self, rows: int, columns: int):
        self.rows = rows
        self.columns = columns

class Intersection:
    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column

    def distance(self, other: Intersection) -> int:
        return abs(self.row - other.row) + abs(self.column - other.column)

class Window:
    def __init__(self, start_at: int, end_by: int):
        self.start_at = start_at
        self.end_by = end_by

class Ride:
    def __init__(self, id, start: Intersection, end: Intersection, window: Window):
        self.id = id
        self.start = start
        self.end = end
        self.window = window


    def valid_ride(self, time: int, vehicle_position: Intersection) -> bool:
        pickup_distance = vehicle_position.distance(self.start)
        ride_distance = self.start.distance(self.end)

        return time + pickup_distance + ride_distance > self.window.end_by

    def priority(self, time: int, vehicle_position: Intersection) -> float:

        vehicle_waiting_weight = 0.5
        pickup_distance_weight = 0.5
        bonus_weight = 0.5

        pickup_distance = vehicle_position.distance(self.start)
        vehicle_waiting_time = self.window.start_at - time + pickup_distance
        gives_bouns = (vehicle_waiting_time >= 0)

        return vehicle_waiting_weight * vehicle_waiting_time \
               + pickup_distance_weight * pickup_distance \
               + bonus_weight * bonus




class Vehicle:
    def __init__(self):
        self.rides =[]
        self.destination = Intersection(0, 0)
        self.time_to_destination = 0

    def tick(self, ride_pool: [], time: int):

        if self.time_to_destination > 0:
            self.time_to_destination -= 1
            return
        else:
            valid_rides = filter(lambda ride: ride.valid_ride(time, self.destination), ride_pool)
            



with open('a_example.in', 'r') as file:
    lines = file.readlines()

    metadata = [int(d) for d in lines[0].split(' ')]

    grid = Grid(metadata[0], metadata[1])
    fleet_size = metadata[2]
    number_of_rides = metadata[3]
    bonus = metadata[4]
    timesteps = metadata[5]

    ride_pool = []

    for id, line in enumerate(lines[1:]):
        params = line.split(' ')
        ride = Ride(
            id,
            Intersection(int(params[0]), int(params[1])),
            Intersection(int(params[2]), int(params[3])),
            Window(int(params[4]), int(params[5]))
        )
        ride_pool.append(ride)

