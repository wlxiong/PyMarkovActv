# some tools
import math
from shared.universe import conf

# conversion of timeslice and minutes
def min2slice(minute):
    if math.isinf(minute):
        return minute
    return int(math.floor((float(minute)/conf.TICK)+0.5))

def slice2min(timeslice):
    if math.isinf(timeslice):
        return timeslice
    return float(timeslice)*conf.TICK

def main():
    
    print slice2min(3)
    print min2slice(9)
    
    
if __name__ == '__main__':
    main()

