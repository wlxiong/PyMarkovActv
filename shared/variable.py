# Utilities, probabilites and flows 

class UtilVar(object):
    def __init__(self):
        # 2-dimension nested dict 
        # i.e. activity_util[timeslice][activity_name]
        self.activity_util = {}
        # 3-dimension nested dict
        # i.e. state_optimal_util[commodity][timeslice][state]
        # the expected maximum utility: E{max_d {V_d} }
        self.state_optimal_util = {}
        # 1-dimension dict, i.e. commodity_optimal_util[commodity]
        self.commodity_optimal_util = {}
        # expected utility for all out-of-home patterns
        # 1-dimension dict, i.e. out_of_home_util[(work, home)]
        self.out_of_home_util = {}
        # expected utility for in-home pattern
        # 1-dimension dict, i.e. in_home_util[(work, home)]
        self.in_home_util = {}
        # expected utility for residential location 
        # 1-dimension dict, i.e. housing_util[(work, home)]
        self.housing_util = {}


class ProbVar(object):
    def __init__(self):
        # residential location choice probability
        # 1-dimension choice probability, i.e. housing_choice_prob[(work, home)]
        self.housing_choice_prob = {}
        # in-home pattern choice probability
        # 1-dimension dict, i.e. in_home_choice_prob[(work, home)]
        self.in_home_choice_prob = {}
        # out-of-home pattern choice probability 
        # 1-dimension dict, i.e. out_of_home_choice_prob[(work, home)]
        self.out_of_home_choice_prob = {}
        # 1-dimension dict, i.e. commodity_choice_probc[comm]
        self.commodity_choice_prob = {}
        # 4-dimension nested dict
        # i.e. transition_choice_prob[commodity][timeslice][state][transition]
        self.transition_choice_prob = {}

class FlowVar(object):
    """ The world of the economic activities and transport network. 
        The variables in this class define the rules of this world.
    """
    def __init__(self):
        
        # assginment
        # 1-dimension dict, i.e. link_flows[move]
        self.movement_flows = {}
        self.movement_steps = {}
        # 4-dimension nested dict
        # i.e. transition_flows[commodity][timeslice][state][transition]
        self.transition_flows = {}
        # 3-dimension nested dict
        # i.e. state_flows[commodity][timeslice][state]
        self.state_flows = {}
        # 1-dimension dict, i.e. commodity_flows[commodity]
        self.commodity_flows = {}
        # 1-dimension dict, i.e. in_home_flows[(work, home)]
        self.in_home_flows = {}
        # 1-dimension dict, i.e. out_of_home_flows[(work, home)]
        self.out_of_home_flows = {}
        # 1-dimension dict, i.e. housing_flows[(work, home)]
        self.housing_flows = {}
        # 3-dimension nested dict
        # i.e. OD_trips[timeslice][origin][destination]
        self.OD_trips = {}
        # 2-dimension nested dict
        # i.e. zone_population[timeslice][zone]
        self.zone_population = {}
        # 2-dimension nested dict
        # i.e. actv_population[timeslice][actv]
        self.actv_population = {}

        ## export to MATLAB
        ## mat_pattern_flow = [None] * num_sample
        ## mat_zone_passenger = [None] * num_sample
        ## mat_aggrg_trip = [None] * num_sample


