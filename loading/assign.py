# compute equilibrium flows
from utils.convert import min2slice
from utils.get import get_move_flow
from shared.universe import flow, conf
from planning.dynaprog import calc_state_optimal_util
from loading.load import calc_location_flows, calc_commodity_flows, calc_state_flows
from loading.init import init_flow_variables, init_step_variables
from loading.init import init_state_optimal_util, init_transition_choice_prob
from loading.init import init_state_steps, init_transition_flows
from iofile.outputs import export_optimal_util
from stats.timer import print_current_time

def update_movement_flows(iter_num):
    for each_move in flow.movement_flows:
        flow.movement_flows[each_move] *= (iter_num / (iter_num + 1.0) )
    for each_move in flow.movement_steps:
        get_move_flow(each_move)
        flow.movement_flows[each_move] += (flow.movement_steps[each_move] / (iter_num + 1.0) )

def update_state_flows(iter_num):
    for comm in flow.state_flows:
        for timeslice in xrange(min2slice(conf.DAY)+1):
            for state in flow.state_flows[comm][timeslice]:
                flow.state_flows[comm][timeslice][state] *= (iter_num / (iter_num + 1.0) )
    for comm in flow.state_steps:
        for timeslice in xrange(min2slice(conf.DAY)+1):
            for state in flow.state_steps[comm][timeslice]:
                flow.state_flows[comm][timeslice][state] += (flow.state_steps[comm][timeslice][state] / (iter_num + 1.0) )
    
def update_commodity_flows(iter_num):
    for each_comm in flow.commodity_flows:
        flow.commodity_flows[each_comm] *= (iter_num / (iter_num + 1.0))
        flow.commodity_flows[each_comm] += (flow.commodity_steps[each_comm] / (iter_num + 1.0) )

def update_housing_flows(iter_num):
    # print util.housing_util
    # print flow.housing_flows
    # print flow.housing_steps
    for each_comm in flow.housing_flows:
        flow.housing_flows[each_comm] *= (iter_num / (iter_num + 1.0) )
        flow.housing_flows[each_comm] += (flow.housing_steps[each_comm] / (iter_num + 1.0) )
    # print flow.housing_flows
    
def calc_utils():
    print '\n [dynamic programming]'
    init_state_optimal_util(None)
    print "  init_state_optimal_util(None)"
    print_current_time()
    init_transition_choice_prob(0.0)
    print '  init_transition_choice_prob(0.0)'
    print_current_time()
    calc_state_optimal_util()
    print '  calc_state_optimal_util()'
    print_current_time()

def calc_flows():
    print '\n [combined choice]'
    # build_choice_model()
    # print '  build_choice_model()'
    # print_current_time()
    calc_location_flows()
    print '  calc_location_flows()'
    print_current_time()
    calc_commodity_flows()
    print '  calc_commodity_flows()'
    print_current_time()

def load_flows():
    print '\n [traffic loading]'
    init_state_steps(0.0)
    print '  init_state_steps(0.0)'
    print_current_time()
    init_transition_flows(0.0)
    print '  init_transition_flows(0.0)'
    print_current_time()
    calc_state_flows()
    print '  calc_state_flows()'
    print_current_time()

def update_flows(iter_num):
    print '\n [update flows]'
    update_movement_flows(iter_num)
    print "  update_movement_flows(%d)" % iter_num
    print_current_time()
    update_state_flows(iter_num)
    print "  update_state_flows(%d)" % iter_num
    print_current_time()
    update_commodity_flows(iter_num)
    print "  update_commodity_flows(%d)" % iter_num
    print_current_time()
    update_housing_flows(iter_num)
    print "  update_housing_flows(%d)" % iter_num
    print_current_time()

def find_init_solution():
    print "\n  ### initialize ###"
    init_flow_variables()
    calc_utils()
    load_flows()
    update_flows(0.0)
    
def find_fixed_point(N):
    " Find the equilibrium flows using method of successive average (MSA). "
    # iterate demand and supply sides
    find_init_solution()
    for iter_num in xrange(1,N+1): 
        print "\n  ### interation %d ###" % iter_num
        init_step_variables()
        print '  init_step_variables()'
        print_current_time()
        calc_utils()
        calc_flows()
        load_flows()
        update_flows(iter_num)
        