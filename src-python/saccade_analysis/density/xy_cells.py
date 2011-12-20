from . import np, contract
from ..tammero.tammero_analysis import compute_axis_angle
from numpy.testing.utils import assert_allclose
import itertools


class XYCells(object):
    
    @contract(radius='>0', ncells='int,>0', assumed_theta='number')
    def __init__(self, radius, ncells, da_cells, assumed_theta=np.pi / 2):
        ''' For computing the axis angle, we assume that the 
            fly is always pointing in a direction. Default is "up".
        '''
        self.radius = radius
        self.ncells = ncells
        shape = (ncells, ncells)
        self.shape = shape 
        self.x = self.zeros()
        self.y = self.zeros()
        self.d = self.zeros()
        self.r = self.zeros()
        self.axis_angle_deg = self.zeros()
        self.assumed_theta = assumed_theta
        
        def interpolate(m, M, i, N):
            return m + (M - m) * float(i) / float(N - 1)
        
        for k in self.iterate_indices():
            self.x[k] = interpolate(-radius, +radius, k[0], shape[0])
            self.y[k] = interpolate(-radius, +radius, k[1], shape[1])
            self.r[k] = np.hypot(self.x[k], self.y[k])
            d = radius - self.r[k]
#            if d < 0: d = np.NAN
            self.d[k] = d
            axis_angle = compute_axis_angle(self.x[k], self.y[k],
                                                    theta=assumed_theta)
            self.axis_angle_deg[k] = np.degrees(axis_angle)

        assert_allclose(interpolate(-radius, +radius, 0, shape[0]),
                        - interpolate(-radius, +radius,
                                      shape[0] - 1, shape[0]))

        self.create_xy_to_cells(da_cells)
        
    def zeros(self, dtype='float'):
        return np.zeros(shape=self.shape, dtype=dtype)
            
    def iterate_indices(self):
        for i, j in itertools.product(range(self.shape[0]),
                                      range(self.shape[1])):
            yield i, j 

    def create_xy_to_cells(self, cells):
        self.xy_to_cells = self.zeros('object')
        self.d_index = self.zeros()
        self.a_index = self.zeros()
        
        self.in_cell = self.zeros('bool')
        
        for k in self.iterate_indices():
            d = self.d[k]
            angle = self.axis_angle_deg[k]
            cell = cells.closest_cell(distance=d, angle_deg=angle)
            if cell is None:
                cell = (0, 0)
                self.in_cell[k] = False
                self.d_index[k] = np.NAN
                self.a_index[k] = np.NAN
            else:
                self.in_cell[k] = True
                self.d_index[k] = cell[0]
                self.a_index[k] = cell[1]
            self.xy_to_cells[k] = cell
            
        self.not_in_cell = np.logical_not(self.in_cell) 
        
    def from_da_field(self, field):
        res = self.zeros(field.dtype)
        for k in self.iterate_indices():
            res[k] = field[self.xy_to_cells[k]]
        res[self.not_in_cell] = np.NAN
        return res
    
    
