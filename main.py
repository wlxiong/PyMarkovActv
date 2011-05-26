# Markov decision process
import traceback
from shared.universe import logs
from debug.traceback import print_exc_plus
from iofile.inputs import load_network, load_activity
from iofile.outputs import export_vehicle_emission_tab, export_social_welfare_tab, export_location_choice_tab
from allocating.generators import gen_activity_util, gen_path_set
from bilevel.bruteforce import enum_housing_supply
from stats.timer import print_current_time

def main():
    # open log file
    logs.open_debug_log()
    # initialize the timer
    print_current_time()
    # the data set name
    case_name = '6node'
    # load activity data
    load_activity(case_name)
    gen_activity_util()
    # load network data
    load_network(case_name)
    gen_path_set()
    print '\n LOAD DATA'
    print_current_time()
    
    # bruce force: run multiple scenarios
    enum_housing_supply(case_name, 10000, 10000, 20, 16)
    
    # export the iterations 
    ftab = open('tables.log', 'w')
    export_location_choice_tab(ftab)
    export_social_welfare_tab(ftab)
    export_vehicle_emission_tab(ftab)
    
    # open log file
    logs.close_debug_log()
    
if __name__ == '__main__':
    # import sys
    # sys.path.append('/Users/xiongyiliang/Workspace/Research/PyMarkovActv/src/')
    try:
        main()
    except:
        traceback.print_exc()
        print_exc_plus()
