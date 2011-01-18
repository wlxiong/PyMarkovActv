# traffic assignment
from utils.convert import min2slice
from utils.get import get_move_step
from shared.universe import conf, elem, flow, prob
from planning.markov import enum_commodity, enum_state, enum_transition

def add_movement_step(path, timeslice, add_step):
    # load the path flow onto movements
    path.get_movements(timeslice)
    for each_move in path.moves_on_path[timeslice]:
        get_move_step(each_move)
        flow.movement_steps[each_move] = flow.movement_steps[each_move] + add_step

def calc_commodity_flow():
    for comm in enum_commodity():
        if comm.bundle == elem.in_home_bundle:
            flow.commodity_flows[comm] = \
                comm.home.population * prob.in_home_choice_prob[comm.home]
        else:
            flow.commodity_flows[comm] = \
                comm.home.population * (1.0 - prob.in_home_choice_prob[comm.home]) * \
                prob.bundle_choice_prob[comm.home][comm.bundle]

def calc_state_flows():
    # calculate flow variables based on state optimal utility
    for comm in enum_commodity():
        print "   commodity %s" % comm
        # backtrack from the ending to the beginning
        for timeslice in xrange(min2slice(conf.DAY)):
            for state in enum_state(comm, timeslice):
                for transition_info in enum_transition(comm, timeslice, state):
                    transition = transition_info[0]
                    starting_time = transition_info[1]
                    # calculate transition flows
                    flow.transition_flows[comm][timeslice][state][transition] = \
                        flow.state_flows[comm][timeslice][state] * \
                        prob.transition_choice_prob[comm][timeslice][state][transition]
                    # add transition flows to edge steps
                    add_movement_step(transition.path, timeslice, \
                        flow.transition_flows[comm][timeslice][state][transition])
                    # update state flows
                    flow.state_flows[comm][starting_time][transition.state] = \
                        flow.state_flows[comm][starting_time][transition.state] + \
                        flow.transition_flows[comm][timeslice][state][transition]
                    # update zone population
                    flow.zone_population[starting_time][transition.state.zone] = \
                        flow.zone_population[starting_time][transition.state.zone] + \
                        flow.transition_flows[comm][timeslice][state][transition]
                    # update activity population
                    flow.actv_population[starting_time][transition.state.activity] = \
                        flow.actv_population[starting_time][transition.state.activity] + \
                        flow.transition_flows[comm][timeslice][state][transition]
                    # update O-D trips
                    flow.OD_trips[timeslice][state.zone][transition.state.zone] = \
                        flow.OD_trips[timeslice][state.zone][transition.state.zone] + \
                        flow.transition_flows[comm][timeslice][state][transition]
