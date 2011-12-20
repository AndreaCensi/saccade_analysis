from . import x_y_from_axisangle_distance, axisangle_distance_from_x_y_theta, np
from numpy.testing.utils import assert_allclose
import itertools

radius = 1.0


def xytheta_coords():
    yield 0., 0., 0.
    yield 0., 0., np.pi
    yield 0., 0., -np.pi
    yield 0., 0., -np.pi / 2
    yield radius, 0., 0.
    yield 0., radius, 0.
    yield 0., radius / 2, 0.
    yield 0., radius, 0.
    yield radius / 2, radius / 2, 0.
    yield -radius / 2, radius / 2, 0.
    yield radius / 2, radius / 2, np.pi / 2
    yield -radius / 2, radius / 2, np.pi / 2
    
    
def test_conversions_1():
    for x, y, theta in xytheta_coords():
        a, d = axisangle_distance_from_x_y_theta(x, y, theta, radius)
        assert d >= 0
        x2, y2 = x_y_from_axisangle_distance(a, d, theta, radius)
        assert_allclose(x2, x, atol=1e-8)
        assert_allclose(y2, y, atol=1e-8)


def ad_coords():
    distances = [0., 0.01, radius / 2, radius]
    angles = [-np.pi, -np.pi / 4, 0., np.pi / 2, np.pi]
    for a, d in itertools.product(angles, distances):
        yield a, d
        

def test_conversions_2():
    for theta in [0., np.pi, -np.pi, np.pi / 2]:
        for a, d in ad_coords():
            assert d >= 0
            x, y = x_y_from_axisangle_distance(a, d, theta, radius)
            a2, d2 = axisangle_distance_from_x_y_theta(x, y, theta, radius)
            
            msg = 'a:%g d:%g x:%g y:%g th:%g a2:%g d2:%g' % (a, d, x,
                                                             y, theta, a2, d2)
            assert_allclose(d2, d, atol=1e-8, err_msg=msg)
            if d < radius:
                # singularity
                assert_allclose(np.cos(a), np.cos(a2), atol=1e-8, err_msg=msg)
                assert_allclose(np.sin(a), np.sin(a2), atol=1e-8, err_msg=msg)
            
