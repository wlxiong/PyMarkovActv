from itertools import product
from shared.universe import elem
from bilevel.subprob import SubProb
from iofile.outputs import export_data
from stats.timer import print_current_time

def enum_housing_supply(case_name, total_population, max_capacity, step_size, iter_num):
    step = max_capacity/step_size
    for capacity_list in product(range(step,max_capacity,step), repeat=len(elem.home_list)):
        if sum(capacity_list) <> total_population:
            continue
        elem.subproblems.append(SubProb(dict(zip(elem.home_list, capacity_list))))
        elem.subproblems[-1].solve(iter_num)
        
        # output the raw results
        export_data(case_name+'_'+str(capacity_list))
        print " export_data(%s_%s)" % (case_name, str(capacity_list))
        print_current_time()
        # generate visual results
        # draw_zone_population(4)
