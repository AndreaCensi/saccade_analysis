import numpy
from geometric_saccade_detector.math_utils import normalize_pi

def compute_approach_angle(x, y, theta, radius=1):
    
    #  || x + cos(theta) t, y + sin(theta) t ||= 1
    
    # leads to
    
    #  t^2  + (2 x cos(theta) + 2 y sin(theta)]  + (x^2 + y^2 - radius^2) = 0
    
    poly = [1,
            2 * x * numpy.cos(theta) + 2 * y * numpy.sin(theta),
            x ** 2 + y ** 2 - radius ** 2]
    
    # check we are inside
    assert poly[2] < 0
    
    roots = numpy.roots(poly)
    
    # get the positive solution
    t = max(roots)
    
    assert t > 0
    
    px = x + t * numpy.cos(theta)
    py = y + t * numpy.sin(theta)
    
    # check (just in case)
    numpy.testing.assert_almost_equal(px ** 2 + py ** 2, radius ** 2)
    
    phi = numpy.arctan2(py, px)
    
    approach_angle = normalize_pi(phi - theta)
    
    return approach_angle


if __name__ == '__main__':
    
    almost = numpy.testing.assert_almost_equal
    pi = numpy.pi
    
    almost(0, compute_approach_angle(0, 0, 0))
    almost(0, compute_approach_angle(0, 0, 42))
    almost(0, compute_approach_angle(0, 0, pi))
    almost(0, compute_approach_angle(0, 0, -pi))
    almost(0, compute_approach_angle(0.5, 0, 0))
    almost(0, compute_approach_angle(0, 0.5, pi / 2))
    
    assert compute_approach_angle(0, 0.2, 0) > 0
    assert compute_approach_angle(0, -0.2, 0) < 0
     
    
    
    
    
    


