# Markov decision process
from iofile.inputs import load_network, load_activity
from iofile.outputs import export_data
from loading.assign import find_fixed_point
from viewer.plot import draw_zone_population
from allocating.generators import gen_solo_activity_util, gen_path_set, find_shortest_path
from allocating.creators import set_corr
from stats.timer import print_current_time

def run_multi_scenarios(case_name, corr_list):
    # try distinct corrs
    for corr in corr_list:
        print '\n***   corr = %f   ***\n' % corr

        # correlations between household members
        set_corr(1, 2, corr)
        
        # generate utils
        gen_solo_activity_util()

        # run the iterative procedure 
        find_fixed_point(4, case_name, corr)

        # output the raw results
        export_data(case_name+'_r'+str(corr))
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
