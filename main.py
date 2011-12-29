# Markov decision process
from itertools import product
from shared.universe import elem
from iofile.inputs import load_network, load_activity
from iofile.outputs import export_data
from loading.assign import find_fixed_point
from viewer.plot import draw_zone_population
from allocating.generators import gen_activity_util, gen_path_set
from stats.estimator import calc_aggregate_flows
from stats.timer import print_current_time
import math

def run_multi_scenarios(case_name, corr_list):
    # try distinct corrs
    for corr in corr_list:
        print '\n***   corr = %f   ***\n' % corr
        # reset joint activity utils
        for each_actv in elem.activities.values(): 
            if each_actv.is_joint:
                each_actv.Um = each_actv.Ur + corr * math.sqrt(each_actv.Ur * each_actv.Ur)
        # generate utils
        gen_activity_util()

        # run the iterative procedure 
        find_fixed_point(2)
        
        # calculate the statistics
        calc_aggregate_flows()

        # output the raw results
        export_data(case_name+'_'+str(corr))
        print "\n [export data]"
        print "     data set: %s" % case_name
        print "  correlation: %f" % corr
        print_current_time()
        # generate visual results
        # draw_zone_population(4)

def main():
    # initialize the timer
    print_current_time()
    # the data set name
    case_name = '6node'
    # load activity data
    load_activity(case_name)
    # load network data
    load_network(case_name)
    gen_path_set()
    print '\n DATA LOADED'
    print_current_time()
    
    # run multiple scenarios
    run_multi_scenarios(case_name, [0.0, 1.0])
    
if __name__ == '__main__':
    import sys
    # sys.path.append('/Users/xiongyiliang/Projects/PyMarkovActv/')
    main()
