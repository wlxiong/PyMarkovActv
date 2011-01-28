# initialize variables
from utils.convert import min2slice
from shared.universe import conf, elem, flow, prob, util
from planning.markov import enum_commodity, enum_state, enum_transition

def init_state_optimal_util(init_value):
    util.state_optimal_util = {}
    for comm in enum_commodity():
        util.state_optimal_util[comm] = {}
        for timeslice in xrange(min2slice(conf.DAY)+1):
            util.state_optimal_util[comm][timeslice] = {}
            for state in enum_state(comm, timeslice):
                util.state_optimal_util[comm][timeslice][state] = init_value
        # initialize the value of terminal state
        util.state_optimal_util[comm][min2slice(conf.DAY)][comm.term_state] = 0.0

def init_state_flows(init_value):
    flow.state_flows = {}
    for comm in enum_commodity():
        flow.state_flows[comm] = {}
        for timeslice in xrange(min2slice(conf.DAY)+1):
            flow.state_flows[comm][timeslice] = {}
            for state in enum_state(comm, timeslice):
                flow.state_flows[comm][timeslice][state] = init_value
    # initialize the population at timeslice 0 for each zone
    for comm in enum_commodity():
        flow.state_flows[comm][0][comm.init_state] = flow.commodity_steps[comm]

def init_transition_flows(init_value):
    flow.transition_flows = {}
    for comm in enum_commodity():
        flow.transition_flows[comm] = {}
        for timeslice in xrange(min2slice(conf.DAY)):
            flow.transition_flows[comm][timeslice] = {}
            for state in enum_state(comm, timeslice):
                flow.transition_flows[comm][timeslice][state] = {}
                for transition_info in enum_transition(comm, timeslice, state):
                    transition = transition_info[0]
                    flow.transition_flows[comm][timeslice][state][transition] = init_value

def init_transition_choice_prob(init_value):
    prob.transition_choice_prob = {}
    for comm in enum_commodity():
        prob.transition_choice_prob[comm] = {}
        for timeslice in xrange(min2slice(conf.DAY)):
            prob.transition_choice_prob[comm][timeslice] = {}
            for state in enum_state(comm, timeslice):
                prob.transition_choice_prob[comm][timeslice][state] = {}
                for transition_info in enum_transition(comm, timeslice, state):
                    transition = transition_info[0]
                    prob.transition_choice_prob[comm][timeslice][state][transition] = init_value

def init_OD_trips(init_value):
    flow.OD_trips = {}
    for timeslice in xrange(min2slice(conf.DAY)+1):
        flow.OD_trips[timeslice] = {}
        for zone_a in elem.zone_list:
            flow.OD_trips[timeslice][zone_a] = {}
            for zone_b in elem.zone_list:
                flow.OD_trips[timeslice][zone_a][zone_b] = init_value

def init_zone_population(init_value):
    flow.zone_population = {}
    for timeslice in xrange(min2slice(conf.DAY)+1):
        flow.zone_population[timeslice] = {}
        for zone in elem.zone_list:
            flow.zone_population[timeslice][zone] = init_value

def init_actv_population(init_value):
    flow.actv_population = {}
    for timeslice in xrange(min2slice(conf.DAY)+1):
        flow.actv_population[timeslice] = {}
        for each_actv in elem.activities.values():
            flow.actv_population[timeslice][each_actv] = init_value

def init_step_variables():
    # clear movements in each path
    for origin in elem.zone_list:
        for dest in elem.zone_list:
            for path in elem.paths[origin][dest]:
                path.init_movements()
    flow.movement_steps = {}
    flow.commodity_steps = {}
    flow.housing_steps = {}

def init_flow_variables():
    flow.movement_flows = {}
    
    flow.commodity_flows = {}
    for comm in enum_commodity():
        flow.commodity_flows[comm] = 0.0
        
    flow.housing_flows = {}
    for home in elem.home_list:
        for work in elem.work_list:
            flow.housing_flows[(work, home)] = work.jobs * float(len(elem.home_list))
