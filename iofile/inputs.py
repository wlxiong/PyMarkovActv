# import data
import math 
from shared.universe import conf, elem, flow
from allocating.creators import add_activity, add_bundle
from allocating.creators import add_line, add_zone, add_sidewalk
from networks.basic import Zone
from networks.transit import Stop
from utils.convert import min2slice, slice2min


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

#############################
###     6 node network
#############################

def creat_activity_6node():
##  add_activity(name, U0, Um, Sigma, Lambda, Xi, time_win, min_duration, is_madatory, pref_timing):
    add_activity('home-am',    1.0, 400, -0.008, 1.0,   720, (0, 1440), 360, 0, -1)
    add_activity('home-pm',    1.0, 400, -0.008, 1.0,   720, (0, 1440), 360, 0, -1)
    add_activity('work',       0.0, 1000,  0.010, 1.0,   720, (0, 1440), 240, 1, 540)
    add_activity('school', 0.0, 160,  0.015, 1.0,   495, (0, 1440),  10, 0, -1)
    add_activity('shopping',   0.0, 400,  0.010, 1.0,  1170, (0, 1440),  10, 0, -1)
    elem.home_am_activity = elem.activities['home-am']
    elem.home_pm_activity = elem.activities['home-pm']

def creat_activity_bundle_6node():
#   add_bundle(key, activity_name_list)
    add_bundle(0, ['home-am', 'home-pm'])
    add_bundle(1, ['home-am', 'home-pm', 'work'])

    add_bundle(2, ['home-am', 'home-pm', 'work', 'shopping'])
    add_bundle(3, ['home-am', 'home-pm', 'work', 'school'])

    add_bundle(4, ['home-am', 'home-pm', 'work', 'shopping', 'school'])

    elem.in_home_bundle = elem.bundles[0]

def creat_line_6node():
	pass

def creat_road_6node():
	add_road(1,		1,		3,		30,		3000/60.0)
	add_road(2,		1,		5,		15,		2000/60.0)
	add_road(3,		2,		5,		15,		2000/60.0)
	add_road(4,		2,		4,		45,		4000/60.0)
	add_road(5,		5,		6,		15,		3000/60.0)
	add_road(6,		6,		3,		15,		2000/60.0)
	add_road(7,		6,		4,		15,		2000/60.0)

	add_road(-1,	3,		1,		30,		3000/60.0)
	add_road(-2,	5,		1,		15,		2000/60.0)
	add_road(-3,	5,		2,		15,		2000/60.0)
	add_road(-4,	4,		2,		45,		4000/60.0)
	add_road(-5,	6,		5,		15,		3000/60.0)
	add_road(-6,	3,		6,		15,		2000/60.0)
	add_road(-7,	4,		6,		15,		2000/60.0)

def creat_sidewalks_6node():
#   add_sidewalk(key, head, tail, walk_time, capacity)
    add_sidewalk( 8,    10,   1,    5,     conf.CAPACITY_ped)
    add_sidewalk( 9,    20,   2,    5,     conf.CAPACITY_ped)
    add_sidewalk(10,    30,   3,    5,     conf.CAPACITY_ped)
    add_sidewalk(11,    40,   4,    5,     conf.CAPACITY_ped)
	add_sidewalk(12,    50,   5,    5,     conf.CAPACITY_ped)
	add_sidewalk(13,    60,   6,    5,     conf.CAPACITY_ped)
	
    add_sidewalk( -8,    1,   10,    5,     conf.CAPACITY_ped)
    add_sidewalk( -9,    2,   20,    5,     conf.CAPACITY_ped)
    add_sidewalk(-10,    3,   30,    5,     conf.CAPACITY_ped)
    add_sidewalk(-11,    4,   40,    5,     conf.CAPACITY_ped)
	add_sidewalk(-12,    5,   50,    5,     conf.CAPACITY_ped)
	add_sidewalk(-13,    6,   60,    5,     conf.CAPACITY_ped)

def creat_traffic_zone_6node():
#   add_zone(key, activity_list, node_list, access_list, population)
	add_zone(10,   ['work'],              0)
	add_zone(20,   ['work'],              0)
    add_zone(30,   ['home-am','home-pm'], 30000)
	add_zone(40,   ['home-am','home-pm'], 40000)
    add_zone(50,   ['school'],            0)
    add_zone(60,   ['shopping'],          0)
    create_node_list()


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

def creat_road_4node():
	pass

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

def load_network(case_name):
	globals()['creat_traffic_zone_'+case_name]()
	globals()['creat_line_'+case_name]()
	globals()['creat_road_'+case_name]()
    globals()['creat_sidewalks_'+case_name]()

def load_activity(net_name):
	globals()['creat_activity_'+case_name]()
	globals()['creat_activity_bundle_'+case_name]()

