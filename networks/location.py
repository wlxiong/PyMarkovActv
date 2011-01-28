# Classes for ctivity locations
from networks.basic import Node


class Zone(Node):
    "A zone is a area where people participate various activities. "
    def __init__(self, name, activity_list):
        super(Zone, self).__init__(name)
        self.involved_activities = activity_list
        for each_actv in self.involved_activities:
            each_actv.add_location(self)
        

class Home(Zone):
    "A home is a zone that people can reside at. "
    def __init__(self, name, activity_list, houses, rent):
        super(Home, self).__init__(name, activity_list)
        self.houses, self.rent = houses, rent


class Work(Zone):
    "A work is a place that people find a job. "
    def __init__(self, name, activity_list, jobs, salary):
        super(Work, self).__init__(name, activity_list)
        self.jobs, self.salary = jobs, salary
