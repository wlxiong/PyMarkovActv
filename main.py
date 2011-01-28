# Markov decision process
from itertools import product
from shared.universe import elem
from iofile.inputs import load_network, load_activity
from iofile.outputs import export_data
from loading.assign import find_fixed_point
from viewer.plot import draw_zone_population
from allocating.generators import gen_activity_util, gen_path_set
from stats.timer import print_current_time

def run_multi_scenarios(case_name, total_population, max_capacity):
    step = max_capacity/10
    for capacity_list in product(range(step,max_capacity,step), repeat=len(elem.home_list)):
        if sum(capacity_list) <> total_population:
            continue
        for home, houses in zip(elem.home_list, capacity_list):
            home.houses = houses
        print '\n  *** Housing Supply ***'
        print ' %s \n' % zip(elem.home_list, capacity_list)

        # run the iterative procedure 
        find_fixed_point(4)

        # output the raw results
        export_data(case_name+'_'+str(capacity_list))
        print " export_data(%s_%s)" % (case_name, str(capacity_list))
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
    gen_activity_util()
    # load network data
    load_network(case_name)
    gen_path_set()
    print '\n LOAD DATA'
    print_current_time()
    
    # run multiple scenarios
    run_multi_scenarios(case_name, 30000, 30000)
    
if __name__ == '__main__':
    import sys
    # sys.path.append('/Users/xiongyiliang/Workspace/Research/PyMarkovActv/src/')
    main()
