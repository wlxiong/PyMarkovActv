# Activity class
import math
import hashlib
import scipy.integrate as integrate
import sys
sys.path.insert(0, 'D:\\Workspace\\MarkovActv')
from activity.activity import *
from iofile.input import *
from iofile.output import *

    
def main():
    fout = open('activity_util.log', 'w')
    creat_activity_4node()
    gen_activity_util()
    export_activity_util(fout)
    creat_activity_pattern_4node()
    for key, pattern in base.patterns.items():
        print key, pattern
 
if __name__ == '__main__':
    main()
    
    
