# implementation of a schedule-based transit network

import math
import hashlib
from basic import *
import sys
sys.path.insert(0, 'D:\\Workspace\\MarkovActv')
from data.universal import *
from iofile.input import *


def main():
    creat_line_4node()
    creat_traffic_zone_4node()
    creat_sidewalks_4node()
    for n in base.nodes:
        print "%s" % n
    for l in base.lines:
        print "%s" % base.lines[l]
        print base.lines[l].timetable
    for w in base.walks:
        print "%s" % w


if __name__ == '__main__':
    main()

