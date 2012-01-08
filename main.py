# Markov decision process
from iofile.inputs import load_network, load_activity
from iofile.outputs import export_multi_run_data
from loading.assign import find_fixed_point
# from viewer.plot import draw_zone_population
from allocating.generators import gen_solo_activity_util, gen_path_set, find_shortest_path
from allocating.creators import set_corr
from stats.timer import print_current_time

def run_multi_scenarios(case_name, corr_list):
    # try distinct corrs
    for corr in corr_list:
        print "       data set: %s" % case_name
        print "    correlation: %.2f" % corr

        # correlations between household members
        set_corr(1, 2, corr)

        # run the iterative procedure 
        find_fixed_point(8, case_name, corr)

        # output the raw results
        # export_data(case_name+'_r'+str(corr))

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

    # generate path sets
    gen_path_set()
    find_shortest_path()
    # generate utils
    gen_solo_activity_util()
    
    print '\n DATA LOADED'
    print_current_time()
    
    # run multiple scenarios
    corr_list = [corr/10.0 for corr in range(10,-1,-1)]
    run_multi_scenarios(case_name, corr_list)
    
    # export multi-run data
    export_multi_run_data(case_name)
    
if __name__ == '__main__':
    # import sys
    # sys.path.append('/Users/xiongyiliang/Projects/PyMarkovActv/')
    main()
