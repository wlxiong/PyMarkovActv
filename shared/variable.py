# Utilities, probabilites and flows 

class UtilVar(object):
    def __init__(self):
        # 2-dimension nested dict 
        # i.e. solo_util[timeslice][activity]
        self.solo_util = {}
        # 3-dimension nested dict 
        # i.e. socio_util[person][timeslice][(activity,zone)]
        self.socio_util = {}
        # 3-dimension nested dict
        # i.e. state_util[commodity][timeslice][state]
        # the expected maximum utility: E{max_d {V_d} }
        self.state_util = {}
        # 1-dimension dict, i.e. commodity_util[commodity]
        self.commodity_util = {}
        # expected utility for all out-of-home patterns
        # 1-dimension dict, i.e. out_of_home_util[person]
        self.out_of_home_util = {}
        # expected utility for in-home pattern
        # 1-dimension dict, i.e. in_home_util[person]
        self.in_home_util = {}
        # expected utility for each individual
        # 1-dimension dict, i.e. person_util[person]
        self.person_util = {}


class ProbVar(object):
    def __init__(self):
        # # in-home pattern choice probability
        # # 1-dimension dict, i.e. in_home_choice_prob[person]
        # self.in_home_choice_prob = {}
        # # out-of-home pattern choice probability 
        # # 1-dimension dict, i.e. out_of_home_choice_prob[person]
        # self.out_of_home_choice_prob = {}
        # # 1-dimension dict, i.e. commodity_choice_probc[comm]
        # self.commodity_choice_prob = {}

        # 4-dimension nested dict
        # i.e. transition_choice_prob[commodity][timeslice][state][transition]
        self.transition_choice_prob = {}
        
        # 3-dimension nested dict
        # i.e. activity_choice_prob[person][timeslice][(activity,zone)]
        self.activity_choice_prob = {}

class FlowVar(object):
    """ The world of the economic activities and transport network. 
        The variables in this class define the rules of this world.
    """
    def __init__(self):
        
        # assginment
        # 1-dimension dict, i.e. movement_flows[move]
        self.movement_flows = {}
        self.movement_steps = {}
        # 4-dimension nested dict
        # i.e. transition_flows[commodity][timeslice][state][transition]
        self.transition_flows = {}
        # 3-dimension nested dict
        # i.e. state_flows[commodity][timeslice][state]
        self.state_flows = {}
        # 2-dimension neested dict 
        # i.e. static_population[commodity_flows][timeslice]
        self.static_population = {}
        # 1-dimension dict, i.e. commodity_flows[commodity]
        self.commodity_flows = {}
        self.commodity_steps = {}
        # 1-dimension dict, i.e. in_home_flows[person]
        self.in_home_flows = {}
        # 1-dimension dict, i.e. out_of_home_flows[person]
        self.out_of_home_flows = {}
        # # 3-dimension nested dict
        # # i.e. OD_trips[timeslice][origin][destination]
        # self.OD_trips = {}
        # 2-dimension nested dict
        # i.e. zone_population[timeslice][zone]
        self.zone_population = {}
        # 2-dimension nested dict
        # i.e. activity_population[timeslice][activity]
        self.activity_population = {}

        ## export to MATLAB
        ## mat_pattern_flow = [None] * num_sample
        ## mat_zone_passenger = [None] * num_sample
        ## mat_aggrg_trip = [None] * num_sample

class StatVar(object):
    """ The statistics generated from multipe scenarios
    """
    def __init__(self):
        self.joint_time_use = {}
        self.joint_activity_duration = {}
        self.indep_activity_duration = {}
        self.average_travel_time = {}
        self.out_of_home_flows = {}
        self.in_home_flows = {}
        self.person_util = {}

