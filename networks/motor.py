# Motor network
import math
from networks.basic import Vector
from shared.universe import conf
from utils.convert import min2slice

class Road(Vector):
    """ Road is the connection between zones (residential location, economic activity area)
        and hubs (i.e. transit stop, parking lot) in transport network. 
    """
    def __init__(self, name, head_node, tail_node, drive_time, capacity, length, toll = 0.0):
        super(Road, self).__init__(name)
        self.head_node, self.tail_node, self.drive_time, self.capacity, self.length, self.toll = \
            head_node, tail_node, drive_time, capacity/min2slice(60.0), length, toll 
        self.head_node.add_adjacent_vector(self)

    def calc_travel_time(self, move_flow):
        if move_flow > self.capacity * 8:
            print "%s: %s / %s" % (self, move_flow, self.capacity)
            raise PendingDeprecationWarning('Road capacity excess (8x)! ')
        self.travel_time = self.drive_time*(1.0 + .5*math.pow(move_flow/self.capacity, 4.0))
        return self.travel_time

    def calc_travel_cost(self, drive_time):
        return drive_time * conf.ALPHA_car + self.toll

    def calc_vehicle_emission(self, drive_time):
        return 0.2038 * drive_time * math.exp(0.7962* (self.length / drive_time))
