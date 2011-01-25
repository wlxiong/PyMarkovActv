# compute equilibrium flows
from shared.universe import flow
from utils.get import get_move_flow
from planning.dynaprog import calc_state_optimal_util
from loading.load import build_choice_model, calc_choice_volume, calc_state_flows
from loading.init import init_movement_steps, init_movement_flows
from loading.init import init_state_optimal_util, init_transition_choice_prob
from loading.init import init_state_flows, init_transition_flows
from stats.timer import print_current_time

def update_movement_flows(iter_num):
    for each_move in flow.movement_flows.keys():
        flow.movement_flows[each_move] *= (iter_num / (iter_num + 1.0))
    for each_move in flow.movement_steps.keys():
        get_move_flow(each_move)
        flow.movement_flows[each_move] += (flow.movement_steps[each_move] / (iter_num + 1.0))

def find_fixed_point(N):
    " Find the equilibrium flows using method of successive average (MSA). "
    # iterate demand and supply sides
    init_movement_flows()
    print '\n init_movement_flows()'
    for iter_num in xrange(N): 
        
        print "\n  ### interation %d ###" % iter_num

        print '\n [dynamic programming]'
        init_movement_steps()
        print '  init_movement_steps()'
        print_current_time()
        init_state_optimal_util(float('-inf'))
        print "  init_state_optimal_util(float('-inf'))"
        print_current_time()
        init_transition_choice_prob(0.0)
        print '  init_transition_choice_prob(0.0)'
        print_current_time()
        
        calc_state_optimal_util()
        print '  calc_state_optimal_util()'
        print_current_time()
        build_choice_model()
        print '  build_choice_model()'
        print_current_time()
        calc_choice_volume()
        print '  calc_choice_volume()'
        print_current_time()
        
        print '\n [traffic assignment]'
        init_state_flows(0.0)
        print '  init_state_flows(0.0)'
        print_current_time()
        init_transition_flows(0.0)
        print '  init_transition_flows(0.0)'
        print_current_time()

        calc_state_flows()
        print '  calc_state_flows()'
        print_current_time()
        update_movement_flows(iter_num)
        print "  update_movement_flows(%d)" % iter_num
        print_current_time()
