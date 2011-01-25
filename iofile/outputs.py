# export data to file
from shared.universe import conf, elem, util, flow
from utils.convert import min2slice
from planning.markov import Commodity, enum_commodity, enum_state
from stats.estimator import calc_average_activity_duration, calc_aggregate_flows
from loading.init import init_OD_trips, init_zone_population, init_actv_population
from stats.timer import print_current_time

def export_activity_util(export):
    print>>export, '---------- activity utility ----------'
    for timeslice in xrange(min2slice(conf.DAY)+1):
        util.activity_util.append(dict() )
        for each_actv in elem.activities:
            print>>export, util.activity_util[timeslice][each_actv],
            print>>export, '\t', 
        print>>export

def export_OD_trips(export):
    print>>export, '\n-------- aggregate O-D trips ---------\n'
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
            zone_population = {}
            for each_actv in comm.bundle.activity_set:
                zone_population[each_actv] = 0.0
            for state in enum_state(comm, timeslice):
                zone_population[state.activity] += flow.state_flows[comm][timeslice][state]
##                print>>export, flow.transition_flows[comm][timeslice][state].values(),
            for each_actv in sorted(comm.bundle.activity_set):
                print>>export, "%8.2f\t" % (zone_population[each_actv]),
            print>>export
        print>>export

def export_zone_population(export):
    print>>export, '\n-------- zone passengers ---------\n'
    for zone in sorted(elem.zone_list):
        print>>export, "\t %s" % (zone),
    print>>export
    for timeslice in xrange(min2slice(conf.DAY)):
        print>>export, "[%3d]   " % timeslice, 
        for zone in sorted(elem.zone_list):
            print>>export, "\t %08.1f" % flow.zone_population[timeslice][zone],
        print>>export

def export_actv_population(export):
    print>>export, '\n-------- activity passengers ---------\n'
    for each_actv in elem.activities.values():
        print>>export, "\t %s" % (each_actv), 
    print>>export
    for timeslice in xrange(min2slice(conf.DAY)):
        print>>export, "[%3d]   " % timeslice, 
        for each_actv in elem.activities.values():
            print>>export, "\t %08.1f" % flow.actv_population[timeslice][each_actv],
        print>>export

def export_optimal_util(export):
    print>>export, '\n------optimal utility------\n'
    for comm in enum_commodity():
        print>>export, " commodity %s " % comm
        for timeslice in xrange(min2slice(conf.DAY)):
            print>>export, " [%3d] " % timeslice, 
            for state in enum_state(comm, timeslice):
                print>>export, ("\t %s: %4.2f" % (state, util.state_optimal_util[comm][timeslice][state])), 
            print>>export
        print>>export

def export_movement_flows(export):
    print>>export, '\n------movement flows------\n'
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


def export_choice_volume(export):
    print>>export, '\n ------- bundle choice -------\n'
    for work in elem.work_list: 
        print>>export, "(Work %s, Jobs %6.1f)\n" % (work, work.jobs)
        for home in elem.home_list: 
            print>>export, "[Home %s, Population %6.1f]" % (home, flow.housing_flows[(work, home)])
            print>>export, "[In-home]\t %6.1f" % (flow.in_home_flows[(work, home)])
            print>>export, "[Out-of-home]\t %6.1f" % (flow.out_of_home_flows[(work, home)])
            for bundle in elem.bundles.values():
                comm = Commodity(work, home, bundle)
                print>>export, "%s\t %6.1f" % (bundle, flow.commodity_flows[comm])
            print>>export

def export_activity_duration(export):
    print>>export, '\n ------- activity duration -------\n'
    for comm in enum_commodity():
        print>>export, " [%s] " % comm 
        average_duration = calc_average_activity_duration(comm)
        for key, value in average_duration.items():
            print>>export, "%s:\t%.1f\t" % (key, value),
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
    # prepare data
    # initialize the aggregate flows
    init_zone_population(0.0)
    print '  init_zone_population(0.0)'
    print_current_time()
    init_actv_population(0.0)
    print '  init_actv_population(0.0)'
    print_current_time()
    init_OD_trips(0.0)
    print '  init_OD_trips(0.0)'
    print_current_time()
    # prepare the aggregate flows for output
    calc_aggregate_flows()
    print '  calc_aggregate_flows()'
    print_current_time()
    # export data
    # export_OD_trips(fout)
    # export_depart_flows(fout)
    # export_zone_population(fout)
    # export_actv_population(fout)
    
# export computational results
def export_data(case_name):
    fout = open('../equil_flows_'+case_name+'.log', 'w')
    # export_configure(fout)
    export_choice_volume(fout)
    export_activity_duration(fout)
    # export_aggregate_flows(fout)
    # export_state_flows(fout)
    # export_optimal_util(fout)
    export_movement_flows(fout)
    # export_travel_times(fout)
    fout.close()

##     export_aggreg_trip(export_file)
##     export_activity_trip(export_file)
##     export_passenger_trip(export_file)
##     export_optimal_util(export_file)
##     export_path_set(export_file)
##     export_link_flow(export_file)
