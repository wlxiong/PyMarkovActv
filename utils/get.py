# get objects
from shared.universe import flow

def get_move_flow(move):
    " Return the flow with the given name, creating it if necessary. "
    if move not in flow.movement_flows:
        flow.movement_flows[move] = 0.0
    return flow.movement_flows[move]

def get_move_step(move):
    " Return the step with the given name, creating it if necessary. "
    if move not in flow.movement_steps:
        flow.movement_steps[move] = 0.0
    return flow.movement_steps[move]

def sorted_dict_values(adict):
    keys = adict.keys( )
    keys.sort( )
    return [adict[key] for key in keys]
