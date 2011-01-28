# traffic assignment
import math
from choice.model import Alternative
from planning.markov import Commodity
from opt.hitchcock import TransProblem
from utils.convert import min2slice
from utils.get import get_move_step
from shared.universe import conf, elem, flow, prob, util
from planning.markov import enum_commodity, enum_state, enum_transition

def build_choice_model(): 
    for work in elem.work_list:
        # # root 0: places of work
        # elem.work_alt[work] = Alternative(str(work), conf.THETA_location, 0.0, None, work.jobs)
        for home in elem.home_list:
            # level 1: choice of residential location 
            home_rent_util = home.rent * conf.ALPHA_rent 
            elem.housing_alt[(work, home)] = Alternative(str(home), conf.THETA_travel, home_rent_util, None)
            # level 2: choice of making trip
            elem.out_of_home_alt[(work, home)] = Alternative('out-of-home', conf.THETA_bundle, 0.0, elem.housing_alt[(work, home)])
            for bundle in elem.bundles.values():
                comm = Commodity(work, home, bundle)
                if bundle == elem.in_home_bundle:
                    # level 2: choice of not making trip
                    elem.in_home_alt[(work, home)] = Alternative('in-home', None, util.commodity_optimal_util[comm], 
                                                                 elem.housing_alt[(work, home)])
                else:
                    # level 3: choice of activity bundle
                    elem.bundle_alt[comm] = Alternative(str(comm), None, util.commodity_optimal_util[comm], 
                                                        elem.out_of_home_alt[(work, home)])

def calc_location_flows():
    # calculate inclusive value
    util_matrix = []
    for home in elem.home_list:
        util_matrix.append(list())
        for work in elem.work_list:
            for bundle in elem.bundles.values():
                if bundle == elem.in_home_bundle:
                    util.in_home_util[(work, home)] = elem.in_home_alt[(work, home)].calc_inclusive_value()
            # calculate expected utility for out-of-home
            util.out_of_home_util[(work, home)] = elem.out_of_home_alt[(work, home)].calc_inclusive_value()
            # calculate expected utility for residential location 
            util.housing_util[(work, home)]     = elem.housing_alt[(work, home)].calc_inclusive_value()
            # add entry to the utility matrix
            if math.pow(flow.housing_flows[(work, home)], 2) < 1e-4:
                util_value = -1e4
            else:
                util_value = -util.housing_util[(work, home)] + \
                              conf.THETA_location * math.log(flow.housing_flows[(work, home)])
            util_matrix[-1].append(util_value)
    # solve the distribution problem
    dist_problem = TransProblem(elem.home_list, elem.work_list, util_matrix)
    dist_problem.solve()
    flow.housing_steps = dist_problem.get_solution()
    # add the location choice results to housing alternatives
    for home in elem.home_list:
        for work in elem.work_list:
            elem.housing_alt[(work, home)].volume = flow.housing_steps[(work, home)]

def calc_commodity_flows():
    # calculate choice volume 
    for work in elem.work_list:
        for home in elem.home_list:
            for bundle in elem.bundles.values():
                comm = Commodity(work, home, bundle)
                if bundle == elem.in_home_bundle:
                    flow.commodity_steps[comm] = elem.in_home_alt[(work, home)].calc_choice_volume()
                else:
                    flow.commodity_steps[comm] = elem.bundle_alt[comm].calc_choice_volume()
            flow.in_home_flows[(work, home)]     = elem.in_home_alt[(work, home)].calc_choice_volume()
            flow.out_of_home_flows[(work, home)] = elem.out_of_home_alt[(work, home)].calc_choice_volume()
            # flow.housing_flows[(work, home)]     = elem.housing_alt[(work, home)].calc_choice_volume()

def add_movement_steps(path, timeslice, add_step):
    # load the path flow onto movements
    path.get_movements(timeslice)
    for each_move in path.moves_on_path[timeslice]:
        get_move_step(each_move)
        flow.movement_steps[each_move] = flow.movement_steps[each_move] + add_step

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
                        flow.state_flows[comm][timeslice][state] * \
                        prob.transition_choice_prob[comm][timeslice][state][transition]
                    # add transition flows to edge steps
                    add_movement_steps(transition.path, timeslice, \
                        flow.transition_flows[comm][timeslice][state][transition])
                    # update state flows
                    flow.state_flows[comm][starting_time][transition.state] = \
                        flow.state_flows[comm][starting_time][transition.state] + \
                        flow.transition_flows[comm][timeslice][state][transition]
