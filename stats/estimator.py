# some statistics for the simulation
from shared.universe import conf, flow
from planning.markov import enum_state
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

def calc_activity_duration_variance():
    pass

def calc_average_wait_time():
    pass

def calc_average_schedule_delay():
    pass

