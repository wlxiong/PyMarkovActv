# compute equilibrium flows
from shared.universe import flow
from utils.get import get_move_flow
from planning.dynaprog import calc_state_util, calc_activity_choice_prob, calc_socio_activity_util
from loading.load import build_choice_model, calc_inclusive_values, calc_commodity_steps, calc_state_flows
from loading.init import init_flow_variables, init_step_variables
from loading.init import init_state_util, init_transition_choice_prob, init_activity_choice_prob, init_socio_activity_util
from loading.init import init_state_flows, init_transition_flows
from stats.timer import print_current_time
from iofile.outputs import export_data

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
    
def find_fixed_point(N, case_name, corr):
    " Find the equilibrium flows using method of successive average (MSA). "

    # iterate demand and supply sides
    init_flow_variables()
    init_socio_activity_util()
    
    for iter_num in xrange(N): 
        
        print "\n  ### interation %d ###" % iter_num
        
        print '\n [initialization]'

        init_step_variables()
        init_state_util()
        init_transition_choice_prob()
        print_current_time()
        
        print '\n [dynamic choice]'

        calc_state_util()
        build_choice_model()
        calc_inclusive_values()
        calc_commodity_steps()
        print_current_time()

        print '\n [traffic loading]'

        init_state_flows(0.0)
        init_transition_flows(0.0)
        calc_state_flows()
        print_current_time()
        
        print '\n [intra-household interaction]'
        init_activity_choice_prob()
        calc_activity_choice_prob()
        calc_socio_activity_util()
        print_current_time()
        
        print '\n [update flows]'
        update_movement_flows(iter_num)
        update_commodity_flows(iter_num)
        print_current_time()
        
        export_data(case_name+'_r'+str(corr)+'_n'+str(iter_num))
