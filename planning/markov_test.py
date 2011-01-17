import math
import hashlib
import copy
import sys
sys.path.insert(0, 'D:\\Workspace\\MarkovActv')
from router.enum import *
from data.universal import *
from planner.markov import *
from planner.dynaprog import *
from iofile.input import *


def main():
    creat_activity_4node()
    creat_activity_pattern_4node()
    creat_traffic_zone_4node()
    
    creat_line_4node()
    creat_sidewalks_4node()
    gen_path_set()

    init_state_util(float('-inf'))
    
    fout = open('markov_state.log', 'w')
    for comm in enum_commodity():
        print>>fout, " commodity %s" % comm
        for timeslice in xrange(min2slice(param.DAY)-1,-1,-1):
            for state in enum_state(comm, timeslice):
                print>>fout, " timeslice %d, state %s" % (timeslice, state)
                for trans in enum_transition(comm, timeslice, state):
                    print>>fout, " transition %s" % trans,
                print>>fout

    fout.close()


if __name__ == '__main__':
    main()

