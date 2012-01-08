# Markov decision process
import math
from utils.convert import min2slice
from shared.universe import conf, util, prob, elem, flow
from planning.markov import enum_commodity, enum_state, enum_transition

def calc_activity_choice_prob():
    # activity/zone choice probability
    for comm in enum_commodity():
        for timeslice in xrange(min2slice(conf.DAY)+1):
            for state in enum_state(comm, timeslice):
                    prob.activity_choice_prob[comm.person][timeslice][(state.activity,state.zone)] += \
                        flow.state_flows[comm][timeslice][state] / elem.person_flows[comm.person]

def calc_socio_activity_util():
    # social utility
    for person in elem.person_list:
        for other in elem.person_list:
            if (person, other) in conf.corr: 
                corr = conf.corr[(person, other)]
                for timeslice in xrange(min2slice(conf.DAY)+1):
                    for each_actv in elem.activities.values():
                        for each_zone in each_actv.locations:
                            if each_actv.is_joint:
                                util.socio_util[person][timeslice][(each_actv,each_zone)] = \
                                    prob.activity_choice_prob[other][timeslice][(each_actv,each_zone)] * \
                                    5.0 * corr * util.solo_util[timeslice][each_actv]
                            else:
                                util.socio_util[person][timeslice][(each_actv,each_zone)] = 0.0

def calc_state_util():
    math.exp = math.exp
    math.log = math.log
    # find the optimal uitility
    for comm in enum_commodity():
        print "    %s" % comm
        # backtrack from the ending to the beginning
        for timeslice in xrange(min2slice(conf.DAY)-1,-1,-1):
            for state in enum_state(comm, timeslice):
                these_util = {}
                for transition, starting_time, travel_cost, schedule_delay in \
                    enum_transition(comm, timeslice, state):
                    these_util[transition] = conf.THETA_tour * ( conf.discount * \
                        util.state_util[comm][starting_time][transition.state] + \
                        util.solo_util[timeslice][state.activity] + \
                        util.socio_util[comm.person][timeslice][(state.activity,state.zone)] - \
                        (travel_cost + schedule_delay) )
                # if these_util == [], the decision space is empty and then continue to next 
                if these_util == {}:
                    continue
                # scale the utility of each decision
                min_util = min(these_util.values())
                max_util = max(these_util.values())
                sum_exp_util = sum([math.exp(utility-(max_util+min_util)/2.0) \
                                    for utility in these_util.values()])
                # calculate the expected optimal utility
                util.state_util[comm][timeslice][state] = \
                    ((max_util+min_util)/2.0 + math.log(sum_exp_util)) / conf.THETA_tour
                # calculate the transition choice probability
                for trans, utility in these_util.items():
                    prob.transition_choice_prob[comm][timeslice][state][trans] = \
                        math.exp(utility - (max_util+min_util)/2.0) / sum_exp_util
        util.commodity_util[comm] = util.state_util[comm][0][comm.init_state]
