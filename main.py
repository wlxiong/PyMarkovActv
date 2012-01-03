# Markov decision process
from shared.universe import elem
from iofile.inputs import load_network, load_activity
from iofile.outputs import export_data
from loading.assign import find_fixed_point, load_all_flows
from viewer.plot import draw_zone_population
from allocating.generators import gen_activity_util, gen_path_set, find_shortest_path
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
                if each_actv == elem.home_am_activity or each_actv == elem.home_pm_activity: 
                    each_actv.Um = each_actv.Ur - corr * .4 * math.sqrt(each_actv.Ur * each_actv.Ur)
                else: 
                    each_actv.Um = each_actv.Ur + corr * .5 * math.sqrt(each_actv.Ur * each_actv.Ur)
            print each_actv, each_actv.Um, each_actv.Ur
        # generate utils
        gen_activity_util()

        # run the iterative procedure 
        find_fixed_point(8)
        
        # load the convergence flows
        # print '\n Now, let\'s get the convergence flows... \n'
        # load_all_flows()
        
        # calculate the statistics
        calc_aggregate_flows()

        # output the raw results
        export_data(case_name+'_'+str(corr))
        print "\n [export data]"
        print "       data set: %s" % case_name
        print "    correlation: %f" % corr
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
    find_shortest_path()
    print '\n DATA LOADED'
    print_current_time()
    
    # run multiple scenarios
    run_multi_scenarios(case_name, [1.0])
    
if __name__ == '__main__':
    import sys
    # sys.path.append('/Users/xiongyiliang/Projects/PyMarkovActv/')
    main()
