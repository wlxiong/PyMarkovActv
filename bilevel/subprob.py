# save variables for each iteration
from shared.universe import elem, flow, util
from loading.assign import find_fixed_point
from stats.environment import calc_total_emission

class SubProb(object):
    def __init__(self, housing_supply):
        self.housing_supply = housing_supply
        self.housing_flows = None
        self.housing_util = None
        self.social_welfare = None
        self.total_emission = None
        for home, supply in self.housing_supply.items():
            home.houses = supply
        
    def save_location_choice(self):
        self.housing_flows = dict(flow.housing_flows)
        
    def save_social_welfare(self):
        self.housing_util = dict(util.housing_util)
        self.social_welfare = 0.0
        for work in elem.work_list: 
            for home in elem.home_list: 
                self.social_welfare += util.housing_util[(work, home)] * flow.housing_flows[(work, home)]
        
    def save_vehicle_emission(self):
        self.total_emission = calc_total_emission()
        
    def solve(self, iter_num):
        print '\n  *** Housing Supply ***'
        print ' %s \n' % self.housing_supply
        # run the iterative procedure 
        find_fixed_point(iter_num)
        # save the solutions and other data
        self.save_location_choice()
        self.save_social_welfare()
        self.save_vehicle_emission()
