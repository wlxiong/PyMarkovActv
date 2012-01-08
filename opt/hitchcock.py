# Solve transportation problem using PuLP modeler functions
from pulp import makeDict, LpProblem, LpMinimize, LpContinuous, LpVariable, LpStatus, lpSum, value, solvers

class TransProblem(object):
    def __init__(self, home_list, work_list, util_matrix):
        """ Input a list of utils
            utils = [   #Works
                    #1 2 3 4 5
                    [2,4,5,2,1],#A   Homes
                    [3,1,3,2,3] #B
                    ]
        """
        self.util_matrix = util_matrix
        self.homes = dict((home, home.houses) for home in home_list)
        self.works = dict((work, work.jobs) for work in work_list)
        self.utils = makeDict([home_list, work_list], util_matrix, 0)

        # Creates the 'prob' variable to contain the problem data
        self.prob = LpProblem("Residential Location Choice Problem",LpMinimize)

        # Creates a list of tuples containing all the possible location choices
        self.choices = [(h, w) for h in self.homes for w in self.works.keys()]

        # A dictionary called 'volumes' is created to contain the referenced variables(the choices)
        self.volumes = LpVariable.dicts("choice",(self.homes,self.works),0,None,LpContinuous)

        # The objective function is added to 'prob' first
        self.prob += lpSum([self.volumes[h][w] * self.utils[h][w] for (h,w) in self.choices]), "Sum_of_Transporting_Costs"

        # The supply maximum constraints are added to prob for each supply node (home)
        for h in self.homes:
            self.prob += lpSum([self.volumes[h][w] for w in self.works]) <= self.homes[h], "Sum_of_Products_out_of_Home_%s"%h

        # The demand minimum constraints are added to prob for each demand node (work)
        for w in self.works:
            self.prob += lpSum([self.volumes[h][w] for h in self.homes]) >= self.works[w], "Sum_of_Products_into_Work%s"%w
        
    def solve(self):
        # The problem data is written to an .lp file
        self.prob.writeLP("ResidentialLocationChoiceProblem.lp")

        # The problem is solved using PuLP's choice of Solver
        self.prob.solve(solvers.GLPK())
        
        # print the utility matrix
        print "Utility Matrix", self.util_matrix
        
        # The status of the solution is printed to the screen
        print "Status:", LpStatus[self.prob.status]
    
        # The optimised objective function value is printed to the screen
        print "Total Utility = ", value(self.prob.objective)

    def get_solution(self):
        # put the solution variables into a dict 
        sol_var = {}
        for vol in self.prob.variables():
            sol_var[vol.name] = vol.varValue
        # construct the solution dict 
        opt_sol = {}
        for home in self.homes:
            for work in self.works:
                key = 'choice'+'_'+str(home)+'_'+str(work)
                opt_sol[(work, home)] = sol_var[key]
                print (work, home), opt_sol[(work, home)]
        return opt_sol

def main():
    # the data set name
    case_name = '6node'
    # load activity data
    load_activity(case_name)
    # load network data
    load_network(case_name)
    print '\n LOAD DATA'
    
    utils = [
            [10, 20],
            [15, 10]]
    test = TransProblem(elem.home_list, elem.work_list, utils)
    test.solve()
    # print test.utils
    
if __name__ == '__main__':
    import sys
    sys.path.append('/Users/xiongyiliang/Projects/PyMarkovActv/')
    from shared.universe import elem
    from iofile.inputs import load_network, load_activity
    main()
