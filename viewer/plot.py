# plot the data
import math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.ticker as ticker
from utils.convert import min2slice
from shared.universe import conf, elem, flow

def draw_zone_population(bar_width):
    # average number of passengers in each aggregate time interval
    avg_zone_population = [None] * len(elem.zone_list)
    for i, each_zone in enumerate(elem.zone_list):
        avg_zone_population[i] = []
        for lower in range(0, min2slice(conf.DAY), bar_width):
            upper = min(lower+bar_width, min2slice(conf.DAY))
            sum_zone_population = sum([flow.zone_population[timeslice][each_zone] \
                                       for timeslice in xrange(lower, upper)]) 
            avg_zone_population[i].append(sum_zone_population/(upper-lower) )

    # plot figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    colors = ['r', 'g', 'b', 'y']
    cc = colors[0:len(elem.zone_list)]
    ordered_zone_population = sorted(avg_zone_population, key=sum)
    for c, z in zip(cc, xrange(len(elem.zone_list))):
        xs = range(int(math.ceil(min2slice(conf.DAY)/float(bar_width))))
        ys = ordered_zone_population[z]
##         print xs
##         print ys
        ax.bar(xs, ys, zs=z*10, zdir='y', color=c, linewidth=None, alpha=0.8)

##     day_len = int(math.ceil(min2slice(DAY)/float(slice_width)))+1
##     xtick_location = range(0, day_len, day_len/4)
##     ax.set_xticks([5, 10])
##     ax.set_xticklabels(['5', '10'])
##     ax.set_yticks(range(len(zone_list) ))
##     ax.set_yticklabels(['5', '10'])
##     ax.set_zticks([10000, 20000, 30000])
##     ax.set_zticklabels(['10,000', '20,000', '30,000'])

    ax.w_yaxis.set_major_locator(ticker.FixedLocator(range(0, 10*len(elem.zone_list), 10)))
    ax.w_yaxis.set_major_formatter(ticker.FuncFormatter(lambda i, j: elem.zone_list[i/10].name))
    for tl in ax.w_xaxis.get_ticklabels():
        tl.set_ha('right')
        tl.set_rotation(30)

    ax.set_xlabel('Time')
#    ax.set_ylabel('Activity locations')
    ax.set_zlabel('Population')
    plt.show()

