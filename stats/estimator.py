# some statistics for the simulation
from shared.universe import conf, flow, util
from planning.markov import enum_commodity, enum_state
from loading.init import init_OD_trips, init_zone_population, init_actv_population
from utils.convert import min2slice
from stats.timer import print_current_time

def calc_average_activity_duration(commodity):
    sum_duration = {}
    average_duration = {}
    # initialize total duration
    for activity in commodity.bundle.activity_set:
        sum_duration[activity] = 0.0
    # total duration
    for timeslice in xrange(min2slice(conf.DAY)+1):
        for state in enum_state(commodity, timeslice):
            sum_duration[state.activity] += conf.TICK * \
                                            flow.state_flows[commodity][timeslice][state]
    # average duration
    for activity in commodity.bundle.activity_set:
        average_duration[activity] = sum_duration[activity] / flow.commodity_steps[commodity]
    # average travel time
    average_travel_time = 1440 - sum(average_duration.values())
    # subtotal for joint and independent activities
    average_duration['joint-activity'] = 0.0
    average_duration['indep-activity'] = 0.0
    for each_actv in commodity.bundle.activity_set:
        if each_actv.is_joint:
            average_duration['joint-activity'] += average_duration[each_actv]
        else: 
            average_duration['indep-activity'] += average_duration[each_actv]
    return average_duration, average_travel_time

def calc_average_temporal_util(commodity):
    sum_utility = {}
    average_utility = {}
    average_travel_disutil = {}
    # total utility 
    for timeslice in xrange(min2slice(conf.DAY)+1):
        sum_utility[timeslice] = 0.0
        for state in enum_state(commodity, timeslice):
            sum_utility[timeslice] += util.activity_util[timeslice][state.activity] * \
                                      flow.state_flows[commodity][timeslice][state]
    # average utility
    for timeslice in xrange(min2slice(conf.DAY)+1):
        average_utility[timeslice] = sum_utility[timeslice] / flow.commodity_steps[commodity]
    for timeslice in xrange(min2slice(conf.DAY)+1):
        average_travel_disutil[timeslice] = (flow.commodity_steps[commodity] - \
                                             flow.temporal_flows[commodity][timeslice]) * \
                                             conf.ALPHA_car / flow.commodity_steps[commodity]
    return average_utility, average_travel_disutil

def calc_aggregate_flows():
    # initialize the aggregate flows
    init_zone_population(0.0)
    print '  init_zone_population(0.0)'
    print_current_time()
    init_actv_population(0.0)
    print '  init_actv_population(0.0)'
    print_current_time()
    init_OD_trips(0.0)
    print '  init_OD_trips(0.0)'
    print_current_time()
    # calculate aggregate flow variables based on transition flows
    flow.temporal_flows = {}
    for comm in enum_commodity():
        flow.temporal_flows[comm] = {}
        # from the beginning to the ending
        for timeslice in xrange(min2slice(conf.DAY)+1):
            flow.temporal_flows[comm][timeslice] = 0.0
            for state in enum_state(comm, timeslice):
                # calculate temporal flows
                flow.temporal_flows[comm][timeslice] += \
                    flow.state_flows[comm][timeslice][state]
                # calculate zone population
                flow.zone_population[timeslice][state.zone] =+ \
                    flow.state_flows[comm][timeslice][state]
                # calculate activity population
                flow.actv_population[timeslice][state.activity] =+ \
                    flow.state_flows[comm][timeslice][state]
    print '  calc_aggregate_flows()'
    print_current_time()

def calc_activity_duration_variance():
    pass

def calc_average_wait_time():
    pass

def calc_average_schedule_delay():
    pass
