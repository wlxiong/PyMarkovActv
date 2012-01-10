# some statistics for the simulation
from shared.universe import conf, flow, util, elem, prob
from planning.markov import enum_commodity, enum_state
from loading.init import init_zone_population, init_activity_population, init_static_population
from utils.convert import min2slice

def calc_average_activity_duration(commodity):
    average_activity_duration = {}
    # initialize average duration
    for activity in commodity.bundle.activity_set:
        average_activity_duration[activity] = 0.0
    # average duration
    for timeslice in xrange(min2slice(conf.DAY)):
        for state in enum_state(commodity, timeslice):
            average_activity_duration[state.activity] += conf.TICK * \
                flow.state_flows[commodity][timeslice][state] / flow.commodity_steps[commodity]
    # average travel time
    average_travel_time = 1440 - sum(average_activity_duration.values())
    return average_activity_duration, average_travel_time

def calc_joint_time_use():
    calc_joint_time_use = {}
    for person in elem.person_list:
        calc_joint_time_use[person] = 0.0
        for other in elem.person_list:
            if (person, other) in conf.corr: 
                for timeslice in xrange(min2slice(conf.DAY)):
                    for each_actv in elem.activities.values():
                        for each_zone in each_actv.locations:
                            if each_actv.is_joint:
                                calc_joint_time_use[person] += conf.TICK * \
                                prob.activity_choice_prob[other][timeslice][(each_actv,each_zone)]
    return calc_joint_time_use

def calc_average_temporal_util(commodity):
    average_temporal_utility = {}
    average_travel_disutil = {}
    for timeslice in xrange(min2slice(conf.DAY)+1):
        # initialize temporal utility
        average_temporal_utility[timeslice] = 0.0
        for state in enum_state(commodity, timeslice):
            # average temporal utility 
            average_temporal_utility[timeslice] += (util.solo_util[timeslice][state.activity] + \
                util.socio_util[commodity.person][timeslice][(state.activity,state.zone)])* \
                flow.state_flows[commodity][timeslice][state] / flow.commodity_steps[commodity]
    # travel disutility
    for timeslice in xrange(min2slice(conf.DAY)+1):
        average_travel_disutil[timeslice] = (flow.commodity_steps[commodity] - \
                                             flow.static_population[commodity][timeslice]) * \
                                             conf.ALPHA_car / flow.commodity_steps[commodity]
    return average_temporal_utility, average_travel_disutil

def calc_population_flows():
    # initialize the population flows
    init_zone_population(0.0)
    init_activity_population(0.0)
    init_static_population(0.0)
    # calculate population flow variables based on state flows
    for comm in enum_commodity():
        for timeslice in xrange(min2slice(conf.DAY)+1):
            for state in enum_state(comm, timeslice):
                # calculate static population
                flow.static_population[comm][timeslice] += \
                    flow.state_flows[comm][timeslice][state]
                # calculate zone population
                flow.zone_population[timeslice][state.zone] += \
                    flow.state_flows[comm][timeslice][state]
                # calculate activity population
                flow.activity_population[timeslice][state.activity] += \
                    flow.state_flows[comm][timeslice][state]
