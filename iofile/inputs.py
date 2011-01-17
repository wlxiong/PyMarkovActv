# import data
import math 
from shared.universe import conf, elem, flow
from allocating.creators import add_activity, add_bundle
from allocating.creators import add_line, add_zone, add_sidewalk
from networks.basic import Zone
from networks.transit import Stop
from utils.convert import min2slice, slice2min

#############################
###     4 node network
#############################

def creat_activity_4node():
##  add_activity(name, U0, Um, Sigma, Lambda, Xi, time_win, min_duration, is_madatory, pref_timing):
    add_activity('home-am',    1.0, 400, -0.008, 1.0,   720, (0, 1440), 360, 0, -1)
    add_activity('home-pm',    1.0, 400, -0.008, 1.0,   720, (0, 1440), 360, 0, -1)
    add_activity('work',       0.0, 1000,  0.010, 1.0,   720, (0, 1440), 240, 1, 540)
    add_activity('school', 0.0, 160,  0.015, 1.0,   495, (0, 1440),  10, 0, -1)
    add_activity('shopping',   0.0, 400,  0.010, 1.0,  1170, (0, 1440),  10, 0, -1)
    add_activity('restaurant',   0.0, 200,  0.030, 1.0,  1140, (0, 1440),  10, 0, -1)
    elem.home_am_activity = elem.activities['home-am']
    elem.home_pm_activity = elem.activities['home-pm']

def creat_activity_bundle_4node():
#   add_bundle(key, activity_name_list)
    add_bundle(0, ['home-am', 'home-pm'])

    add_bundle(1, ['home-am', 'home-pm', 'work'])
    add_bundle(2, ['home-am', 'home-pm', 'shopping', 'work'])
    add_bundle(3, ['home-am', 'home-pm', 'work', 'restaurant'])
    add_bundle(4, ['home-am', 'home-pm', 'shopping', 'work', 'restaurant'])

    add_bundle(5, ['home-am', 'home-pm', 'school', 'work'])
    add_bundle(6, ['home-am', 'home-pm', 'shopping', 'work', 'school'])    
    add_bundle(7, ['home-am', 'home-pm', 'work', 'restaurant', 'school'])
    add_bundle(8, ['home-am', 'home-pm', 'shopping', 'work', 'restaurant', 'school'])
    elem.in_home_bundle = elem.bundles[0]
    
# creat all the objects related to the network
def creat_line_4node():
    # fare matrices
    fare_matrix_bus = { \
        1: {1:0, 2:5, 3:5, 4:8}, \
        2: {1:5, 2:0, 3:0, 4:5}, \
        3: {1:5, 2:0, 3:0, 4:5}, \
        4: {1:8, 2:5, 3:5, 4:0}
    }
    fare_matrix_sub = { \
        1: {1:00, 2:10, 3:15, 4:25}, \
        2: {1:10, 2:00, 3:10, 4:15}, \
        3: {1:15, 2:10, 3:00, 4:10}, \
        4: {1:25, 2:15, 3:10, 4:00}
    }
#   add_line(key, offset, headway, n_run, stop_list, time_list, fare_matrix, capacity)
    add_line(1,    5,      10,       289,    [1,2,4],   [20, 20], fare_matrix_bus, conf.CAPACITY_bus)
    add_line(2,    10,      10,       289,    [1,3,4],   [15, 15], fare_matrix_bus, conf.CAPACITY_bus)
    add_line(3,    15,      10,      289,    [1,2,3,4], [15, 10, 15], fare_matrix_bus, conf.CAPACITY_bus)
    add_line(-1,    5,      10,       289,    [4,2,1],   [20, 20], fare_matrix_bus, conf.CAPACITY_bus)
    add_line(-2,    10,      10,       289,    [4,3,1],   [15, 15], fare_matrix_bus, conf.CAPACITY_bus)
    add_line(-3,    15,      10,      289,    [4,3,2,1], [15, 10, 15], fare_matrix_bus, conf.CAPACITY_bus)
    add_line(10,    10,      5,       289,    [1,2,4],   [5, 5], fare_matrix_sub, conf.CAPACITY_sub)
    add_line(-10,    10,      5,       289,    [4,2,1],   [5, 5], fare_matrix_sub, conf.CAPACITY_sub)

def travel_time_curve(time, peak, Um):
    Sigma = 0.015
    Lambda = 1.0
    U0 = 0.8
    nominator = Sigma*Lambda*Um
    denominator = (math.exp( Sigma*(time-peak) ) *
        math.pow(1.0+math.exp( -Sigma*(time-peak) ), Lambda+1.0) )
    return U0 + nominator/denominator

def creat_static_travel_times():
    for origin in elem.zone_list:
        flow.static_travel_times[origin] = {}
        for dest in elem.zone_list:
            if origin == dest:
                flow.static_travel_times[origin][dest] = 0.0
            else:
                flow.static_travel_times[origin][dest] = 20.0

def creat_dyna_travel_times():
    creat_static_travel_times()
    for timeslice in xrange(min2slice(conf.DAY)):
        flow.dyna_travel_times.append(dict())
        for origin in elem.zone_list:
            flow.dyna_travel_times[timeslice][origin] = {}
            for dest in elem.zone_list:
                flow.dyna_travel_times[timeslice][origin][dest] = min2slice(\
                    flow.static_travel_times[origin][dest] * \
                    (travel_time_curve(slice2min(timeslice), 9*60, 600) + \
                    travel_time_curve(slice2min(timeslice), 18*60, 800)))
    
def creat_sidewalks_4node():
#   add_sidewalk(key, head, tail, walk_time, capacity)
    add_sidewalk(4,    10,   1,    5,     conf.CAPACITY_ped)
    add_sidewalk(5,    20,   2,    5,     conf.CAPACITY_ped)
    add_sidewalk(6,    30,   3,    5,     conf.CAPACITY_ped)
    add_sidewalk(7,    40,   4,    5,     conf.CAPACITY_ped)
    add_sidewalk(-4,    1,  10,    5,     conf.CAPACITY_ped)
    add_sidewalk(-5,    2,  20,    5,     conf.CAPACITY_ped)
    add_sidewalk(-6,    3,  30,    5,     conf.CAPACITY_ped)
    add_sidewalk(-7,    4,  40,    5,     conf.CAPACITY_ped)


def create_node_list():
    # create stop list
    for n in elem.nodes:
        if isinstance(elem.nodes[n], Stop):
            elem.stop_list.append(elem.nodes[n])
    # create zone list
    for n in elem.nodes:
        if isinstance(elem.nodes[n], Zone):
            elem.zone_list.append(elem.nodes[n])
    # create home list
    for z in elem.zone_list:
        if z.population > 1:
            elem.home_list.append(z)
    elem.zone_list.sort()
    print "home_list %s" % elem.home_list

def creat_traffic_zone_4node():
#   add_zone(key, activity_list, node_list, access_list, population)
    add_zone(10,   ['home-am','home-pm'], 30000)
    add_zone(20,   ['school'],            0)
    add_zone(30,   ['shopping', 'restaurant'],          0)
    add_zone(40,   ['work'],              0)
    create_node_list()

###################################
### load data sets
###################################
def load_4node_net():
    creat_traffic_zone_4node()
    creat_timetable_4node()
    creat_access_arc_4node()
    creat_activity_4node()
    creat_activity_pattern_4node()
    
def load_network(net_name):
    fun_name = 'load_'+net_name+'_net'
    globals()[fun_name]()
    
