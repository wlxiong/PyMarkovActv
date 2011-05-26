# get objects
from shared.universe import flow

def get_move_flow(move):
    " Return the flow with the given name, creating it if necessary. "
    try:
        return flow.movement_flows[move]
    except KeyError:
        flow.movement_flows[move] = 0.0
        return flow.movement_flows[move]

def get_move_step(move):
    " Return the step with the given name, creating it if necessary. "
    try:
        return flow.movement_steps[move]
    except KeyError:
        flow.movement_steps[move] = 0.0
        return flow.movement_steps[move]
