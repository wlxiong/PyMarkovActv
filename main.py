# Markov decision process
from itertools import product
from shared.universe import elem
from iofile.inputs import load_network, load_activity
from iofile.outputs import export_data
from loading.assign import find_fixed_point
from viewer.plot import draw_zone_population
from allocating.generators import gen_activity_util, gen_path_set

def run_multi_scenarios(case_name, total_population, max_capacity):
    step = max_capacity/4
    for capacity_list in product(range(0,max_capacity+1,step), repeat=len(elem.home_list)):
        if sum(capacity_list) < total_population:
            continue
        for home, capacity in zip(elem.home_list, capacity_list):
            home.capacity = capacity
        print '\n *** Housing Supply ***'
        print ' %s \n' % zip(elem.home_list, capacity_list)
        # run the iterative procedure 
        find_fixed_point(1)
        # output the raw results
        export_data(case_name+'_'+str(capacity_list))
        # generate visual results
        # draw_zone_population(4)

def main():
    # the data set name
    case_name = '6node'
    # load activity data
    load_activity(case_name)
    gen_activity_util()
    # load network data
    load_network(case_name)
    gen_path_set()
    # run multiple scenarios
    run_multi_scenarios(case_name, 30000, 30000)
    
if __name__ == '__main__':
    import sys
    sys.path.append('/Users/xiongyiliang/Workspace/Research/PyMarkovActv/src/')
    main()
