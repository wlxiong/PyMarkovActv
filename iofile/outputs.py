# export data to file
from shared.universe import conf, elem, util, flow, prob, stat
from utils.convert import min2slice
from utils.get import get_move_flow, sorted_dict_values
from planning.markov import Commodity, enum_commodity, enum_state
from stats.estimator import calc_average_activity_duration, calc_average_temporal_util, calc_population_flows
from stats.environment import calc_total_emission

def export_solo_activity_util(export):
    print>>export, '\n---------- solo activity utility ----------\n'
    for actv_name in sorted(elem.activities.keys()):
        print>>export, "%s\t" % actv_name, 
    print>>export
    for timeslice in xrange(min2slice(conf.DAY)+1):
        print>>export, "[%3d]\t" % timeslice, 
        for each_actv in sorted_dict_values(elem.activities):
            print>>export, "%8.2f\t" % util.solo_util[timeslice][each_actv],
        print>>export

def export_socio_activity_util(export):
    print>>export, '\n---------- socio activity utility ----------\n'
    for person in elem.person_list:
        print>>export, "%s" % person
        # print titles
        for each_actv in sorted_dict_values(elem.activities):
            for each_zone in each_actv.locations:
                print>>export, "\t%8s" % (each_actv),
        print>>export 
        for each_actv in sorted_dict_values(elem.activities):
            for each_zone in each_actv.locations:
                print>>export, "\t%8s" % (each_zone),
        print>>export
        # print utility
        for timeslice in xrange(min2slice(conf.DAY)+1):
            print>>export, "[%3d]\t" % timeslice, 
            for each_actv in sorted_dict_values(elem.activities):
                for each_zone in each_actv.locations:
                    print>>export, "%8.2f\t" % util.socio_util[person][timeslice][(each_actv,each_zone)],
            print>>export
        print>>export

def export_activity_choice_prob(export):
    print>>export, '\n---------- activity choice prob ----------\n'
    for person in elem.person_list:
        print>>export, "%s" % person
        # print titles
        print>>export, "\t travel", 
        for each_actv in sorted_dict_values(elem.activities):
            for each_zone in each_actv.locations:
                print>>export, "\t%8s" % (each_actv),
        print>>export
        print>>export, "\t   road", 
        for each_actv in sorted_dict_values(elem.activities):
            for each_zone in each_actv.locations:
                print>>export, "\t%8s" % (each_zone),
        print>>export
        # print probability
        for timeslice in xrange(min2slice(conf.DAY)+1):
            print>>export, "[%3d]\t" % timeslice, 
            static_percent = sum(prob.activity_choice_prob[person][timeslice].values())
            print>>export, "%8.2f\t" % (1.0 - static_percent), 
            for each_actv in sorted_dict_values(elem.activities):
                for each_zone in each_actv.locations:
                    print>>export, "%8.2f\t" % prob.activity_choice_prob[person][timeslice][(each_actv,each_zone)],
            print>>export
        print>>export

def export_OD_trips(export):
    print>>export, '\n-------- O-D trips ---------\n'
    for timeslice in xrange(min2slice(conf.DAY)):
        for O in elem.zone_list:
            print>>export, "[%3d] " % timeslice,
            for D in elem.zone_list:
                print>>export, "%08.1f\t" % (flow.OD_trips[timeslice][O][D]),
            print>>export

def export_depart_flows(export):
    print>>export, '\n-------- departure flows ---------\n'
    for O in elem.zone_list:
        for D in elem.zone_list:
            print>>export, "\t %s->%s" % (O, D), 
    print>>export
    for timeslice in xrange(min2slice(conf.DAY)):
        print>>export, "[%3d] " % timeslice,
        for O in elem.zone_list:
            for D in elem.zone_list:
                print>>export, "\t %08.1f" % (flow.OD_trips[timeslice][O][D]),
        print>>export
    
def export_state_flows(export):
    print>>export, '\n-------- state flows ---------\n'
    for comm in enum_commodity():
        print>>export, " %s " % comm
        for timeslice in xrange(min2slice(conf.DAY)+1):
            print>>export, " [%03d]\t" % timeslice, 
            for state in enum_state(comm, timeslice):
                print>>export, " %s: %8.2f\t" % (state, flow.state_flows[comm][timeslice][state]), 
            print>>export

def export_static_population(export):
    print>>export, '\n-------- temporal flows ---------\n'
    for comm in enum_commodity():
        print>>export, " %s " % comm
        print>>export, "\t static\t traveling"
        for timeslice in xrange(min2slice(conf.DAY)+1):
            print>>export, " [%03d]\t" % timeslice, 
            print>>export, "%8.2f\t" % flow.static_population[comm][timeslice], 
            print>>export, "%8.2f\t" % (flow.commodity_steps[comm] - flow.static_population[comm][timeslice])
        print>>export
            
def export_zone_population(export):
    print>>export, '\n-------- zone passengers ---------\n'
    for zone in sorted(elem.zone_list):
        print>>export, "\t %s" % (zone),
    print>>export
    for timeslice in xrange(min2slice(conf.DAY)+1):
        print>>export, "[%3d]\t" % timeslice, 
        for zone in sorted(elem.zone_list):
            print>>export, "%08.1f\t" % flow.zone_population[timeslice][zone],
        print>>export

def export_activity_population(export):
    print>>export, '\n-------- activity passengers ---------\n'
    for each_actv in sorted_dict_values(elem.activities):
        print>>export, "\t %s" % (each_actv), 
    print>>export
    for timeslice in xrange(min2slice(conf.DAY)+1):
        print>>export, "[%3d]\t" % timeslice, 
        for each_actv in sorted_dict_values(elem.activities):
            print>>export, "%08.1f\t" % flow.activity_population[timeslice][each_actv],
        print>>export

def export_state_util(export):
    print>>export, '\n------ state utility ------\n'
    for comm in enum_commodity():
        print>>export, " %s " % comm
        for timeslice in xrange(min2slice(conf.DAY)):
            print>>export, "[%3d] " % timeslice, 
            for state in enum_state(comm, timeslice):
                print>>export, ("\t %s: %4.2f" % (state, util.state_util[comm][timeslice][state])), 
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
    # initialize
    corr = conf.corr.values()
    stat.in_home_flows[corr[0]]     = 0.0
    stat.out_of_home_flows[corr[0]] = 0.0
    stat.person_util[corr[0]]       = 0.0
    for person in elem.person_list:
        work, home = person.work, person.home
        print>>export, "[Person %s, Population %6.1f]]" % (person, elem.person_flows[person])
        print>>export, "[In-home]\t %6.1f" % (flow.in_home_flows[person])
        print>>export, "[Out-of-home]\t %6.1f" % (flow.out_of_home_flows[person])
        print>>export, "[Daily Activity Utility]\t %6.1f" % (util.person_util[person])
        for bundle in elem.bundles.values():
            comm = Commodity(person, bundle)
            print>>export, "%s\t %6.1f" % (bundle, flow.commodity_steps[comm])
        print>>export
        # save the statistics for each scenario
        percent = elem.person_flows[person] / sum(elem.person_flows.values())
        stat.in_home_flows[corr[0]]     += percent * flow.in_home_flows[person]
        stat.out_of_home_flows[corr[0]] += percent * flow.out_of_home_flows[person]
        stat.person_util[corr[0]]       += percent * util.person_util[person]

def export_activity_duration(export):
    print>>export, '\n------- activity duration -------\n'
    # initialize
    corr = conf.corr.values()
    stat.average_travel_time[corr[0]]     = 0.0
    stat.joint_activity_duration[corr[0]] = 0.0
    stat.indep_activity_duration[corr[0]] = 0.0
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
        # print activity names
        print>>export, "%12s\t%12s\t%12s" % ('travel', 'joint', 'indep'), 
        for each_actv in activity_list:
            print>>export, "%12s\t" % (each_actv.name),
        print>>export
        # print average activty durations
        print>>export, "%12.1f\t%12.1f\t%12.1f" % (average_travel_time, 
                                                   joint_activity_duration, 
                                                   indep_activity_duration), 
        for each_actv in activity_list:
            print>>export, "%12.1f\t" % (average_activity_duration[each_actv]),
        print>>export, "\n"
        # save the statistics for each scenario
        percent = flow.commodity_steps[comm] / sum(elem.person_flows.values())
        stat.average_travel_time[corr[0]]     += percent * average_travel_time
        stat.joint_activity_duration[corr[0]] += percent * joint_activity_duration
        stat.indep_activity_duration[corr[0]] += percent * indep_activity_duration

def export_average_temporal_util(export):
    print>>export, '\n------- average temporal utility -------\n'
    for comm in enum_commodity():
        print>>export, " %s " % comm
        print>>export, "\t utility\t disutility"
        average_utility, average_travel_disutil = calc_average_temporal_util(comm)
        for timeslice in xrange(min2slice(conf.DAY)+1):
            print>>export, " [%d]\t" % timeslice, 
            print>>export, "%8.1f\t%8.1f\t" % (average_utility[timeslice], average_travel_disutil[timeslice]),
            print>>export
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

def export_total_emission(export):
    print>>export, '\n------- vehicle emission -------\n'
    print>>export, calc_total_emission()

def export_configure(export):
    print>>export, '\n------- settings -------\n'
    for key in sorted(conf.__dict__.keys()):
        print>>export, "%16s\t%s" % (key, conf.__dict__[key])
    
# export computational results
def export_data(case_name):
    fout = open('logs/equil_flows_'+case_name+'.log', 'w')

    # calculate the statistics
    calc_population_flows()

    export_configure(fout)
    export_choice_volume(fout)
    export_activity_duration(fout)
    
    export_solo_activity_util(fout)
    export_socio_activity_util(fout)
    export_activity_choice_prob(fout)
    
    export_zone_population(fout)
    export_activity_population(fout)
    export_static_population(fout)
    export_average_temporal_util(fout)
    
    # export_state_util(fout)
    # export_state_flows(fout)
    
    # export_OD_trips(fout)
    # export_depart_flows(fout)
    # export_movement_flows(fout)
    # export_total_emission(fout)
    
    fout.close()

def export_multi_run_data(case_name):
    # export to a MATLAB script file
    fout = open('logs/multi_run_'+case_name+'.m', 'w')
    print>>fout, "%s = %s;" % ('corr', sorted(stat.person_util.keys()) )
    print>>fout, "%s = %s;" % ('joint_duration', sorted_dict_values(stat.joint_activity_duration) )
    print>>fout, "%s = %s;" % ('indep_duration', sorted_dict_values(stat.indep_activity_duration) )
    print>>fout, "%s = %s;" % ('travel_time', sorted_dict_values(stat.average_travel_time) )
    print>>fout, "%s = %s;" % ('out_of_home', sorted_dict_values(stat.out_of_home_flows) )
    print>>fout, "%s = %s;" % ('in_home', sorted_dict_values(stat.in_home_flows) )
    print>>fout, "%s = %s;" % ('daily_util', sorted_dict_values(stat.person_util) )
    
def main():
    export_data('test')

if __name__ == '__main__':
    import sys
    sys.path.append('/Users/xiongyiliang/Projects/PyMarkovActv/')
    main()
