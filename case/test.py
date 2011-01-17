# just a test

import math
import hashlib

class node:
    def __init__(self, node_name):
        self.node_name = node_name
        self.adj_list = []

    def __repr__(self):
        return "%d" % self.node_name

class grid:
    "A grid in the spacetime network is a pair of node and time. "
    def __init__(self, line, node, time):
        self.line = line
        self.node = node
        self.time = time
        
    def __repr__(self):
        return "%s(%d): %.1f" % (self.node, self.line, self.time)
        
    def __eq__(self, other):
        return self.line == other.line and self.node == other.node and self.time == other.time
        
    def __hash__(self):
        return int(hashlib.md5(repr(self)).hexdigest(), 16)


class Ddict(dict):
    def __init__(self, default=None):
        self.default = default

    def __getitem__(self, key):
        if not self.has_key(key):
            self[key] = self.default()
        return dict.__getitem__(self, key)
        
        
def main():
    a = [3,4,5]
    b = [5,6,4,3]
    c = [5,6,4,3]
    
    d = a+[c]
    print d
    if 6<9<=100:
        print True

    node1 = node(10)
    node2 = node(20)
    line0 = 0
    time0 = 99
    gg = grid(line0, node1, time0)
    print node1
    gg.node.node_name = 30
    print node1
    
if __name__ == '__main__':
    main()
