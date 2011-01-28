from shared.universe import flow
from utils.get import get_move_flow
from networks.motor import Road 

def calc_total_emission():
    total_emission = 0.0
    for each_move in flow.movement_flows:
        move_flow = get_move_flow(each_move)
        related_vector   = each_move.related_edge.related_vector
        if isinstance(related_vector, Road):
            travel_time      = related_vector.calc_travel_time(move_flow)
            vehicle_emission = related_vector.calc_vehicle_emission(travel_time)
            total_emission  += vehicle_emission
    return total_emission
