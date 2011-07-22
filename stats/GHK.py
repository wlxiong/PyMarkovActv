import scipy.stats
import numpy

def diffMat(J, i):
    IArr = numpy.identity(J, float)
    IArr[:,i] = -1.0
    IMat = numpy.matrix(numpy.delete(IArr, i, 0))
    return IMat

def simulated_choice_prob(Sigma, Utility, i, N):
    J = Sigma.shape[0]
    IMat = diffMat(J, i)
    transformedSigma = IMat * numpy.matrix(Sigma) * IMat.T
    transformedUtility = IMat * Utility.T
    LL = numpy.linalg.cholesky(transformedSigma)
    P = numpy.ones(N)
    for r in xrange(N):
        eta = numpy.zeros(J-1)
        for j in xrange(J-1):
            V = transformedUtility[j]
            cc = numpy.array(LL[j,:]).ravel()
            X = -(V + numpy.dot(eta,cc))/cc[j]
            P[r] *= scipy.stats.norm.cdf(X)
            eta[j] = scipy.stats.truncnorm.rvs(float('-inf'),X)
    return P.mean()

def main():
    covMatrix = numpy.matrix([[1, .2, .6], 
                           [.2, 1, .3], 
                           [.6, .3, 1]])
    Utility = numpy.matrix([[5, 5, 6]])
    PP = numpy.zeros(3)
    for i in xrange(3):
        PP[i] = simulated_choice_prob(covMatrix, Utility, i, 100)
    print PP, PP.sum()

if __name__ == '__main__':
    main()

