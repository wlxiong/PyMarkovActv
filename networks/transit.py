# implementation of a schedule-based transit network
import math
from networks.basic import Node, Vector

class Stop(Node):
    "A stop has a name and a list of lines passing by it. "
    def __init__(self, name):
        super(Stop, self).__init__(name)

class TransitLine(Vector):
    "A line is an ordered list of stops, associated with a timetable. "
    def __init__(self, name, timetable, stop_list, fare_matrix, capacity):
        super(TransitLine, self).__init__(name)
        self.timetable = timetable
        self.stops_on_line, self.fare_matrix, self.capacity = stop_list, fare_matrix, capacity
        self.stop_order = {}
        for order, each_stop in enumerate(self.stops_on_line):
            each_stop.add_adjacent_vector(self)
            self.stop_order[each_stop] = order

    def __str__(self):
        return " line %s: %s " % (self.name, self.stops_on_line)

    def calc_arrival_time(self, time, origin, dest):
        " Return the arrival time and waiting since time (min). "
        try:
            i_origin = self.stop_order[origin]
        except KeyError:
            raise KeyError('Cannot find the stop on the line. ')
        if dest in self.stop_order:
            i_dest = self.stop_order[dest]
            if i_dest > i_origin:
                for run in xrange(len(self.timetable)):
                    if time <= self.timetable[run][i_origin]:
                        wait_time = self.timetable[run][i_origin] - time
                        arrival_time = self.timetable[run][i_dest]
                        return (arrival_time , wait_time)
        return (float('inf'), float('inf'))

    def calc_travel_cost(self, in_vehicle_time, move_flow):
        if move_flow > self.capacity * 8:
            print "%s: %s / %s" % (self, move_flow, self.capacity)
            raise PendingDeprecationWarning('Transit line capacity excess (8x)! ')
        self.travel_cost = in_vehicle_time*(1.0 + .15*math.pow(move_flow/self.capacity, 4.0))
        return self.travel_cost

