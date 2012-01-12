# import data
from shared.universe import conf, elem
from allocating.creators import add_activity, add_bundle, add_person
from allocating.creators import add_line, add_road, add_zone, add_home, add_work, add_sidewalk


#############################
###     6 node network
#############################

def creat_activity_6node():
##  add_activity(name, U0, Um, Sigma, Lambda, Xi, time_win, min_duration, is_joint, is_madatory, pref_timing):
    add_activity('home-am',          1.0,  600, -0.010, 1.0,   720, (  0,  720), 360, 1, 0,  -1)
    add_activity('home-pm',          1.0,  600, -0.010, 1.0,   720, (720, 1440), 360, 1, 0,  -1)
    add_activity('work',             0.0, 1600,  0.010, 1.0,   720, (240, 1440), 240, 0, 1, 540)
    add_activity('restaurent',       0.0,  420,  0.010, 1.0,  1170, (720, 1440),  10, 0, 0,  -1)
    add_activity('joint-restaurent', 0.0,  100,  0.010, 1.0,  1170, (720, 1440),  10, 1, 0,  -1)
    add_activity('shopping',         0.0,  500,  0.010, 1.0,  1110, (720, 1440),  10, 0, 0,  -1)
    add_activity('joint-shopping',   0.0,  120,  0.010, 1.0,  1110, (720, 1440),  10, 1, 0,  -1)

def creat_activity_bundle_6node():
#   add_bundle(key, activity_name_list)
    # individual activities
    add_bundle(0, ['home-am', 'home-pm'])
    add_bundle(1, ['home-am', 'home-pm', 'work'])

    add_bundle(2, ['home-am', 'home-pm', 'work', 'shopping'])
    add_bundle(3, ['home-am', 'home-pm', 'work', 'restaurent'])
    
    add_bundle(4, ['home-am', 'home-pm', 'work', 'shopping', 'restaurent'])

    # joint activities
    add_bundle(5, ['home-am', 'home-pm', 'work', 'joint-shopping'])
    add_bundle(6, ['home-am', 'home-pm', 'work', 'joint-restaurent'])
    
    add_bundle(7, ['home-am', 'home-pm', 'work', 'joint-shopping', 'restaurent'])
    add_bundle(8, ['home-am', 'home-pm', 'work', 'shopping', 'joint-restaurent'])
    add_bundle(9, ['home-am', 'home-pm', 'work', 'joint-shopping', 'joint-restaurent'])
    
    elem.in_home_bundle = elem.bundles[0]

def creat_line_6node():
    pass

def creat_road_6node():
    add_road(1,     1,      3,      40,     3000, 40.0)
    add_road(2,     1,      5,      20,     2000, 15.0)
    add_road(3,     2,      5,      20,     2000, 15.0)
    add_road(4,     2,      4,      60,     4000, 50.0)
    add_road(5,     5,      6,      20,     3000, 20.0)
    add_road(6,     6,      3,      20,     2000, 20.0)
    add_road(7,     6,      4,      20,     2000, 20.0)
                                                
    add_road(-1,    3,      1,      40,     3000, 40.0)
    add_road(-2,    5,      1,      20,     2000, 15.0)
    add_road(-3,    5,      2,      20,     2000, 15.0)
    add_road(-4,    4,      2,      60,     4000, 50.0)
    add_road(-5,    6,      5,      20,     3000, 20.0)
    add_road(-6,    3,      6,      20,     2000, 20.0)
    add_road(-7,    4,      6,      20,     2000, 20.0)

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
#   add_zone(key, activity_list)
    add_work(10,   10000, 0.0)
    add_work(20,   10000, 10.0)
    add_home(30,   20000, 0.0)
    # add_home(40,   20000, 0.0)
    
    # persons in the household
    add_person(1, 10, 30, 30000)
    add_person(2, 20, 30, 30000)

    add_zone(40,   ['restaurent', 'joint-restaurent'])
    add_zone(50,   ['shopping', 'joint-shopping'])
    add_zone(60,   ['shopping', 'restaurent'])

    elem.zone_list.sort()


#############################
###     4 node network
#############################

def creat_activity_4node():
##  add_activity(name, U0, Um, Sigma, Lambda, Xi, time_win, min_duration, is_madatory, pref_timing):
    add_activity('home-am',    1.0, 400, -0.008, 1.0,   720, (0, 1440), 360, 0, -1)
    add_activity('home-pm',    1.0, 400, -0.008, 1.0,   720, (0, 1440), 360, 0, -1)
    add_activity('work',       0.0,1000,  0.010, 1.0,   720, (0, 1440), 240, 1, 540)
    add_activity('school',     0.0, 160,  0.015, 1.0,   495, (0, 1440),  10, 0, -1)
    add_activity('shopping',   0.0, 400,  0.010, 1.0,  1170, (0, 1440),  10, 0, -1)
    add_activity('restaurant', 0.0, 200,  0.030, 1.0,  1140, (0, 1440),  10, 0, -1)
    # elem.home_am_activity = elem.activities['home-am']
    # elem.home_pm_activity = elem.activities['home-pm']

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
    elem.zone_list.sort()

###################################
### load data sets
###################################

def load_network(case_name):
    globals()['creat_traffic_zone_'+case_name]()
    globals()['creat_line_'+case_name]()
    globals()['creat_road_'+case_name]()
    globals()['creat_sidewalks_'+case_name]()

def load_activity(case_name):
    globals()['creat_activity_'+case_name]()
    globals()['creat_activity_bundle_'+case_name]()

