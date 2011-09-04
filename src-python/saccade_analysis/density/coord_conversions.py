from contracts import contract, new_contract
from ..tammero.tammero_analysis import compute_axis_angle
import numpy as np

new_contract('angle_pi', 'float,>=-pi,<=pi')

@contract(x='float', y='float', theta='angle_pi', radius='>0,x',
          returns='tuple(angle_pi,(>=0,<=x))')
def axisangle_distance_from_x_y_theta(x, y, theta, radius):
    axis_angle = compute_axis_angle(x, y, theta)
    r = np.hypot(x, y)
    assert r <= radius, 'r=%s radius=%s' % (r, radius)
    distance = radius - r
    return axis_angle, distance
    

@contract(axis_angle='angle_pi', distance='>=0,x',
          assumed_theta='angle_pi', radius='>0,>=x',
          returns='tuple(float, float)')
def x_y_from_axisangle_distance(axis_angle,
                                distance,
                                assumed_theta,
                                radius):
    phi = assumed_theta - axis_angle
    norm = radius - distance
    x = np.cos(phi) * norm
    y = np.sin(phi) * norm
    return x, y
