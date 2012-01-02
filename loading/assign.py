# compute equilibrium flows
from shared.universe import flow
from utils.get import get_move_flow
from planning.dynaprog import calc_state_util
from loading.load import build_choice_model, calc_inclusive_values, calc_commodity_steps, calc_state_flows
from loading.init import init_flow_variables, init_step_variables
from loading.init import init_state_optimal_util, init_transition_choice_prob
from loading.init import init_state_flows, init_transition_flows
from stats.timer import print_current_time

def update_movement_flows(iter_num):
    for each_move in flow.movement_flows:
        flow.movement_flows[each_move] *= (iter_num / (iter_num + 1.0))
    for each_move in flow.movement_steps:
        get_move_flow(each_move)
        flow.movement_flows[each_move] += (flow.movement_steps[each_move] / (iter_num + 1.0))

def update_commodity_flows(iter_num):
    for each_comm in flow.commodity_flows:
        flow.commodity_flows[each_comm] *= (iter_num / (iter_num + 1.0))
    for each_comm in flow.commodity_steps:
        flow.commodity_flows[each_comm] += (flow.commodity_steps[each_comm] / (iter_num + 1.0))

def load_all_flows():
    print '\n [dynamic programming]'
    init_step_variables()
    print '  init_step_variables()'
    print_current_time()
    init_state_optimal_util(float('-inf'))
    print "  init_state_optimal_util(float('-inf'))"
    print_current_time()
    init_transition_choice_prob(0.0)
    print '  init_transition_choice_prob(0.0)'
    print_current_time()
    
    print '\n [combined choice]'
    calc_state_util()
    print '  calc_state_optimal_util()'
    print_current_time()
    build_choice_model()
    print '  build_choice_model()'
    print_current_time()
    calc_inclusive_values()
    print '  calc_inclusive_values()'
    print_current_time()
    calc_commodity_steps()
    print '  calc_commodity_steps()'
    print_current_time()
    
    print '\n [traffic loading]'
    init_state_flows(0.0)
    print '  init_state_flows(0.0)'
    print_current_time()
    init_transition_flows(0.0)
    print '  init_transition_flows(0.0)'
    print_current_time()
    calc_state_flows()
    print '  calc_state_flows()'
    print_current_time()

def find_fixed_point(N):
    " Find the equilibrium flows using method of successive average (MSA). "
    # iterate demand and supply sides
    init_flow_variables()
    print '\n init_flow_variables()'
    for iter_num in xrange(N): 
        
        print "\n  ### interation %d ###" % iter_num
        load_all_flows()
        
        print '\n [update flows]'
        update_movement_flows(iter_num)
        print "  update_movement_flows(%d)" % iter_num
        print_current_time()
        update_commodity_flows(iter_num)
        print "  update_commodity_flows(%d)" % iter_num
        print_current_time()
