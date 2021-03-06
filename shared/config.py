# configuration class


class Config(object):
    # length of a single day
    DAY = 1440
    # minutes per tick
    TICK = 20

    def __init__(self, MAX_ITER=16, HORIZON=1440):
        self.MAX_ITER, self.HORIZON = MAX_ITER, HORIZON

        # log file
        self.log_file_name = 'logs/debug'+'.log'
        self.log = open(self.log_file_name, 'w')
        
        # variance tolerance of preferred activitiy timing
        self.DELTA = 0.25 * 60.0
        # the link capacity
        self.CAPACITY_ped = 30000
        self.CAPACITY_bus = 120
        self.CAPACITY_sub = 1500

        # the equivalent utility of unit generalized travel time
        min2h = 1.0/60.0 # convert time unit from minute to hour
        # the equivalent utility of unit in-vehicle travel time
        self.ALPHA_in = 60.0 * min2h
        # the equivalent utility of unit drive travel time
        self.ALPHA_car = 60.0 * min2h
        # the equivalent utility of unit waiting time
        self.ALPHA_wait = 120.0 * min2h
        # the equivalent utility of unit walking time
        self.ALPHA_walk = 120.0 * min2h
        # the equivalent utility of line transfering 
        self.ALPHA_tran = 5.0
        # the equivalent utility of one dollar
        self.ALPHA_fare = 1.0
        # the unit cost of early arrival (dollar/hour)
        self.ALPHA_early = 0.0 # 30.0 * min2h
        # the unit cost of late arrival (dollar/hour)
        self.ALPHA_late = 0.0  # 90.0 * min2h
        # the unit cost of house rent 
        self.ALPHA_rent = 1.0

        # the parameter related to residential location 
        self.THETA_location = 0.002
        # the parameter related to making a trip or not
        self.THETA_travel = 0.005
        # the parameter related to pattern choice
        self.THETA_bundle = 0.008
        # the parameter related to tour choice
        self.THETA_tour = 0.01
        # the parameter related to path choice
        # self.THETA_path = 0.1
        # discount of future utility
        self.discount = 1.0
        # correlation between household members
        # 1-dimension dict, i.e. corr[(person 1,person 2)]
        self.corr = {}


conf = Config()
