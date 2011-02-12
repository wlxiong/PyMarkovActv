import hashlib
from shared.universe import conf, elem, util
from utils.convert import min2slice

#class InitDict(dict):
#    def __init__(self, default = None):
#        self.default = default
#
#    def __getitem__(self, key):
#        if not self.has_key(key):
#            self[key] = self.default()
#        return dict.__getitem__(self, key)

class Commodity(object):
    """ The passengers come from every residential location (home) and place of work (work) is a
        defined as a commodity. The activity bundles are enumerated implicitly here. 
    """
    def __init__(self, work, home):
        self.work, self.home, self.bundle = work, home
        self.init_state = State(elem.home_am_activity, self.home)
        self.term_state = State(elem.home_pm_activity, self.home)
        
    def __repr__(self):
        return "(%s-%s).%s" % (self.work, self.home)
        
    def __hash__(self):
        return int(hashlib.md5(repr(self)).hexdigest(), 16)
        
    def __eq__(self, other):
        return self.work == other.work and \
               self.home == other.home 


class State(object):
    """ The state contains the position of the traveler (zone), the activity participated, 
        excluding timeslice. 
    """
    def __init__(self, activity, zone):
        self.zone, self.activity = zone, activity
        
    def __repr__(self):
        return "%s-%s(%s)" % (self.zone, self.activity)
        
    def __hash__(self):
        return int(hashlib.md5(repr(self)).hexdigest(), 16)
        
    def __eq__(self, other):
        return self.activity == other.activity and \
               self.zone == other.zone 

    
class Transition(object):
    """ Transition defines the next state according to current state, including the travel path. 
    """
    def __init__(self, state, path):
        self.state, self.path = state, path
        
    def __repr__(self):
        return "%s-%s" % (self.state, self.path)
        
    def __hash__(self):
        return int(hashlib.md5(repr(self)).hexdigest(), 16)
        
    def __eq__(self, other):
        return self.state == other.state and \
               self.path == other.path


def enum_commodity():
    # for different work-home location and activity bundles
    for work in elem.work_list:
        for home in elem.home_list:
                yield Commodity(work, home)

def enum_state(commodity, timeslice):
    # enumerate all the activities
    for each_actv in elem.activities:
        if each_actv.time_win[0] > timeslice or \
           timeslice > each_actv.time_win[1]:
            continue
        # choose one location for the activity
        for each_dest in each_actv.locations:
            yield State(each_actv, each_dest)

def enum_path(timeslice, this_zone, next_zone):
    for each_path in elem.paths[this_zone][next_zone]:
        # for travel_time, prob in each_path.travel_time_distribution: # stochastic travel time
        travel_timeslice, travel_cost = each_path.calc_travel_impedences(timeslice)
        arrival_timeslice = timeslice + travel_timeslice
        starting_time = arrival_timeslice + 1
        if starting_time > min2slice(conf.DAY):
            continue
        yield each_path, starting_time, travel_cost

def enum_transition(commodity, timeslice, state):
    if state.activity == elem.home_pm_activity:
        todo_list = [elem.home_pm_activity]
    else:
        todo_list = elem.activities
    for next_actv in todo_list:
        if next_actv == elem.home_am_activity or next_actv == elem.home_pm_activity:
            location_set = [commodity.home]
        elif next_actv == elem.work_activity:
            location_set = [commodity.work]
        else: 
            location_set = next_actv.locations
    for next_zone in location_set:
        # calculate the new state variable
        next_state = State(next_actv, next_zone)
        for each_path, starting_time, travel_cost in \
            enum_path(timeslice, state.zone, next_zone):
            if util.state_optimal_util[commodity][starting_time][next_state] == float('-inf'):
                continue
            # calculate of schedule delay
            schedule_delay = 0.0
            if state.activity <> next_actv:
                schedule_delay = next_actv.calc_schedule_delay(starting_time)
            yield (Transition(next_state, each_path), 
                   starting_time, travel_cost, schedule_delay)

