# Pedestrian network for accessing other transportation facilities
import math
from networks.basic import Vector
from shared.universe import conf

class Sidewalk(Vector):
    """ Sidewalk is the connection between zones (residential location, economic activity area)
        and hubs (i.e. transit stop, parking lot) in transport network. 
    """
    def __init__(self, name, head_node, tail_node, walk_time, capacity):
        super(Sidewalk, self).__init__(name)
        self.head_node, self.tail_node = head_node, tail_node
        self.head_node.add_adjacent_vector(self)
        self.walk_time, self.capacity = walk_time, capacity

    def calc_travel_time(self, move_flow):
        if move_flow > self.capacity * 8:
            print "%s: %s / %s" % (self, move_flow, self.capacity)
            raise PendingDeprecationWarning('Sidewalk capacity excess (8x)! ')
        self.travel_time = self.walk_time*(1.0 + .15*math.pow(move_flow/self.capacity, 4.0))
        return self.travel_time

    def calc_travel_cost(self, walk_time):
        return walk_time * conf.ALPHA_walk

