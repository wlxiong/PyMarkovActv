# some statistics for the simulation
from shared.universe import conf, flow
from planning.markov import enum_commodity, enum_state, enum_transition
from utils.convert import min2slice

def calc_average_activity_duration(commodity):
    sum_duration = {}
    average_duration = {}
    for activity in commodity.bundle.activity_set:
        sum_duration[activity] = 0.0
        average_duration[activity] = 0.0
    for timeslice in xrange(min2slice(conf.DAY)):
        for state in enum_state(commodity, timeslice):
            sum_duration[state.activity] += flow.state_flows[commodity][timeslice][state]
    for activity in commodity.bundle.activity_set:
        sum_duration[activity] = sum_duration[activity] * conf.TICK
        average_duration[activity] = sum_duration[activity] / flow.commodity_flows[commodity]
    nontravel_duration = sum(average_duration.values())
    average_duration['travel'] = 1440 - nontravel_duration
    return average_duration

def calc_aggregate_flows():
    # calculate aggregate flow variables based on transition flows
    for comm in enum_commodity():
        # from the beginning to the ending
        for timeslice in xrange(min2slice(conf.DAY)):
            for state in enum_state(comm, timeslice):
                for transition_info in enum_transition(comm, timeslice, state):
                    transition = transition_info[0]
                    starting_time = transition_info[1]
                    # calculate zone population
                    flow.zone_population[starting_time][transition.state.zone] = \
                        flow.zone_population[starting_time][transition.state.zone] + \
                        flow.transition_flows[comm][timeslice][state][transition]
                    # calculate activity population
                    flow.actv_population[starting_time][transition.state.activity] = \
                        flow.actv_population[starting_time][transition.state.activity] + \
                        flow.transition_flows[comm][timeslice][state][transition]
                    # calculate O-D trips
                    flow.OD_trips[timeslice][state.zone][transition.state.zone] = \
                        flow.OD_trips[timeslice][state.zone][transition.state.zone] + \
                        flow.transition_flows[comm][timeslice][state][transition]

def calc_activity_duration_variance():
    pass

def calc_average_wait_time():
    pass

def calc_average_schedule_delay():
    pass

