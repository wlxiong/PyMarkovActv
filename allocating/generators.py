# assign values
from utils.convert import min2slice
from shared.universe import conf, util, elem
from routing.enum import find_all_path

def gen_activity_util():
    for timeslice in xrange(min2slice(conf.DAY)+1):
        util.activity_util[timeslice] = {}
        for activity in elem.activities.values():
            util.activity_util[timeslice][activity] = activity.discrete_util(timeslice)

def gen_path_set():
    for origin in elem.zone_list:
        elem.paths[origin] = {}
        for dest in elem.zone_list:
            elem.paths[origin][dest] = find_all_path(origin, dest)
