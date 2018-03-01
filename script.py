file_name = 'b_should_be_easy.in'

def write_to_file(filename, fleet):
    rides = ''
    for vehicle in fleet:
        rides += '{}'.format(len(vehicle.rides))
        for ride in vehicle.rides:
            rides += ' ' + str(ride.id)
        rides += '\n'

    with open(filename, 'w') as file:
        file.write(rides)

class Grid:
    def __init__(self, rows: int, columns: int):
        self.rows = rows
        self.columns = columns

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
        return self.window.start_at - time + self.pickup_distance(vehicle_position)

    def priority(self, time: int, vehicle_position: Intersection) -> float:

        vehicle_waiting_weight = 0.5
        pickup_distance_weight = 0.5
        bonus_weight = 0.5

        pickup_distance = self.pickup_distance(vehicle_position)
        vehicle_waiting_time = self.vehicle_waiting_time(time, vehicle_position)
        gives_bouns = (vehicle_waiting_time >= 0)

        return vehicle_waiting_weight * vehicle_waiting_time \
               + pickup_distance_weight * pickup_distance \
               - bonus_weight * gives_bouns




class Vehicle:
    def __init__(self):
        self.rides =[]
        self.postition = Intersection(0, 0)
        self.time_to_destination = 0
        self.picked_ride = None

    def tick(self, ride_pool: [], time: int):

        if self.time_to_destination > 0:
            self.time_to_destination -= 1
        else:
            valid_rides = list(filter(lambda ride: ride.valid_ride(time, self.postition), ride_pool))

            if len(valid_rides) > 0:
                self.picked_ride = sorted(valid_rides, key=lambda ride: ride.priority(time, self.postition))[0]
                ride_pool.remove(self.picked_ride)

    def commit_tick(self, time: int):
        if self.picked_ride:
            self.time_to_destination = self.picked_ride.pickup_distance(self.postition) + max(0, self.picked_ride.vehicle_waiting_time(time, self.postition))
            self.postition = self.picked_ride.end
            self.rides.append(self.picked_ride)
            self.picked_ride = None

with open(file_name, 'r') as file:
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

fleet = []
for i in range(fleet_size):
    fleet.append(Vehicle())

for time in range(timesteps):

    if time % 100 == 0: print('time {}'.format(time))

    for vehicle in fleet:
        vehicle.tick(ride_pool, time)
        vehicle.commit_tick(time)

write_to_file(file_name.split('.')[0] + '.out', fleet)
