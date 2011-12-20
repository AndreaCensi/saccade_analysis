from . import (plot_kernel, plot_feature_comparison, XYCells, plot_image,
    plot_arena, scale_score, np, Report)


def report_visual_stimulus(confid, stats): 
    r = Report('%s_stimulus_fit' % confid)
    f = r.figure(cols=3)
    cells = stats['cells']
    poses = stats['equiv_pose']  
    visual_stimulus = stats['visual_stimulus']
    directions = stats['directions']

    feature = stats['feature']

    # XXX: repeated code
    ncells = 200
    xy_cells = XYCells(radius=1, ncells=ncells, da_cells=cells)
    da2xy = lambda F:  xy_cells.from_da_field(F.astype('float')) 


    num_photo = directions.size
    num_cells = visual_stimulus.size
    Y = np.zeros((num_cells, num_photo))
    Z = np.zeros(num_cells)
    i = 0
    for c in cells.iterate():
        Y[i, :] = visual_stimulus[c.k]['optic_flow']
        Z[i] = feature[c.k]['mean']
        i += 1


    reduce_factor = 4
    directions = directions[::reduce_factor]
    Y = Y[:, ::reduce_factor]
    num_photo = Y.shape[1]

    A_lst, residues, rank, S = np.linalg.lstsq(Y, Z) #@UnusedVariable
    
    print('Detected rank: %s' % rank)
    
    def plot_stats(name, A, desc):
        print('plot_stats(%s)' % name)
        # normalize A such that the norm is 1
        A = A / np.linalg.norm(A)
        
        s = r.node(name)
        fi = s.figure(caption=desc, cols=3)

        plot_kernel(s, fi, 'kernel', directions, A, caption=None)
        
        Zpred = np.dot(Y, A) 
        Zpred = Zpred / np.abs(Zpred).max()
        
        plot_feature_comparison(s, fi, Z, Zpred) 


        Zpred_field = cells.zeros()
        for c in cells.iterate():
            optic_flow = visual_stimulus[c.k]['optic_flow']
            Zpred_field[c.k] = np.sum(A * optic_flow[::reduce_factor])
        
        Zpred_field2 = nonlinearfit(Zpred_field, Z)

        plot_image(s, fi, 'feature1', cells, Zpred_field,
               colors='posneg',
                   caption='Feature in axis angle/distance plane')

        plot_arena(s, fi, 'feature2', da2xy(Zpred_field),
               colors='posneg',
                   caption='Feature in reduced coordinates') 

        plot_arena(s, fi, 'feature3', da2xy(Zpred_field2),
               colors='posneg',
                   caption='Feature in reduced coordinates (normalized)') 
        
        
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
    for alpha in [0.01, 0.1, 10, 1000, 10000, 100000]: #, 1000000]:
        Q = np.dot(Y.T, Y) + alpha * np.dot(C.T, C)
        A_reg = np.linalg.solve(Q, np.dot(Y.T, Z))    
        plot_stats('regc-%g' % alpha, A_reg,
                   'Curvature norm reg., alpha=%g' % alpha)
    

    if False:
        with f.plot('coords') as pylab:    
            for c in cells.iterate():
                pose = stats['equiv_pose'][c.k]
                pylab.plot(pose['x'], pose['y'], '.')
        f.last().add_to(f)
    
    for c in cells.iterate():
        if (c.k[0] + c.k[1]) % 10 != 0:
            continue 
        
        if True: continue # XXX

        pose = poses[c.k]
        x = pose['x']
        y = pose['y']
        theta = pose['theta']
        distance = visual_stimulus[c.k]['distance']
        retinal_velocities = visual_stimulus[c.k]['retinal_velocities']
        optic_flow = visual_stimulus[c.k]['optic_flow']
        
        with f.plot('c.%d.%d' % c.k, 'readings') as pylab: 
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

        with f.plot('c.%d.%d_distance' % c.k, caption='distance'):
            plot_field_of_view(pylab, directions, distance, bounds=[0, 2])
            pylab.ylabel('distance (m)')
            

        with f.plot('c.%d.%d_rv' % c.k, caption='Retinal velocities') as pylab:
            plot_field_of_view(pylab, directions,
                               np.degrees(retinal_velocities))
            pylab.ylabel('retinal vel (deg/s)')
        
        with f.plot('c.%d.%d_of' % c.k, caption='Opti flow') as pylab:
            plot_field_of_view(pylab, directions, optic_flow)
            pylab.ylabel('optic flow')
    

        with f.plot('c.%d.%d_distance2' % c.k, caption='Distance'):
            polar_negative(pylab, directions, distance, 'b-')

        
        with f.plot('c.%d.%d_rv2' % c.k, caption='Retinal velocities'): 
            polar_negative(pylab, directions,
                           np.degrees(retinal_velocities), 'b-')
        
        with f.plot('c.%d.%d_of2' % c.k, caption='Optic flow'):
            polar_negative(pylab, directions, optic_flow, 'b-')
        
            
    return r


def nonlinearfit(x, Z):
    assert x.size == Z.size
    x_order = scale_score(x).astype('int') 
    Z_sorted = np.sort(Z.flat)
    x2 = Z_sorted[x_order]
    return x2
    

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
