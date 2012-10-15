# static path class
import hashlib
from shared.universe import conf
from utils.convert import min2slice, slice2min
from utils.get import get_move_flow
from networks.basic import Move
from networks.transit import TransitLine

class Path(object):
    "A path in transport network is a ordered set of nodes. "
    def __init__(self, node_list=None, edge_list=None):
        if node_list == None:
            self.nodes_on_path = []
        else:
            self.nodes_on_path = node_list
        if edge_list == None:
            self.edges_on_path = []
        else:
            self.edges_on_path = edge_list
        self.id = "%s" % (self.edges_on_path)
        self.moves_on_path = {}
        self.path_travel_timeslice = {}
        self.path_travel_time = {}
        self.path_travel_cost = {}
        self.num_transfer = self.calc_tranfer()
        
    def __cmp__(self, other):
        self.calc_travel_impedences(0)
        other.calc_travel_impedences(0)
        return self.path_travel_timeslice[0] - other.path_travel_timeslice[0]
    
    def __add__(self, extpath):
        if self.nodes_on_path == []:
            return extpath
        elif (self.nodes_on_path[-1] == extpath.nodes_on_path[0]):
            return Path(self.nodes_on_path + extpath.nodes_on_path[1:], \
                        self.edges_on_path + extpath.edges_on_path)
        else:
            raise ValueError('These two paths cannot be joined. ')
        
    def __eq__(self, other):
        return self.nodes_on_path == other.nodes_on_path and \
               self.edges_on_path == other.edges_on_path
        
    def __hash__(self):
        # return int(hashlib.md5(repr(self)).hexdigest(), 16)
        return hash(repr(self))
        
    def __repr__(self):
        return self.id

    def init_movements(self):
        self.moves_on_path = {}
        self.path_travel_timeslice = {}
        self.path_travel_time = {}
        self.path_travel_cost = {}
    
    def calc_tranfer(self):
        # calculate number of transfers
        num_transfer = 0.0
        all_lines = []
        for each_edge in self.edges_on_path:
            if isinstance(each_edge.related_vector, TransitLine):
                all_lines.append(each_edge.related_vector)
        for i in xrange(len(all_lines)-1):
            if all_lines[i] != all_lines[i+1]:
                num_transfer = num_transfer + 1.0
        return num_transfer

    def get_movements(self, timeslice):
        ''' Return the list of movements at timeslice or generate the list if neccessary.
            The travel time and travel cost is calculated at the same time. 
        '''
        if timeslice in self.moves_on_path:
            return self.moves_on_path[timeslice]
        # first calculate transfer cost
        total_travel_cost = self.num_transfer * conf.ALPHA_tran
        # then generate memoization for movements on path, and calculate other travel costs
        self.moves_on_path[timeslice] = []
        self.path_travel_time[timeslice] = 0.0
        timeline = timeslice
        for each_edge in self.edges_on_path:
            if isinstance(each_edge.related_vector, TransitLine):
                # if the edge is a transit line
                line = each_edge.related_vector
                (arrival_time, wait_time) = line.calc_arrival_time(
                    slice2min(timeline), each_edge.head_node, each_edge.tail_node)
                # when there is no public transport service at timeslice, return infinite travel time/cost 
                if arrival_time == float('inf') or wait_time == float('inf'):
                    self.path_travel_timeslice[timeslice] = float('inf')
                    self.path_travel_cost[timeslice] = float('inf')
                    return []
                in_vehicle_time = arrival_time - slice2min(timeline) - wait_time
                # create transit line move
                line_move = Move(timeline + min2slice(wait_time), each_edge)
                self.moves_on_path[timeslice].append(line_move)
                timeline = min2slice(arrival_time)
                # calculate travel cost
                wait_cost = wait_time * conf.ALPHA_wait
                move_flow = get_move_flow(line_move)
                in_vehicle_cost = line.calc_travel_cost(in_vehicle_time, move_flow)
                total_travel_cost = total_travel_cost + in_vehicle_cost + wait_cost
            else:
                # if the edge is NOT a transit line
                each_vector = each_edge.related_vector
                next_move = Move(timeline, each_edge)
                self.moves_on_path[timeslice].append(next_move)
                move_flow = get_move_flow(next_move)
                travel_time = each_vector.calc_travel_time(move_flow)
                travel_cost = each_vector.calc_travel_cost(travel_time)
                timeline = timeline + min2slice(travel_time)
                total_travel_cost = total_travel_cost + travel_cost
                self.path_travel_time[timeslice] += travel_time
        self.path_travel_timeslice[timeslice] = timeline - timeslice
        self.path_travel_cost[timeslice] = total_travel_cost
        return self.moves_on_path[timeslice]

    def calc_travel_impedences(self, timeslice):
        self.get_movements(timeslice)
        # return two travel impedences: travel time (slice) and travel cost
        return (self.path_travel_timeslice[timeslice], self.path_travel_cost[timeslice])
    
    def get_travel_time(self, timeslice):
        return self.path_travel_time[timeslice]
