# Motor network
import math
from shared.universe import flow 

class Road(Vector):
    """ Sidewalk is the connection between zones (residential location, economic activity area)
        and hubs (i.e. transit stop, parking lot) in transport network. 
    """
    def __init__(self, name, head_node, tail_node, drive_time, capacity, toll = 0.0):
        road_name = 'RD' + str(name)
        super(Road, self).__init__(road_name)
        self.head_node, self.tail_node, self.drive_time, self.capacity = \
                        head_node, tail_node, drive_time, capacity

    def get_travel_time(self, move):
##        # non-congestion travel time
##        return drive_time
        get_edge_flow(move)
        if flow.edge_flows[move] > self.capacity * 8:
            print self
            raise PendingDeprecationWarning('Road capacity excess (8x)! ')
        self.travel_time = self.drive_time*(1.0 + .15*math.pow(flow.edge_flows[move]/self.capacity, 4.0))
        return self.travel_time

    def get_travel_cost(self):
        return self.travel_time * base.ALPHA_car + self.toll

