from . import (Report, np, plot_image, plot_arena, XYCells, nonlinearfit,
    scale_score)
from reprep import MIME_RST
from reprep.plot_utils import y_axis_balanced, x_axis_set
 
__all__ = ['report_intuitive']

def report_intuitive(confid, stats):
    cells = stats['cells']  
    visual_stimulus = stats['visual_stimulus']
    directions = stats['directions']

    r = Report('%s_intuitive' % confid)

    models = []

    forward = np.sign(np.cos(directions)) > 0
    
    models.append({
        'name': 'forward',
        'kernel':forward,
        'desc': 'cos(theta) > 0'
    })

    models.append({
        'name': 'cos',
        'kernel': np.cos(directions),
        'desc': 'cos(theta)'
    })
    

    models.append({
        'name': 'cos_forward',
        'kernel': forward * np.cos(directions),
        'desc': 'max(cos(theta), 0)'
    })

    models.append({
        'name': 'cosP1',
        'kernel': np.cos(directions) + 0.2,
        'desc': 'cos(theta) + 0.2'
    })

    
    for model in models:
        kernel = model['kernel']
        kernel *= (1.0 / np.abs(kernel).max())
    
        feature = cells.zeros()
        for c in cells.iterate():
            optic_flow = visual_stimulus[c.k]['optic_flow']
            feature[c.k] = np.sum(optic_flow * kernel)
    
        model['feature'] = -feature

    ncells = 200
    xy_cells = XYCells(radius=1, ncells=ncells, da_cells=cells)
    da2xy = lambda F:  xy_cells.from_da_field(F.astype('float')) 

    r.text('description',
           'These are some examples of feature fields that can be '
           'expressed as linear combinations of perceived optic flow '
           'times a given kernel. ', MIME_RST)

    Z = stats['feature']['mean']
    Z_order = scale_score(Z) 

    for model in models:
        name = model['name']
        feature = model['feature']
        kernel = model['kernel']
        desc = model['desc']

        feature_order = scale_score(feature)
        
        s = r.node(name)
        f = s.figure('Figure0', cols=3)
        
        with f.plot('kernel', caption='kernel: %s' % desc) as pylab:
            theta = np.rad2deg(directions)
            pylab.plot(theta, kernel)
            y_axis_balanced(pylab, 0.2)
            x_axis_set(pylab, -180, +180)
            pylab.xlabel('directions')
            
        with s.plot('Z_Z2', caption='Feature vs predicted feature') as pylab:
            pylab.plot(feature, Z, '.')
            pylab.xlabel('feature')
            pylab.ylabel('predicted feature')
        s.last().add_to(f)
        
        
        with s.plot('Z_Z2_order',
            caption="order(feature) vs order(predicted feat.)") as pylab:
            pylab.plot(Z_order, feature_order, '.')
            pylab.xlabel('Z')
            pylab.ylabel('Z2')
        s.last().add_to(f)            
        
        plot_image(s, f, 'feature1', cells, feature, use_posneg=True,
                   caption='Feature in axis angle/distance plane')

        plot_arena(s, f, 'feature2', da2xy(feature), use_posneg=True,
                   caption='Feature in reduced coordinates') 

        feature2 = nonlinearfit(feature, Z)
    
        plot_arena(s, f, 'feature2nonlinear', da2xy(feature2), use_posneg=True,
                   caption='Feature in reduced coordinates (nonlinear fit)') 
    
    return r



