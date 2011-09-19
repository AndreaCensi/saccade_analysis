from reprep import Report
import numpy as np 
from . import scale_score


def report_visual_stimulus(confid, stats): 

    r = Report('%s_stimulus_fit' % confid)
    f = r.figure(cols=3)
    cells = stats['cells']
    poses = stats['equiv_pose']  
    visual_stimulus = stats['visual_stimulus']
    directions = stats['directions']

    feature = stats['feature']
    
    num_photo = directions.size
    num_cells = visual_stimulus.size
    Y = np.zeros((num_cells, num_photo))
    Z = np.zeros(num_cells)
    i = 0;
    for c in cells.iterate():
        Y[i, :] = visual_stimulus[c.k]['optic_flow']
        Z[i] = feature[c.k]['mean']
        i += 1


    reduce_factor = 8
    directions = directions[::reduce_factor]
    Y = Y[:, ::reduce_factor]
    num_photo = Y.shape[1]

    A_lst, residues, rank, S = np.linalg.lstsq(Y, Z) #@UnusedVariable
    
    print('Detected rank: %s' % rank)
    
    def plot_stats(name, A, desc):
        
        # normalize A such that the norm is 1
        A = A / np.linalg.norm(A)
        
        with f.data_pylab('%s_solution' % name) as pylab:
            plot_field_of_view(pylab, directions, A, marker='x-')
            pylab.plot([-180, 180], [0, 0], 'k-')
            pylab.axis((-180, 180, -1, 1))
        f.last().add_to(f, desc)
        
        Zpred = np.dot(Y, A) 
        with f.data_pylab('%s_Z_Z2' % name) as pylab:
            pylab.plot(Z, Zpred, '.')
            pylab.xlabel('feature')
            pylab.ylabel('predicted feature')
        f.last().add_to(f, 'Feature vs predicted feature')
            
        Z_order = scale_score(Z)
        Zpred_order = scale_score(Zpred)
        with f.data_pylab('%s_Z_Z2_order' % name) as pylab:
            pylab.plot(Z_order, Zpred_order, '.')
            pylab.xlabel('Z')
            pylab.ylabel('Z2')
        f.last().add_to(f, 'order(feature) vs order(predicted feat.)')
            
        
    plot_stats('lst', A_lst, 'Least square solution')
    
    for alpha in [0.001, 0.01, 0.1, 1, 100, 10000]:
        Q = np.dot(Y.T, Y) + alpha * np.eye(num_photo)
        A_reg = np.linalg.solve(Q, np.dot(Y.T, Z))    
        plot_stats('reg-%g' % alpha, A_reg,
                   'Norm regularization, alpha=%g' % alpha) 
    
    B = deriv_matrix_phased(num_photo)
    for alpha in [0.01, 0.1, 10, 1000, 10000, 100000]:
        Q = np.dot(Y.T, Y) + alpha * np.dot(B.T, B)
        A_reg = np.linalg.solve(Q, np.dot(Y.T, Z))    
        plot_stats('regd-%g' % alpha, A_reg,
                   'Derivative norm reg., alpha=%g' % alpha)
    
    C = deriv2_matrix(num_photo)
    for alpha in [0.01, 0.1, 10, 1000, 10000, 100000]:
        Q = np.dot(Y.T, Y) + alpha * np.dot(C.T, C)
        A_reg = np.linalg.solve(Q, np.dot(Y.T, Z))    
        plot_stats('regc-%g' % alpha, A_reg,
                   'Curvature norm reg., alpha=%g' % alpha)
    

    if False:
        with f.data_pylab('coords') as pylab:    
            for c in cells.iterate():
                pose = stats['equiv_pose'][c.k]
                pylab.plot(pose['x'], pose['y'], '.')
        f.last().add_to(f)
    
    for c in cells.iterate():
        if (c.k[0] + c.k[1]) % 10 != 0:
            continue 
        
        if True: continue

        pose = poses[c.k]
        x = pose['x']
        y = pose['y']
        theta = pose['theta']
        distance = visual_stimulus[c.k]['distance']
        retinal_velocities = visual_stimulus[c.k]['retinal_velocities']
        optic_flow = visual_stimulus[c.k]['optic_flow']
        
        with f.data_pylab('c.%d.%d' % c.k) as pylab: 
            xs = []
            ys = []
            for phi, rho in zip(directions, distance):
                x1 = x + np.cos(theta + phi) * rho
                y1 = y + np.sin(theta + phi) * rho
                xs.extend([x, x1, None])
                ys.extend([y, y1, None])
            pylab.plot(xs, ys, 'b-')
            A = 0.15
            pylab.plot([x, x + np.cos(theta) * A],
                       [y, y + np.sin(theta) * A], 'r-', markersize=3); 
            pylab.axis('equal')
        f.last().add_to(f, 'readings')

        with f.data_pylab('c.%d.%d_distance' % c.k):
            plot_field_of_view(pylab, directions, distance, bounds=[0, 2])
            pylab.ylabel('distance (m)')
            
        f.last().add_to(f, 'Distance')
        
        with f.data_pylab('c.%d.%d_rv' % c.k) as pylab:
            plot_field_of_view(pylab, directions,
                               np.degrees(retinal_velocities))
            pylab.ylabel('retinal vel (deg/s)')
        f.last().add_to(f, 'Retinal velocities')
        
        with f.data_pylab('c.%d.%d_of' % c.k) as pylab:
            plot_field_of_view(pylab, directions, optic_flow)
            pylab.ylabel('optic flow')
        f.last().add_to(f, 'Optic flow')
             

        with f.data_pylab('c.%d.%d_distance2' % c.k):
            polar_negative(pylab, directions, distance, 'b-')
        f.last().add_to(f, 'Distance')
        
        with f.data_pylab('c.%d.%d_rv2' % c.k): 
            polar_negative(pylab, directions,
                           np.degrees(retinal_velocities), 'b-')
        f.last().add_to(f, 'Retinal velocities')
        
        with f.data_pylab('c.%d.%d_of2' % c.k):
            polar_negative(pylab, directions, optic_flow, 'b-')
        f.last().add_to(f, 'Optic flow')
            
    return r

def deriv_matrix(n):
    X = np.zeros((n, n))
    for i in range(n):
        X[i, (i + 1) % n] = +1
        X[i, (i - 1) % n] = -1
        
    return X

def deriv_matrix_phased(n):
    X = np.zeros((n, n))
    for i in range(n):
        X[i, i] = +1
        X[i, (i - 1) % n] = -1
        
    return X

def deriv2_matrix(n):
    X = np.eye(n) * 2
    for i in range(n):
        X[i, (i + 1) % n] = -1
        X[i, (i - 1) % n] = -1
        
    return X

def plot_field_of_view(pylab, directions, values, bounds=None, marker='-'):
    ''' Plots a retinal quantity in an intuitive way. '''
    pylab.plot(-np.degrees(directions), values, marker)
    
    if bounds is None:
        axis = pylab.axis()
        bounds = [axis[2], axis[3]]
    
#    pylab.axis((-180, 180, bounds[0], bounds[1]))
                   
    pylab.xticks([-180, -90, 0, +90, 180],
                 ['+180', 'left', 'center', 'right', '-180'])
   
   
def polar_negative(pylab, phi, values, *argv, **args):
    m0 = np.abs(values).max()
    # rescale [
    
    A = 1
    b = 3
    
    x = b + A * (values / m0)
    
    pylab.polar(phi, 0 * values + b, 'k-')
    pylab.polar(phi, 0 * values + b - A, 'k--')
    pylab.polar(phi, 0 * values + b + A, 'k--')
    
    phi2 = phi + np.pi / 2
    pylab.polar(phi2, x, *argv, **args)

    pos = values >= 0
    neg = values <= 0
    xpos = x.copy()
    xpos[neg] = np.nan
    xneg = x.copy()
    xneg[pos] = np.nan
    pylab.polar(phi2, xpos, 'r')
    pylab.polar(phi2, xneg, 'b')
    
    
    #pylab.polar(phi2, x, *argv, **args)
