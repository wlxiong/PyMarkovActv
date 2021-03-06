# The simulation world

class Element(object):
    # most of the variables in Element are indexed by their names or IDs
    def __init__(self):
        
        # basic elements of the network
        # 1-dimension list nested in 2-dimension dict, 
        # i.e. paths[origin][destination][path_id]
        self.paths = {}
        # 2-dimension dict, i.e. paths[origin][destination]
        self.shortest_path = {}
        # 1-dimension dict, i.e. lines[line_id]
        self.lines = {}
        # 1-dimension dict, i.e. walks[walk_id]
        self.walks = {}
        # 1-dimension dict, i.e. roads[walk_id]
        self.roads = {}
        # 1-dimension dict, i.e. nodes[node_id]
        self.nodes = {}
        
        # activity destinations
        # 1-dimension list
        self.zone_list = []
        # 1-dimension list 
        self.work_list = []
        # 1-dimension list
        self.home_list = []
        
        # activities 
        # 1-dimension dict, i.e. activities[activity_name]
        self.activities = {}
        # 1-dimension dict, i.e. bundles[bundle_name]
        self.bundles = {}
        # in-home activity pattern
        self.in_home_bundle = None
        # special activities
        self.home_am_activity = None
        self.home_pm_activity = None
        self.work_activity = None
        
        # choice alternatives
        self.person_alt = {}
        self.in_home_alt = {}
        self.out_of_home_alt = {}
        self.bundle_alt = {}

        # persons in the household
        # 1-dimension dict, i.e. persons[person_id]
        self.persons = {}
        # 1-dimension list
        self.person_list = []
        # 1-dimension dict, i.e. person_flows[person]
        self.person_flows = {}
