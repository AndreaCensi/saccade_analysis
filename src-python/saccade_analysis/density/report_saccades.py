from . import ParamsEstimation, np, Report
from reprep import MIME_PDF
import warnings
from . import plot_circle

def report_saccades(confid, saccades):
    center = ParamsEstimation.arena_center
    radius = ParamsEstimation.arena_radius 
    warnings.warn('Using hardcoded arena size and position (%s, %s)' 
                  % (center, radius))

    r = Report('%s_saccades' % confid)
    f = r.figure()
    print saccades['position'].shape
    x = saccades['position'][:, 0]
    y = saccades['position'][:, 1]

    with f.plot('histogram', mime=MIME_PDF, figsize=(10, 10)) as pylab:
        pylab.plot(x, y, '.', markersize=0.8)
        plot_arena_with_circles(pylab, center=center, radius=radius)
        pylab.plot(center[0], center[1], 'r+', markersize=2)
        pylab.axis('equal')
        pylab.title('Center: %s' % str(center))

    with f.plot('hist_phi', mime=MIME_PDF, figsize=(10, 10)) as pylab:
        
        phi = saccades['axis_angle']
        d = saccades['distance_from_wall']
        pylab.plot(phi, d, '.', markersize=0.8)
        pylab.xlabel('phi')
        pylab.ylabel('d')
        
    return r



def plot_arena_with_circles(pylab, center, radius, col='b-'):
    for r in np.linspace(0.1, radius, 10):
        plot_circle(pylab, center, r, col, linewidth=0.7)      
    plot_circle(pylab, center, radius, 'k-')      
