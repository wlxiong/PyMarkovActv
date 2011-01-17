# The basic structure for transport network
import hashlib

class Node(object):
    " node is a base class here. stop, zone and intersection are derived from it. "
    def __init__(self, name):
        self.name = name
        self.adjacent_vectors = []

    def __eq__(self, other):
        return self.name == other.name
    
    def __repr__(self):
        return "%s" % (self.name)

    def __hash__(self):
        return int(hashlib.md5(repr(self)).hexdigest(), 16)

    def add_adjacent_vector(self, vector):
        self.adjacent_vectors.append(vector)
        
    
class Zone(Node):
    "A zone is a area where people participate various activities. "
    def __init__(self, name, activity_list, population):
        super(Zone, self).__init__(name)
        self.involved_activities = activity_list
        for each_actv in self.involved_activities:
            each_actv.add_location(self)
        self.population = population


class Vector(object):
    "Vector is the base class for road, transit line and sidewalk. "
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name
    
    def __repr__(self):
        return "%s" % (self.name)

    def __hash__(self):
        return int(hashlib.md5(repr(self)).hexdigest(), 16)

    def calc_travel_time(self, move):
        raise NotImplementedError

    def calc_travel_cost(self, travel_time, move):
        raise NotImplementedError


class Edge(object):
    "Edge is the base class for segments of road, transit line and sidewalk. "
    def __init__(self, vector, head_node, tail_node):
        self.related_vector, self.head_node, self.tail_node = \
            vector, head_node, tail_node

    def __eq__(self, other):
        return self.related_vector == other.related_vector and \
               self.head_node == other. head_node and \
               self.tail_node == other. tail_node

    def __repr__(self):
        return "%s(%s)%s" % (self.head_node, repr(self.related_vector), self.tail_node)

    def __hash__(self):
        return int(hashlib.md5(repr(self)).hexdigest(), 16)


class Move(object):
    "A move (movement) is a pair of time and edge. The time recodes when the traveler enters the edge. "
    def __init__(self, timeslice, edge):
        self.timeslice, self.related_edge = timeslice, edge

    def __eq__(self, other):
        return self.timeslice == other.timeslice and \
               self.related_edge == other.related_edge

    def __repr__(self):
        return "@%s-%s" % (self.timeslice, self.related_edge)

    def __hash__(self):
        return int(hashlib.md5(repr(self)).hexdigest(), 16)
