from time import clock

def print_current_time(last_time=[None]):
    if last_time[0] <> None:
        elapsed_time = clock() - last_time[0]
        print '\t\t\t\t\t...Elapsed Time: %3.1f s...' % (elapsed_time)
    last_time[0] = clock()
