# traffic assignment
import math
from choice.model import Alternative
from planning.markov import Commodity
from opt.hitchcock import TransProblem
from utils.convert import min2slice
from utils.get import get_move_step
from shared.universe import conf, elem, flow, prob, util
from planning.markov import enum_commodity, enum_state, enum_transition


def calc_location_flows():
    # calculate inclusive value
    util_matrix = []
    for home in elem.home_list:
        util_matrix.append(list())
        for work in elem.work_list:
            comm = Commodity(work, home)
            # calculate expected utility for residential location 
            util.housing_util[(work, home)] = util.commodity_optimal_util[comm]
            # add entry to the utility matrix
            util_value = -util.housing_util[(work, home)] + \
                          conf.THETA_location * math.log(flow.housing_flows[(work, home)])
            util_matrix[-1].append(util_value)

    housing_util_local  = util.housing_util
    housing_flows_local = flow.housing_flows
    # solve the distribution problem 
    dist_problem = TransProblem(elem.home_list, elem.work_list, util_matrix)
    dist_problem.solve()
    flow.housing_steps = dist_problem.get_solution()
    # print util.housing_util
    # print flow.housing_flows
    # print flow.housing_steps

def calc_commodity_flows():
    # calculate choice volume 
    for comm in enum_commodity():
        flow.commodity_steps[comm] = flow.housing_steps[(comm.work, comm.home)]

def add_movement_steps(path, timeslice, add_step):
    # load the path flow onto movements
    path.get_movements(timeslice)
    for each_move in path.moves_on_path[timeslice]:
        get_move_step(each_move)
        flow.movement_steps[each_move] += add_step

def calc_state_flows():
    # calculate flow variables based on state optimal utility
    for comm in enum_commodity():
        print "    %s" % comm
        # from the beginning to the ending
        for timeslice in xrange(min2slice(conf.DAY)):
            for state in enum_state(comm, timeslice):
                for transition_info in enum_transition(comm, timeslice, state):
                    transition = transition_info[0]
                    starting_time = transition_info[1]
                    # calculate transition flows
                    flow.transition_flows[comm][timeslice][state][transition] = \
                        flow.state_steps[comm][timeslice][state] * \
                        prob.transition_choice_prob[comm][timeslice][state][transition]
                    # add transition flows to edge steps
                    add_movement_steps(transition.path, timeslice, \
                        flow.transition_flows[comm][timeslice][state][transition])
                    # update state flows
                    flow.state_steps[comm][starting_time][transition.state] = \
                        flow.state_steps[comm][starting_time][transition.state] + \
                        flow.transition_flows[comm][timeslice][state][transition]
