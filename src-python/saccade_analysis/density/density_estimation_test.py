from . import get_distance_edges, contract, np

from numpy.ma.testutils import  assert_almost_equal

def get_distance_edges_test():
    
    n = 10
    R = 2
    distance_edges = get_distance_edges(arena_radius=R, n=n)
    
    assert len(distance_edges) == n + 1
    assert distance_edges[0] == 0
    assert distance_edges[-1] == R
    
    
    def area(R): 
        return np.pi * R * R
    
    @contract(r0='x', r1='>x')
    def area_between(r0, r1):
        return area(r1) - area(r0)
    
    should_be = area(R) / (n)
    #print('Should be %g' % should_be)
    for i in range(n):
        r0 = R - distance_edges[i]
        r1 = R - distance_edges[i + 1]
        strip = area_between(r1, r0)
        #print('Between %5.3f and %5.3f dist %g strip is %g' % (r0,r1,
        #                                                       r1-r0,strip))
        
        assert_almost_equal(strip, should_be)
