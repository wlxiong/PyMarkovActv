# traffic assignment
from choice.model import Alternative
from planning.markov import Commodity
from utils.convert import min2slice
from utils.get import get_move_step
from shared.universe import conf, elem, flow, prob, util
from planning.markov import enum_commodity, enum_state, enum_transition

def build_choice_model(): 
    for person in elem.person_list:
        # root 1: residential location
        elem.person_alt[person] = Alternative(str(person), conf.THETA_travel, 0.0, None)
        # level 2: choice of making trip
        elem.out_of_home_alt[person] = Alternative('out-of-home', conf.THETA_bundle, 0.0, elem.person_alt[person])
        for bundle in elem.bundles.values():
            comm = Commodity(person, bundle)
            if bundle == elem.in_home_bundle:
                # level 2: choice of not making trip
                elem.in_home_alt[person] = Alternative('in-home', None, util.commodity_util[comm], 
                                                       elem.person_alt[person])
            else:
                # level 3: choice of activity bundle
                elem.bundle_alt[comm]    = Alternative(str(comm), None, util.commodity_util[comm], 
                                                    elem.out_of_home_alt[person])

def calc_inclusive_values():
    # calculate inclusive value
    for person in elem.person_list:
        for bundle in elem.bundles.values():
            if bundle == elem.in_home_bundle:
                # calculate expected utility for in-home choice
                util.in_home_util[person] = elem.in_home_alt[person].calc_inclusive_value()
        # calculate expected utility for out-of-home choice
        util.out_of_home_util[person] = elem.out_of_home_alt[person].calc_inclusive_value()
        # calculate expected utility for each individual
        util.person_util[person]     = elem.person_alt[person].calc_inclusive_value()
    # add the location choice results to housing alternatives
    for person in elem.person_list:
        elem.person_alt[person].volume = elem.person_flows[person]

def calc_commodity_steps():
    # calculate choice volume 
    for person in elem.person_list:
        for bundle in elem.bundles.values():
            comm = Commodity(person, bundle)
            if bundle == elem.in_home_bundle:
                flow.commodity_steps[comm] = elem.in_home_alt[person].calc_choice_volume()
            else:
                flow.commodity_steps[comm] = elem.bundle_alt[comm].calc_choice_volume()
        flow.in_home_flows[person]     = elem.in_home_alt[person].calc_choice_volume()
        flow.out_of_home_flows[person] = elem.out_of_home_alt[person].calc_choice_volume()

def add_movement_steps(path, timeslice, add_step):
    # load the path flow onto movements
    # if path is None:
    #     return
    path.get_movements(timeslice)
    for each_move in path.moves_on_path[timeslice]:
        get_move_step(each_move)
        flow.movement_steps[each_move] = flow.movement_steps[each_move] + add_step

def calc_state_flows():
    # calculate flow variables based on state optimal utility
    for comm in enum_commodity():
        # print "    %s" % comm
        # from the beginning to the ending
        for timeslice in xrange(min2slice(conf.DAY)):
            for state in enum_state(comm, timeslice):
                for transition, starting_time, cost, delay in enum_transition(comm, timeslice, state):
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
