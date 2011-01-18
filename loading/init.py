# initialize variables
from utils.convert import min2slice
from shared.universe import conf, elem, flow, prob, util
from planning.markov import enum_commodity, enum_state, enum_transition

def init_state_optimal_util(init_value):
    for comm in enum_commodity():
        util.state_optimal_util[comm] = []
        for timeslice in xrange(min2slice(conf.DAY)+1):
            util.state_optimal_util[comm].append( dict())
            for state in enum_state(comm, timeslice):
                util.state_optimal_util[comm][timeslice][state] = init_value
        # initialize the value of terminal state
        util.state_optimal_util[comm][min2slice(conf.DAY)][comm.term_state] = 0.0

def init_state_flows(init_value):
    for comm in enum_commodity():
        flow.state_flows[comm] = []
        for timeslice in xrange(min2slice(conf.DAY)+1):
            flow.state_flows[comm].append( dict())
            for state in enum_state(comm, timeslice):
                flow.state_flows[comm][timeslice][state] = init_value
    # initialize the population at timeslice 0 for each zone
    for comm in enum_commodity():
        flow.state_flows[comm][0][comm.init_state] = flow.commodity_flows[comm]

def init_transition_flows(init_value):
    for comm in enum_commodity():
        flow.transition_flows[comm] = []
        for timeslice in xrange(min2slice(conf.DAY)):
            flow.transition_flows[comm].append( dict())
            for state in enum_state(comm, timeslice):
                flow.transition_flows[comm][timeslice][state] = {}
                for transition_info in enum_transition(comm, timeslice, state):
                    transition = transition_info[0]
                    flow.transition_flows[comm][timeslice][state][transition] = init_value

def init_transition_choice_prob(init_value):
    for comm in enum_commodity():
        prob.transition_choice_prob[comm] = []
        for timeslice in xrange(min2slice(conf.DAY)):
            prob.transition_choice_prob[comm].append( dict())
            for state in enum_state(comm, timeslice):
                prob.transition_choice_prob[comm][timeslice][state] = {}
                for transition_info in enum_transition(comm, timeslice, state):
                    transition = transition_info[0]
                    prob.transition_choice_prob[comm][timeslice][state][transition] = init_value

def init_OD_trips(init_value):
    for timeslice in xrange(min2slice(conf.DAY)+1):
        flow.OD_trips.append( dict())
        for zone_a in elem.zone_list:
            flow.OD_trips[timeslice][zone_a] = {}
            for zone_b in elem.zone_list:
                flow.OD_trips[timeslice][zone_a][zone_b] = init_value

def init_zone_population(init_value):
    for timeslice in xrange(min2slice(conf.DAY)+1):
        flow.zone_population.append( dict())
        for zone in elem.zone_list:
            flow.zone_population[timeslice][zone] = init_value

def init_actv_population(init_value):
    for timeslice in xrange(min2slice(conf.DAY)+1):
        flow.actv_population.append( dict())
        for each_actv in elem.activities.values():
            flow.actv_population[timeslice][each_actv] = init_value

def init_movement_steps():
    flow.movement_steps = {}
    for origin in elem.zone_list:
        for dest in elem.zone_list:
            for path in elem.paths[origin][dest]:
                path.init_movements()

def init_movement_flows():
    flow.movement_flows = {}

