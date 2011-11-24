from saccade_analysis.density.da_cells import DACell
from . import np

def test_180deg():
    
    cell_0_10 = DACell(a=0, d=0, a_min=0, a_max=10, d_min=0, d_max=1)
    
    inside = [0, 5, 10]
    outside = [15, -5]
    
    for theta in inside:
        a = theta 
        assert cell_0_10.inside(axis_angle=np.array([a]),
                                distance=np.array([0.5]))
    
    for theta in outside:
        a = theta 
        assert not cell_0_10.inside(axis_angle=np.array([a]),
                                    distance=np.array([0.5]))
    
    
    inside = [180, -175, -170, -180]
    outside = [175, -165]
    
    cell_180_190 = DACell(a=0, d=0, a_min=180, a_max=190, d_min=0, d_max=1)
   
    for theta in inside:
        a = theta 
        assert cell_180_190.inside(axis_angle=np.array([a]),
                                   distance=np.array([0.5]))
    for theta in outside:
        a = theta 
        assert not cell_180_190.inside(axis_angle=np.array([a]),
                                       distance=np.array([0.5]))
   
