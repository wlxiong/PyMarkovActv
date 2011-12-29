# create elements
from shared.universe import elem
from events.activity import Activity, Bundle
from networks.basic import Node 
from networks.motor import Road
from networks.location import Zone, Home, Work 
from networks.transit import Stop, TransitLine
from networks.pedestrian import Sidewalk

def add_activity(name, U0, Um, Sigma, Lambda, Xi, \
                 time_win, min_duration, \
                 is_joint, is_madatory, pref_timing):
    elem.activities[name] = Activity(name, U0, Um, Sigma, Lambda, Xi, \
                                     time_win, min_duration, \
                                     is_joint, is_madatory, pref_timing)
    if name == 'home-am':
        elem.home_am_activity = elem.activities['home-am']
    elif name == 'home-pm':
        elem.home_pm_activity = elem.activities['home-pm']
    elif name == 'work':
        elem.work_activity = elem.activities['work']

def add_bundle(key, activity_name_list):
    bundle_name = 'PN' + str(key)
    activity_list = map(lambda actv_name: elem.activities[actv_name], \
                        activity_name_list)
    elem.bundles[key] = Bundle(bundle_name, activity_list)

def get_stop(key):
    "Return the stop with the given name, creating it if necessary. "
    if key not in elem.nodes:
        stop_name = 'ST' + str(key)
        elem.nodes[key] = Stop(stop_name)
    return elem.nodes[key]

def get_node(key):
    "Return the node with the given name, creating it if necessary. "
    if key not in elem.nodes:
        node_name = 'ND' + str(key)
        elem.nodes[key] = Node(node_name)
    return elem.nodes[key]

def add_zone(key, activity_name_list):
    zone_name = 'ZN' + str(key)
    activity_list = map(lambda actv_name: elem.activities[actv_name], activity_name_list)
    # add it to the node dict and zone list
    elem.nodes[key] = Zone(zone_name, activity_list)
    elem.zone_list.append(elem.nodes[key])
    
def add_home(key, houses, rent):
    home_name = 'HH' + str(key)
    elem.nodes[key] = Home(home_name, [elem.home_am_activity, elem.home_pm_activity], houses, rent)
    # add it to the home and zone lists
    elem.home_list.append(elem.nodes[key])
    elem.zone_list.append(elem.nodes[key])

def add_work(key, jobs, salary):
    work_name = 'WW' + str(key)
    elem.nodes[key] = Work(work_name, [elem.work_activity], jobs, salary)
    # add it to the work and zone lists
    elem.work_list.append(elem.nodes[key])
    elem.zone_list.append(elem.nodes[key])

def add_sidewalk(key, head_name, tail_name, walk_time, capacity):
    sidewalk_name = 'SW' + str(key)
    get_node(head_name)
    get_node(tail_name)
    head_node, tail_node = elem.nodes[head_name], elem.nodes[tail_name]
    elem.walks[key] = Sidewalk(sidewalk_name, head_node, tail_node, walk_time, capacity)

def add_road(key, head_name, tail_name, drive_time, capacity, length):
    road_name = 'RD' + str(key)
    get_node(head_name)
    get_node(tail_name)
    head_node, tail_node = elem.nodes[head_name], elem.nodes[tail_name]
    elem.roads[key] = Road(road_name, head_node, tail_node, drive_time, capacity, length)

def gen_timetable(offset, headway, dwell_time, total_run, in_vehicle_time):
    " Generate the timetable with given parameters. "
    timetable = [None] * total_run
    sum_in_vehicle_time = [sum(in_vehicle_time[0:i+1]) for i in xrange(len(in_vehicle_time))]
    for run in xrange(total_run):
        move_time = lambda tt: tt + headway*run + offset + dwell_time
        timetable[run] = map(move_time, [0] + sum_in_vehicle_time)
    return timetable

def add_line(key, offset, headway, n_run, stop_name_list, time_list, fare_matrix, capacity):
    line_name = 'LN' + str(key)
    # generate stop list
    stop_list = []
    for stop_name in stop_name_list:
        new_stop = get_stop(stop_name)
        stop_list.append(new_stop)
    # generate timetable
    timetable = gen_timetable(offset, headway, 0, n_run, time_list)
    elem.lines[key] = TransitLine(line_name, timetable, stop_list, fare_matrix, capacity)
