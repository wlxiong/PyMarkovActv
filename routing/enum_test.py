# enumerate paths
import sys
sys.path.insert(0, 'D:\\Workspace\\MarkovActv')
from iofile.input import *
from router.enum import *

def find_all_path(start_node, end_node, thepath=Path()):
    "Find all possible paths between nodes[start] and nodes[end] when departing at clock time. "
    if start_node == end_node:
        return [thepath]
    path_set = []
    for each_vector in start_node.adjacent_vectors:
        if isinstance(each_vector, Sidewalk):
            sidewalk = each_vector
            next_node = sidewalk.tail_node
            if next_node not in thepath.nodes_on_path:
                extpath = thepath + Path([start_node, next_node], \
                                         [Edge(sidewalk, start_node, next_node)])
                newpaths = find_all_path(next_node, end_node, extpath)
                for newpath in newpaths:
                    path_set.append(newpath)
        if isinstance(each_vector, TransitLine):
            line = each_vector
            i_start = line.stop_order[start_node]
            next_stop_set = line.stops_on_line[i_start+1:i_start+2]
            for next_stop in next_stop_set:
                if next_stop not in thepath.nodes_on_path:
                    extpath = thepath + Path([start_node, next_stop], \
                                             [Edge(line, start_node, next_stop)])
                    newpaths = find_all_path(next_stop, end_node, extpath)
                    for newpath in newpaths:
                        path_set.append(newpath)
##    if isinstance(start_node, Road):
##        pass
    return path_set


def gen_path_set():
    for origin in base.zone_list:
        base.paths[origin] = {}
        for dest in base.zone_list:
            base.paths[origin][dest] = find_all_path(origin, dest)

def update_path_cost(origin, dest):
    for each_path in base.paths[origin][dest]:
        each_path.update_travel_cost()
        
def main():
    creat_line_4node()
    creat_traffic_zone_4node()
    creat_sidewalks_4node()
    gen_path_set()

    for origin in base.zone_list:
        for dest in base.zone_list:
            print origin, dest
            for each_path in base.paths[origin][dest]:
                print 
                print each_path
                print each_path.calc_travel_impedences(0)
            print

if __name__ == '__main__':
    main()

