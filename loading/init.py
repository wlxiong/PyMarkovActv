# initialize variables
from utils.convert import min2slice
from shared.universe import conf, elem, flow, prob, util
from planning.markov import enum_commodity, enum_state, enum_transition

def init_activity_choice_prob():
    prob.activity_choice_prob = {}
    for person in elem.person_list:
        prob.activity_choice_prob[person] = {}
        for timeslice in xrange(min2slice(conf.DAY)+1):
            prob.activity_choice_prob[person][timeslice] = {}
            for each_actv in elem.activities.values():
                for each_zone in each_actv.locations:
                    prob.activity_choice_prob[person][timeslice][(each_actv,each_zone)] = 0.0

def init_socio_activity_util():
    util.socio_util = {}
    for person in elem.person_list:
        util.socio_util[person] = {}
        for timeslice in xrange(min2slice(conf.DAY)+1):
            util.socio_util[person][timeslice] = {}
            for each_actv in elem.activities.values():
                for each_zone in each_actv.locations:
                    util.socio_util[person][timeslice][(each_actv,each_zone)] = 0.0

def init_state_util():
    util.state_util = {}
    for comm in enum_commodity():
        util.state_util[comm] = {}
        for timeslice in xrange(min2slice(conf.DAY)+1):
            util.state_util[comm][timeslice] = {}
            for state in enum_state(comm, timeslice):
                # flag the states that has not been visited by 
                # setting the state utilities to negative infinity
                util.state_util[comm][timeslice][state] = float('-inf')
        # initialize the value of terminal state to zeros
        # and the backward recursive process starts here
        util.state_util[comm][min2slice(conf.DAY)][comm.term_state] = 0.0

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

def init_transition_choice_prob():
    prob.transition_choice_prob = {}
    for comm in enum_commodity():
        prob.transition_choice_prob[comm] = {}
        for timeslice in xrange(min2slice(conf.DAY)):
            prob.transition_choice_prob[comm][timeslice] = {}
            for state in enum_state(comm, timeslice):
                prob.transition_choice_prob[comm][timeslice][state] = {}
                for transition_info in enum_transition(comm, timeslice, state):
                    transition = transition_info[0]
                    prob.transition_choice_prob[comm][timeslice][state][transition] = 0.0

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

def init_activity_population(init_value):
    flow.activity_population = {}
    for timeslice in xrange(min2slice(conf.DAY)+1):
        flow.activity_population[timeslice] = {}
        for each_actv in elem.activities.values():
            flow.activity_population[timeslice][each_actv] = init_value

def init_static_population(init_values):
    flow.static_population = {}
    for comm in enum_commodity():
        flow.static_population[comm] = {}
        for timeslice in xrange(min2slice(conf.DAY)+1):
            flow.static_population[comm][timeslice] = 0.0
    
def init_step_variables():
    # clear movements in each path
    for origin in elem.zone_list:
        for dest in elem.zone_list:
            elem.shortest_path[origin][dest].init_movements()
    flow.movement_steps = {}
    flow.commodity_steps = {}

def init_flow_variables():
    flow.movement_flows = {}
    flow.commodity_flows = {}
    for comm in enum_commodity():
        flow.commodity_flows[comm] = 0.0
