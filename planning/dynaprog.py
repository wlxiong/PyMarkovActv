# semi-Markov decision process
import math
from utils.convert import min2slice
from shared.universe import conf, util, prob, elem
from planning.markov import Commodity
from planning.markov import enum_commodity, enum_state, enum_transition

def calc_state_optimal_util():
    mexp = math.exp
    mlog = math.log
    # find the optimal uitility
    for comm in enum_commodity():
        print "   commodity %s" % comm
        # backtrack from the ending to the beginning
        for timeslice in xrange(min2slice(conf.DAY)-1,-1,-1):
            for state in enum_state(comm, timeslice):
                these_util = {}
                for transition, starting_time, travel_cost, schedule_delay in \
                    enum_transition(comm, timeslice, state):
#                    if util.state_optimal_util[comm][starting_time][transition.state] == float('-inf'):
#                        continue
                    these_util[transition] = conf.THETA_tour * ( conf.discount * \
                        util.state_optimal_util[comm][starting_time][transition.state] + \
                        util.activity_util[timeslice][state.activity] - \
                        travel_cost - schedule_delay)
                # if these_util == [], the decision space is empty and then continue to next 
                if these_util == {}:
                    continue
                # scale the utility of each decision
                min_util = min(these_util.values())
                max_util = max(these_util.values())
                sum_exp_util = sum([mexp(utility-(max_util+min_util)/2.0) \
                                    for utility in these_util.values()])
                # calculate the expected optimal utility
                util.state_optimal_util[comm][timeslice][state] = \
                    ((max_util+min_util)/2.0 + mlog(sum_exp_util)) / conf.THETA_tour
                # calculate the transition choice probability
                for trans, utility in these_util.items():
                    prob.transition_choice_prob[comm][timeslice][state][trans] = \
                        mexp(utility - (max_util+min_util)/2.0) / sum_exp_util
        util.commodity_optimal_util[comm] = util.state_optimal_util[comm][0][comm.init_state]

def calc_bundle_choice_prob():
    mexp = math.exp
    mlog = math.log
    for home in elem.home_list:
        # calculate in-home utility
        in_home_commodity = Commodity(home, elem.in_home_bundle)
        util.in_home_util[home] = util.commodity_optimal_util[in_home_commodity]
        # calculate out-of-home utility
        # -1.0 is used to canceled the utility of in-home bundle
        sum_commodity_util = -1.0
        for bundle in elem.bundles.values():
            out_of_home_commodity = Commodity(home, bundle)
            sum_commodity_util += mexp(conf.THETA_bundle * ( \
                                       util.commodity_optimal_util[out_of_home_commodity] - \
                                       util.commodity_optimal_util[in_home_commodity]))
        util.out_of_home_util[home] = util.commodity_optimal_util[in_home_commodity] + \
                                      mlog(sum_commodity_util) / conf.THETA_bundle
        # calculate choice probability for in-home bundle
        prob.in_home_choice_prob[home] = mexp(conf.THETA_travel * util.in_home_util[home]) / \
            (mexp(conf.THETA_travel * util.out_of_home_util[home]) + mexp(conf.THETA_travel * util.in_home_util[home]))
        # calculate choice probability for out-of-home bundles
        prob.bundle_choice_prob[home] = {}
        for bundle in elem.bundles.values():
            if bundle == elem.in_home_bundle:
                continue
            out_of_home_commodity = Commodity(home, bundle)
            prob.bundle_choice_prob[home][bundle] = \
                mexp(conf.THETA_bundle * util.commodity_optimal_util[out_of_home_commodity]) / \
                mexp(conf.THETA_bundle * util.out_of_home_util[home])
