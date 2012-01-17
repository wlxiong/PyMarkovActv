import hashlib
from shared.universe import conf, elem, util
from utils.convert import min2slice
from itertools import combinations

#class InitDict(dict):
#    def __init__(self, default = None):
#        self.default = default
#
#    def __getitem__(self, key):
#        if not self.has_key(key):
#            self[key] = self.default()
#        return dict.__getitem__(self, key)


class Commodity(object):
    """ The commodity is the cross product of the set of household members and the set of activity bundles.
        Or the activity bundles are enumerated implicitly.
    """
    def __init__(self, person, bundle):
        self.person, self.bundle = person, bundle
        self.work, self.home = person.work, person.home
        self.id = "%s>%s" % (self.person, self.bundle)
        self.init_state = State(elem.home_am_activity, self.home, self.bundle.activity_set)
        self.term_state = State(elem.home_pm_activity, self.home, frozenset([elem.home_pm_activity]))

    def __repr__(self):
        return self.id

    def __hash__(self):
        # return int(hashlib.md5(repr(self)).hexdigest(), 16)
        return hash(repr(self))

    def __eq__(self, other):
        return self.person == other.person and \
               self.bundle == other.bundle


class State(object):
    """ The state contains the position of the traveler (zone), the activity participated
        and --lagged variable (autoregressive process)--, excluding timeslice.
    """
    def __init__(self, activity, zone, todo):
        self.zone, self.activity, self.todo = zone, activity, todo

    def __repr__(self):
        return "%s-%s-%s" % (self.zone, self.activity, sorted(self.todo))

    def __hash__(self):
        # return int(hashlib.md5(repr(self)).hexdigest(), 16)
        return hash(repr(self))

    def __eq__(self, other):
        return self.activity == other.activity and \
               self.zone == other.zone and \
               self.todo == other.todo


class Transition(object):
    """ Transition defines the next state according to current state, including timeslice.
    """
    def __init__(self, state, path):
        self.state, self.path = state, path

    def __repr__(self):
        return "%s-%s" % (self.state, self.path)

    def __hash__(self):
        # return int(hashlib.md5(repr(self)).hexdigest(), 16)
        return hash(repr(self))

    def __eq__(self, other):
        return self.state == other.state and \
               self.path == other.path

def enum_commodity():
    # for different work-home location and activity bundles
    for person in elem.person_list:
        for bundle in elem.bundles.values():
            yield Commodity(person, bundle)

def enum_state(commodity, timeslice):
    activity_bundle = commodity.bundle.activity_set
    indoor_activities = [elem.home_am_activity, elem.home_pm_activity]
    outdoor_activities = activity_bundle.difference(indoor_activities)
    # yield a state with all activities
    yield commodity.init_state
    # yield states with different number of activities
    for N in xrange(len(outdoor_activities)):
        # generate different combinations from the N activities
        for todo_list in combinations(outdoor_activities, N+1):
            todo_set = frozenset(todo_list + (elem.home_pm_activity , ))
            # pick up each activity in the todo list
            for each_actv in todo_list:
                # choose one location for the activity
                for position in each_actv.locations:
                    yield State(each_actv, position, todo_set)
    # yield a state with the last activity: in-home activity in PM
    yield commodity.term_state

def enum_path(timeslice, this_zone, next_zone):
    shortest_path = elem.shortest_path[this_zone][next_zone]
    travel_timeslice, travel_cost = shortest_path.calc_travel_impedences(timeslice)
    arrival_timeslice = timeslice + travel_timeslice
    starting_time = arrival_timeslice + 1
    if starting_time > min2slice(conf.DAY):
        return
    yield shortest_path, starting_time, travel_cost

def enum_transition(commodity, timeslice, state):
    for next_actv in state.todo:
        if next_actv.time_win[0] > timeslice or \
           timeslice > next_actv.time_win[1]:
            continue
        if next_actv == elem.home_pm_activity and len(state.todo) > 2:
            continue
        else:
            if next_actv == elem.home_am_activity or next_actv == elem.home_pm_activity:
                location_set = [commodity.home]
            elif next_actv == elem.work_activity:
                location_set = [commodity.work]
            elif next_actv == state.activity:
                location_set = [state.zone]
            else:
                location_set = next_actv.locations
        if next_actv <> state.activity:
            next_todo = state.todo.difference([state.activity])
        else:
            next_todo = state.todo
        for next_zone in location_set:
            # calculate the new state variable
            next_state = State(next_actv, next_zone, next_todo)
            for each_path, starting_time, travel_cost in \
                enum_path(timeslice, state.zone, next_zone):
                if util.state_util[commodity][starting_time][next_state] == float('-inf'):
                    continue
                # calculate of schedule delay
                schedule_delay = 0.0
                if state.activity <> next_actv:
                    schedule_delay = next_actv.calc_schedule_delay(starting_time)
                yield (Transition(next_state, each_path),
                       starting_time, travel_cost, schedule_delay)
