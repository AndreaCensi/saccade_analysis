import numpy

    
class Markov:
    def __init__(self, transition_matrix):
        assert_stochastic(transition_matrix)
        
        self.P = transition_matrix
        self.pi = stationary_distribution(self.P)
        self.state = sample_discrete_distribution(self.pi)
        
    def sample(self):
        self.pi = numpy.dot(self.P, self.pi)
        assert_distribution(self.pi)
        self.pi = self.pi / self.pi.sum()
        self.state = sample_discrete_distribution(self.pi)
        return self.state
    


def matrix_power(P, k):
    res = numpy.eye(P.shape[0])
    while k > 0:
        res = numpy.dot(res, P)
        k -= 1 
    return res
    
def assert_almost_equal(a, b, threshold=1e-6):
    diff = numpy.linalg.norm(a - b)
    if not diff < threshold:
        assert False, "%s != %s" % (a, b) 
    
def assert_stochastic(P):
    n = P.shape[0]
    assert(P.shape == (n, n))
    assert_almost_equal(P.sum(axis=0), numpy.array([1, 1]))
    PP = numpy.dot(P, P)
    assert_almost_equal(PP.sum(axis=0), numpy.array([1, 1]))
    
def assert_distribution(pi):
    # XXX
    assert_almost_equal(pi.sum(), 1)

    
def stationary_distribution(P):
    pi = numpy.dot(matrix_power(P, 20), numpy.array([0.5, 0.5]))
    assert_distribution(pi)
    return pi
    
def sample_discrete_distribution(pdist):
    assert_distribution(pdist)
    assert pdist.shape[0] == 2 
    if numpy.random.rand() < pdist[0]:
        return 1
    else:
        return 0
