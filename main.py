# Markov decision process
from iofile.inputs import load_network, load_activity
from iofile.outputs import export_data
from loading.assign import find_fixed_point
from viewer.plot import draw_zone_population
from allocating.generators import gen_activity_util, gen_path_set

def main():
    # the data set name
    case_name = '6node'
    # load activity data
    load_activity(case_name)
    gen_activity_util()
    # load network data
    load_network(case_name)
    gen_path_set()

    # run the iterative procedure 
    find_fixed_point(2)

    # output the raw results
    export_data(case_name)
    # generate visual results
#    draw_zone_population(4)

if __name__ == '__main__':
    import sys
    sys.path.append('/Users/xiongyiliang/Workspace/Research/PyMarkovActv/src/')
    main()
