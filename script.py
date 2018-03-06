import sys

file_name = sys.argv[1]
vehicle_waiting_weight = float(sys.argv[2])
pickup_distance_weight = float(sys.argv[3])
bonus_weight = float(sys.argv[4])


def write_to_file(filename, fleet):
    rides = ''
    for vehicle in fleet:
        rides += '{}'.format(len(vehicle.rides))
        for ride in vehicle.rides:
            rides += ' ' + str(ride.id)
        rides += '\n'

    with open('output/{}.out'.format(filename), 'w') as file:
        file.write(rides)


class Intersection:
    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column

    def distance(self, other) -> int:
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

    def pickup_distance(self, vehicle_position: Intersection):
        return vehicle_position.distance(self.start)

    def ride_distance(self):
        return self.start.distance(self.end)

    def valid_ride(self, time: int, vehicle_position: Intersection) -> bool:
        pickup_distance = self.pickup_distance(vehicle_position)
        ride_distance = self.ride_distance()

        return time + pickup_distance + ride_distance < self.window.end_by

    def vehicle_waiting_time(self, time, vehicle_position):
        return abs(self.window.start_at - time + self.pickup_distance(vehicle_position))

    def priority(self, time: int, vehicle_position: Intersection) -> float:

        pickup_distance = self.pickup_distance(vehicle_position)
        vehicle_waiting_time = self.vehicle_waiting_time(time, vehicle_position)
        gives_bonus = (vehicle_waiting_time >= 0)

        return vehicle_waiting_weight * vehicle_waiting_time \
               + pickup_distance_weight * pickup_distance \
               - bonus_weight * gives_bonus


class Vehicle:
    def __init__(self):
        self.rides =[]
        self.position = Intersection(0, 0)
        self.time_to_destination = 0
        self.picked_ride = None
        self.empty_rides = 0
        self.boni = 0

    def tick(self, ride_pool: [], time: int):

        if self.time_to_destination > 0:
            self.time_to_destination -= 1
        else:
            valid_rides = list(filter(lambda ride: ride.valid_ride(time, self.position), ride_pool))

            if len(valid_rides) > 0:
                self.picked_ride = sorted(valid_rides, key=lambda ride: ride.priority(time, self.position))[0]
                ride_pool.remove(self.picked_ride)

    def commit_tick(self, time: int):
        if self.picked_ride:
            self.time_to_destination = \
                self.picked_ride.pickup_distance(self.position) \
                + max(0, self.picked_ride.vehicle_waiting_time(time, self.position)) \
                + self.picked_ride.ride_distance()

            self.position = self.picked_ride.end
            self.rides.append(self.picked_ride)
            self.empty_rides += self.picked_ride.pickup_distance(self.position) \
                + max(0, self.picked_ride.vehicle_waiting_time(time, self.position))
            self.boni += (self.picked_ride.vehicle_waiting_time(time, self.position) >= 0)
            self.picked_ride = None

with open('input/{}.in'.format(file_name), 'r') as file:
    lines = file.readlines()

    metadata = [int(d) for d in lines[0].split(' ')]

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

fleet = []
for i in range(fleet_size):
    fleet.append(Vehicle())

empty_rides = 0
boni = 0

for time in range(timesteps):

    for vehicle in fleet:
        vehicle.tick(ride_pool, time)
        vehicle.commit_tick(time)

for vehicle in fleet:
    empty_rides += vehicle.empty_rides
    boni += vehicle.boni

write_to_file('{}-{}-{}-{}'.format(file_name, vehicle_waiting_weight, pickup_distance_weight, bonus_weight), fleet)

meta = '{}: {}, {}, {}\n'.format(file_name, vehicle_waiting_weight, pickup_distance_weight, bonus_weight) \
       + 'unserved rides: {}\n'.format(len(ride_pool)) \
       + 'empty rides: {}\n'.format(empty_rides / fleet_size) \
       +'boni percentage: {}\n'.format((boni / (number_of_rides - len(ride_pool ))) * 100) \
       + '---------------------\n\n'

with open('output/meta.txt', 'a') as file:
    file.write(meta)
