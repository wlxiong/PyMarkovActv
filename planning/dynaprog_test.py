# semi-Markov decision process
import math
import hashlib
import copy
import sys
sys.path.insert(0, 'D:\\Workspace\\MarkovActv')
from planner.dynaprog import *
from iofile.input import *
from iofile.output import *
from router.enum import *
from network.transit import *
from network.pedestrian import *


def main():
    creat_activity_4node()
    gen_activity_util()
    creat_activity_pattern_4node()
    creat_traffic_zone_4node()
    
    creat_line_4node()
    creat_sidewalks_4node()
    gen_path_set()

    init_state_util(float('-inf'))
    print "init_state_util(float('-inf'))"
    init_choice_prob(0.0)
    print 'init_choice_prob(0.0)'
    find_state_optimal_util()
    print 'find_state_optimal_util()'

    fout = open('optimal_util.log', 'w')
    export_optimal_util(fout)
##    for comm in enum_commodity():
##        print>>fout, " commodity %s" % comm
##        for timeslice in xrange(min2slice(param.DAY)-1,-1,-1):
##            for state in enum_state(comm, timeslice):
##                print>>fout, " timeslice %d, state %s" % (timeslice, state)
##                for trans in enum_transition(comm, timeslice, state):
##                    print>>fout, " transition %s" % trans,
##                print>>fout

    fout.close()

if __name__ == '__main__':
    main()

