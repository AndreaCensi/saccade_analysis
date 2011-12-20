from . import (Report, np, plot_image, plot_arena, XYCells, nonlinearfit,
    plot_kernel, plot_feature_comparison)
from reprep import MIME_RST
 
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
        'kernel': forward,
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

    for model in models:
        name = model['name']
        feature = model['feature']
        kernel = model['kernel']
        desc = model['desc']
 
        s = r.node(name)
        f = s.figure('Figure0', cols=3)
        
        plot_kernel(s, f, 'kernel', directions, kernel,
                    caption='kernel: %s' % desc)
            
        plot_feature_comparison(s, f, Z, feature)

        plot_image(s, f, 'feature1', cells, feature, colors='posneg',
                   caption='Feature in axis angle/distance plane')

        plot_arena(s, f, 'feature2', da2xy(feature), colors='posneg',
                   caption='Feature in reduced coordinates') 

        feature2 = nonlinearfit(feature, Z)
    
        plot_arena(s, f, 'feature2nonlinear', da2xy(feature2), colors='posneg',
                   caption='Feature in reduced coordinates (nonlinear fit)') 
    
    return r



