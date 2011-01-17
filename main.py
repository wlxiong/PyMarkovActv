# stochastic discrete choice model
## import pycallgraph
## pycallgraph.start_trace()
import iofile.output

def sim_rand_assign(N, case):
    "Generate random utility of activity and assign the passengers to network. "
    for n in range(N):
        print '\n*** %d ***' % n
        init_flow_step(0.0)
        init_path_flow(10.0)
        calc_flow_step()
        update_link_flow(1)
        # initialize the activities
    ##     gen_activity_util()
        gen_rand_activity_util()
        # find equilibrium flows
        init_avg_trip()
        find_fixed_point(num_iter)
        # export and visualize data
        export_file_name = case + '-' + str(n)
        export_data(export_file_name)
        export_sample_zn_png()
    
def main():
    
    # load data sets
    case = '4node'
    load_network(case)
    # initialize the transit network
    gen_path_set()
    gen_flow_set()
    sim_rand_assign(num_sample, case)
#    draw_zone_passenger(10)
#    draw_zone_passenger(5)
#    draw_zone_passenger(2)
#    plt.show()
    
    
if __name__ == '__main__':
##     prof = hotshot.Profile("hotshot_stats")
##     prof.runcall(main)
##     prof.close()
#    main()
##    pycallgraph.make_dot_graph('SA-main.png')
