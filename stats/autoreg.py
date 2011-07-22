import scipy.integrate as integrate
from scipy.stats import norm
import numpy as np
import math

def calc_state_grid(N, mean, stddev):
    frac = np.linspace(0.0, 1.0, N+1)
    print frac
    ends = norm.ppf(frac, mean, stddev)
    probs = norm.pdf( (ends-mean)/stddev)
    grids = mean - np.diff(probs)*stddev*N
    return ends, grids

def grid_transition_dens(x, lower, upper, mean, stddev, autocorr):
    expn_part = norm.pdf(x, mean, stddev)
    prob_part = norm.cdf( (upper - mean*(1.0-autocorr) - autocorr*x) / stddev) - \
                norm.cdf( (lower - mean*(1.0-autocorr) - autocorr*x) / stddev)
    return expn_part * prob_part

def calc_grid_transition_prob(N, ends, mean, stddev, autocorr):
    transition_prob = {}
    for i in xrange(N):
        transition_prob[i] = {}
        for j in xrange(N):
            density_fun = lambda x: grid_transition_dens(x, ends[j], ends[j+1], mean, stddev, autocorr)
            transition_prob[i][j] = integrate.quad(density_fun, ends[i], ends[i+1])[0] * N
    return transition_prob

def main():
    N = 3
    autocorr = 0.5
    mean = 0.0
    stddev = 1.0/math.sqrt(1-autocorr*autocorr)
    ends, grids = calc_state_grid(N, mean, stddev)
    transition_prob = calc_grid_transition_prob(N, ends, mean, stddev, autocorr)
    print 'grids', grids
    print ' ends', ends
    print 'probs', norm.cdf( (ends-mean)/stddev)
    for i in xrange(N):
        for j in xrange(N):
            print transition_prob[i][j],
        print 

if __name__ == '__main__':
    main()

