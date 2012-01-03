# export data to file
from shared.universe import conf, elem, util, flow
from utils.convert import min2slice
from utils.get import get_move_flow
from planning.markov import Commodity, enum_commodity, enum_state
from stats.estimator import calc_average_activity_duration, calc_average_temporal_util
from stats.environment import calc_total_emission

def export_activity_util(export):
    print>>export, '\n---------- activity temporal utility ----------\n'
    for actv_name in sorted(elem.activities.keys()):
        print>>export, "%s\t" % actv_name, 
    print>>export
    for timeslice in xrange(min2slice(conf.DAY)+1):
        for actv_name in sorted(elem.activities.keys()):
            each_actv = elem.activities[actv_name]
            print>>export, "%8.2f\t" % util.activity_util[timeslice][each_actv],
        print>>export

def export_OD_trips(export):
    print>>export, '\n-------- O-D trips ---------\n'
    for timeslice in xrange(min2slice(conf.DAY)):
            for O in elem.zone_list:
                print>>export, " [%3d] " % timeslice,
                for D in elem.zone_list:
                    print>>export, "\t %08.1f" % (flow.OD_trips[timeslice][O][D]),
                print>>export

def export_depart_flows(export):
    print>>export, '\n-------- departure flows ---------\n'
    for O in elem.zone_list:
        for D in elem.zone_list:
            print>>export, "\t %s->%s" % (O, D), 
    print>>export
    for timeslice in xrange(min2slice(conf.DAY)):
        print>>export, " [%3d] " % timeslice,
        for O in elem.zone_list:
            for D in elem.zone_list:
                print>>export, "\t %08.1f" % (flow.OD_trips[timeslice][O][D]),
        print>>export
    
def export_state_flows(export):
    print>>export, '\n-------- state flows ---------\n'
    for comm in enum_commodity():
        print>>export, ">>commodity %s " % comm
        for timeslice in xrange(min2slice(conf.DAY)+1):
            print>>export, " [%03d]\t" % timeslice, 
            for state in enum_state(comm, timeslice):
                print>>export, " %s: %8.2f\t" % (state, flow.state_flows[comm][timeslice][state]), 
            print>>export

def export_temporal_flows(export):
    print>>export, '\n-------- temporal flows ---------\n'
    for comm in enum_commodity():
        print>>export, ">>commodity %s " % comm
        for timeslice in xrange(min2slice(conf.DAY)+1):
            print>>export, " [%03d]\t" % timeslice, 
            print>>export, "%8.2f\t" % flow.temporal_flows[comm][timeslice], 
            print>>export, "%8.2f\t" % (flow.commodity_steps[comm] - flow.temporal_flows[comm][timeslice])
        print>>export
    print>>export
            
def export_zone_population(export):
    print>>export, '\n-------- zone passengers ---------\n'
    for zone in sorted(elem.zone_list):
        print>>export, "\t %s" % (zone),
    print>>export
    for timeslice in xrange(min2slice(conf.DAY)+1):
        print>>export, "[%3d]   " % timeslice, 
        for zone in sorted(elem.zone_list):
            print>>export, "\t %08.1f" % flow.zone_population[timeslice][zone],
        print>>export

def export_activity_population(export):
    print>>export, '\n-------- activity passengers ---------\n'
    for each_actv in elem.activities.values():
        print>>export, "\t %s" % (each_actv), 
    print>>export
    for timeslice in xrange(min2slice(conf.DAY)+1):
        print>>export, "[%3d]   " % timeslice, 
        for each_actv in elem.activities.values():
            print>>export, "\t %08.1f" % flow.actv_population[timeslice][each_actv],
        print>>export

def export_optimal_util(export):
    print>>export, '\n------ optimal utility ------\n'
    for comm in enum_commodity():
        print>>export, " commodity %s " % comm
        for timeslice in xrange(min2slice(conf.DAY)):
            print>>export, " [%3d] " % timeslice, 
            for state in enum_state(comm, timeslice):
                print>>export, ("\t %s: %4.2f" % (state, util.state_optimal_util[comm][timeslice][state])), 
            print>>export
        print>>export

def export_movement_flows(export):
    print>>export, '\n------ movement flows ------\n'
    sorted_moves = sorted(flow.movement_flows.keys(), key = repr)
    max_bus_flow, max_sub_flow,max_hwy_flow, max_ped_flow = \
        float('-inf'), float('-inf'), float('-inf'), float('-inf')
    for each_move in sorted_moves:
        # print>>export, " %s\t%6.1f" % (each_move, flow.movement_flows[each_move])
        if each_move.related_edge.related_vector.capacity == conf.CAPACITY_bus:
            if max_bus_flow < flow.movement_flows[each_move]:
                max_bus_flow = flow.movement_flows[each_move]
        elif each_move.related_edge.related_vector.capacity == conf.CAPACITY_sub:
            if max_sub_flow < flow.movement_flows[each_move]:
                max_sub_flow = flow.movement_flows[each_move]
        elif each_move.related_edge.related_vector.capacity == conf.CAPACITY_ped:
            if max_ped_flow < flow.movement_flows[each_move]:
                max_ped_flow = flow.movement_flows[each_move] 
        else:
            if max_hwy_flow < flow.movement_flows[each_move]:
                max_hwy_flow = flow.movement_flows[each_move] 
    print>>export, " maximum transit line flows %6.1f png" % (max_bus_flow)
    print>>export, " maximum subway line flows %6.1f png" % (max_sub_flow)
    print>>export, " maximum highway flows %6.1f png" % (max_hwy_flow)
    print>>export, " maximum pedestrian flows %6.1f png" % (max_ped_flow)

    print>>export, '\n movement flow variables (exceeding capacity) \n'
    for origin in elem.zone_list:
        for dest in elem.zone_list:
            # print>>export, [origin, dest]
            path = elem.shortest_path[origin][dest]
            print>>export, "\n%s" % path
            for timeslice in xrange(min2slice(conf.DAY)):
                path_travel_timeslice, path_travel_cost = path.calc_travel_impedences(timeslice)
                print>>export, "[%3d] " % timeslice, 
                print>>export, "%8.2f\t%8.2f\t" % (path.get_travel_time(timeslice), path_travel_cost)
                for each_move in path.moves_on_path[timeslice]:
                    get_move_flow(each_move)
                    print>>export, " %s:\t" % each_move, 
                    print>>export, "%8.2f / %8.2f" % (flow.movement_flows[each_move],
                                                        each_move.related_edge.related_vector.capacity), 
                    if flow.movement_flows[each_move] > each_move.related_edge.related_vector.capacity:
                        print>>export, " !!", 
                    print>>export

def export_choice_volume(export):
    print>>export, '\n------- bundle choice -------\n'
    for work in elem.work_list: 
        print>>export, "(Work %s, Jobs %6.1f)\n" % (work, work.jobs)
        for home in elem.home_list: 
            print>>export, "[Home %s, Population %6.1f]" % (home, elem.housing_flows[(work, home)])
            print>>export, "[In-home]\t %6.1f" % (flow.in_home_flows[(work, home)])
            print>>export, "[Out-of-home]\t %6.1f" % (flow.out_of_home_flows[(work, home)])
            print>>export, "[Daily Activity Utility]\t %6.1f" % (util.housing_util[(work, home)])
            for bundle in elem.bundles.values():
                comm = Commodity(work, home, bundle)
                print>>export, "%s\t %6.1f" % (bundle, flow.commodity_steps[comm])
            print>>export

def export_activity_duration(export):
    print>>export, '\n------- activity duration -------\n'
    for comm in enum_commodity():
        print>>export, " [%s] " % comm
        activity_list = sorted(list(comm.bundle.activity_set))
        average_activity_duration, average_travel_time = calc_average_activity_duration(comm)
        # subtotal for joint and independent activities
        joint_activity_duration = 0.0
        indep_activity_duration = 0.0
        for each_actv in activity_list:
            if each_actv.is_joint:
                joint_activity_duration += average_activity_duration[each_actv]
            else: 
                indep_activity_duration += average_activity_duration[each_actv]
        print>>export, "%12s\t%12s\t%12s" % ('travel', 'joint', 'indep')
        print>>export, "%12.1f\t%12.1f\t%12.1f" % (average_travel_time, joint_activity_duration, indep_activity_duration)
        # print the activity names
        for each_actv in activity_list:
            print>>export, "%12s\t" % (each_actv.name),
        print>>export
        # print the average activity durations
        for each_actv in activity_list:
            print>>export, "%12.1f\t" % (average_activity_duration[each_actv]),
        print>>export

def export_average_temporal_util(export):
    print>>export, '\n------- average temporal utility -------\n'
    for comm in enum_commodity():
        print>>export, " [%s] " % comm
        average_utility, average_travel_disutil = calc_average_temporal_util(comm)
        for timeslice in xrange(min2slice(conf.DAY)+1):
            print>>export, " [%d]\t" % timeslice, 
            print>>export, "%8.1f\t%8.1f\t" % (average_utility[timeslice], average_travel_disutil[timeslice]),
            print>>export

# def export_travel_times(export):
#     print>>export, '\n ------- dynamic travel time -------\n'
#     for timeslice in xrange(min2slice(conf.DAY)):
#         print>>export, "[%d]" % timeslice
#         for origin in elem.zone_list:
#             print>>export, "(%s)  " % origin,
#             for dest in elem.zone_list:
#                 print>>export, "%s: %3.2f  " % (dest, flow.dyna_travel_times[timeslice][origin][dest]),
#             print>>export

def export_aggregate_flows(export):
    # export_OD_trips(export)
    # export_depart_flows(export)
    export_zone_population(export)
    export_activity_population(export)
    export_temporal_flows(export)

def export_total_emission(export):
    print>>export, '\n------- vehicle emission -------\n'
    print>>export, calc_total_emission()
    
# export computational results
def export_data(case_name):
    fout = open('logs/equil_flows_'+case_name+'.log', 'w')
    # export_configure(fout)
    export_choice_volume(fout)
    export_activity_duration(fout)
    export_activity_util(fout)
    export_aggregate_flows(fout)
    export_average_temporal_util(fout)
    export_movement_flows(fout)
    # export_state_flows(fout)
    # export_total_emission(fout)
    # export_state_flows(fout)
    # export_optimal_util(fout)
    fout.close()

##     export_travel_times(fout)
##     export_aggreg_trip(export_file)
##     export_activity_trip(export_file)
##     export_passenger_trip(export_file)
##     export_optimal_util(export_file)
##     export_path_set(export_file)
##     export_link_flow(export_file)

def main():
    export_data('test')

if __name__ == '__main__':
    import sys
    sys.path.append('/Users/xiongyiliang/Projects/PyMarkovActv/')
    main()
