# Markov decision process
from iofile.inputs import *
from iofile.outputs import *
from loading.assign import find_fixed_point
from viewer.plot import draw_zone_population
from allocating.generators import gen_activity_util, gen_path_set

def main():
    creat_activity_4node()
    gen_activity_util()
    creat_activity_bundle_4node()
    
    creat_traffic_zone_4node()
#    creat_dyna_travel_times()
    creat_line_4node()
    creat_sidewalks_4node()
    gen_path_set()

    find_fixed_point(4)

    fout = open('equil_flows.log', 'w')
#    export_configure(fout)
    export_bundle_choice(fout)
    export_activity_duration(fout)
    export_zone_population(fout)
    export_actv_population(fout)
    export_state_flows(fout)
    export_depart_flows(fout)
    export_optimal_util(fout)
#    export_movement_flows(fout)
#    export_travel_times(fout)
    fout.close()
#    draw_zone_population(4)

if __name__ == '__main__':
    import sys
    sys.path.append('D:\Workspace\PyMarkovActv\src')
    main()

