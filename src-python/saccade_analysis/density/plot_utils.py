from . import (scale_score_norm, ParamsEstimation, PlotParams, np, contract)
from reprep import filter_colormap, posneg, scale
from reprep.plot_utils import (y_axis_balanced, x_axis_set,
    plot_horizontal_line)
import itertools
import warnings


@contract(field='array[AxB]')
def plot_image(r, fig, nid, cells, field, caption=None, scale_params={},
               colors='scale',
               scale_format=None):
    print('plot_image(%s)' % nid)

    assert colors in ['scale', 'posneg', 'cmap']
    
    cells.check_compatible_shape(field)
    
    d_edges = cells.d_edges
    a_edges = cells.a_edges
    
    nd = len(d_edges) - 1 
    
    properties = get_rgb(field, colors, **scale_params)
    colorbar = properties['color_bar']
    rgb = properties['rgb']    
    
    figparams = dict(figsize=PlotParams.figsize)
    
    with r.plot(nid, caption=caption, **figparams) as pl:

        for a, d in itertools.product(range(len(a_edges) - 1),
                                      range(len(d_edges) - 1)):
            a_min = a_edges[a]
            a_max = a_edges[a + 1] 
            d_min = d
            d_max = d + 1
            quatx = [a_min, a_min, a_max, a_max]
            quaty = [d_min, d_max, d_max, d_min] 
            pl.fill(quatx, quaty, color=rgb[d, a, :])
            
        labels_at = [0.16, 0.20, 0.30, 0.40, 0.5, 0.6, 0.70, 1]
        tick_pos = []
        tick_label = []
        for l in labels_at:
            closest = np.argmin(np.abs(d_edges - l))
            tick_pos.append(closest)
            tick_label.append('%.2f' % l)
        pl.yticks(tick_pos, tick_label)
       
        bar_w = 15
        bar_x = 180 + 3 * bar_w
        pl.axis((-180, bar_x + bar_w * 4, 0, nd))

        if colorbar is not None:
            f = 3
            plot_vertical_colorbar(pl, colorbar,
                                   bar_x=bar_x, bar_w=bar_w,
                                   bar_y_min=f, bar_y_max=nd - f,
                                   vdist=0.40,
                                   min_value=properties['min_value'],
                                   max_value=properties['max_value'],
                                   scale_format=scale_format)
        pl.axis((-180, bar_x + bar_w * 4, 0, nd))
       

        pl.xticks([-180, -135, -90, -45, 0, 45, +90, 135, 180],
                    ["-180", "", "-90", "", "", "", "+90", "", "180"]) 
        
        
        # pl.xlabel('axis angle \\ $\\varphi$ (deg)')
        pl.xlabel('$\\varphi$ (deg)')
        pl.ylabel('distance from wall $d$ (m)')
        pl.gca().xaxis.set_label_coords(0.38, -0.02)
        pl.gca().yaxis.set_label_coords(-0.17, 0.5)

        
    if r != fig:
        r.last().add_to(fig)


def plot_arena(r, fig, nid, xy_field, caption=None, scale_params={},
               colors='scale', scale_format=None):
    print('plot_arena(%s)' % nid)
    arena_radius = ParamsEstimation.arena_radius
    warnings.warn('Using hardcoded arena radius %s.' % arena_radius)
    
    scale_params['nan_color'] = [1, 1, 1]
    
    properties = get_rgb(xy_field, colors, **scale_params)
    colorbar = properties['color_bar']
    rgb = properties['rgb']
    
    figparams = dict(figsize=PlotParams.figsize)
    with r.plot(nid, caption=caption, **figparams) as pl:
        
        a = np.transpose(rgb, axes=(1, 0, 2))
        a = np.flipud(a) 
        dx1 = -0.03
        dx2 = 0.03
        dy = 0
        dy1 = -0.04 
        pl.imshow(a, extent=(-1 + dx1, +1 + dx2, -1 + dy1, +1 + dy)) 
        pl.xlabel('$x^a$ (m)')
        pl.ylabel('$y^a$ (m)')
        pl.gca().yaxis.set_label_coords(0, 0.5)
        pl.gca().xaxis.set_label_coords(0.5, -0.02)

        xt = [-1, +1]
        pl.xticks(xt, ['%+.1f' % x for x in xt])
        pl.yticks(xt, ['%+.1f' % x for x in xt])
      
        # Plot arena profile
        plot_circle(pl, [0, 0], arena_radius, 'k-')

        plot_circle(pl, [0, 0],
                    arena_radius - ParamsEstimation.min_distance, 'k--',
                    linewidth=0.5)

        if colorbar is not None:
            plot_vertical_colorbar(pl, colorbar,
                                   bar_x=1.2, bar_w=0.05,
                                   bar_y_min= -0.5, bar_y_max=0.5,
                                   vdist=0.06,
                                   min_value=properties['min_value'],
                                   max_value=properties['max_value'],
                                   scale_format=scale_format)
        pl.axis('equal')
        
    if fig != r:
        r.last().add_to(fig)
    
    
def plot_vertical_colorbar(pl, colorbar, bar_x, bar_w, bar_y_min, bar_y_max,
                           vdist, min_value, max_value, scale_format=None):
    
    if scale_format is None:
        if isinstance(max_value, int):
            scale_format = '%d'
        else:
            scale_format = '%.2f'
        
    label_min = scale_format % min_value
    if min_value == 0:
        label_min = '0'
    label_max = scale_format % max_value
                                   
    ex = [bar_x - bar_w, bar_x + bar_w, bar_y_min, bar_y_max]

    border = colorbar.shape[1] / 10
    print('using border %d for %s' % (border, colorbar.shape))
    for b in range(border):
        colorbar[0 + b, :, 0:3] = 0
        colorbar[-1 - b, :, 0:3] = 0
        colorbar[:, 0 + b, 0:3] = 0
        colorbar[:, -1 - b, 0:3] = 0
         
    pl.imshow(colorbar, origin='lower',
              extent=ex, aspect='auto')
#    pl.fill([ex[0], ex[0], ex[1], ex[1]],
#            [ex[2], ex[3], ex[3], ex[2]], facecolor='none', edgecolor='k')


    pl.annotate(label_min, (bar_x, bar_y_min - vdist),
                horizontalalignment='center', verticalalignment='top')
    pl.annotate(label_max, (bar_x, bar_y_max + vdist),
                horizontalalignment='center', verticalalignment='bottom') 


@contract(kernel='array[K]')
def plot_kernel(r, f, name, directions, kernel, caption=None):
    
    middle = kernel[kernel.shape[0] / 2]
    if middle < 0:
        kernel *= -1
        
    kernel = kernel / np.abs(kernel).max()
    
    with r.plot(name, caption=caption, figsize=PlotParams.figsize) as pylab:
        theta = np.rad2deg(directions)
        pylab.plot(theta, kernel)
        y_axis_balanced(pylab, 0.2)        
        x_axis_set(pylab, -180, +180)
        plot_horizontal_line(pylab, -1, 'k--')
        plot_horizontal_line(pylab, +1, 'k--')
        pylab.xlabel('directions')
        pylab.ylabel('kernel')
        xt = [-180, -90, +90, 180]
        pylab.xticks(xt, ['%d' % x for x in xt])
        xt = [-1, -0.5, 0, 0.5, +1]
        xtt = ['-1.0', "", "", "", '+1.0']
        pylab.yticks(xt, xtt)

        pylab.gca().yaxis.set_label_coords(-0.05, 0.5)
        pylab.gca().xaxis.set_label_coords(0.5, -0.05)
        
    r.last().add_to(f)
    
def plot_feature_comparison(r, f, Z, Zpred):
    def normalize(x):
        return x / np.abs(x).max()
    Z = normalize(Z)
    Zpred = normalize(Zpred)

    Z_order = scale_score_norm(Z) 
    Zpred_order = scale_score_norm(Zpred)

    
    print Zpred_order[Z_order == 0]
    if Zpred_order[Z_order == 0] > 0.5:
        Zpred = -Zpred  
        Zpred_order = scale_score_norm(Zpred)
    print Zpred_order[Z_order == 0]
    
    M = 1.1
    
    h = PlotParams.figsize[1]
    figsize = (h, h)
    with r.plot('Z_Z2', figsize=figsize,
                caption='Feature vs predicted feature') as pylab:
        pylab.plot(Z, Zpred, 'b.', markersize=0.7) 
        pylab.ylabel('predicted $\\hat{z}$')
        pylab.xlabel('observed $z$')
        pylab.xticks([-1, 1], ['-1', '-1'])
        pylab.yticks([-1, 1], ['-1', '+1'])
        pylab.axis([-M, M, -M, M])
        pylab.gca().yaxis.set_label_coords(0, 0.5)
        pylab.gca().xaxis.set_label_coords(0.5, -0.02)

        
    r.last().add_to(f)
        
    
#    with r.plot('Z_Z2_order', figsize=figsize,
#        caption="order(feature) vs order(predicted feat.)") as pylab:
#        pylab.plot(Z_order, Zpred_order, 'b.', markersize=0.6)
#        pylab.ylabel('predicted $\\mathsf{order}(\\hat{z})$')
#        pylab.xlabel('observed $\\mathsf{order}(z)$')
#        pylab.xticks([0, 1], ['0', '$K-1$'])
#        pylab.yticks([0, 1], ['0', '$K-1$'])
#        pylab.axis([-0.1, 1.1, -0.1, 1.1])
#    r.last().add_to(f)

    with r.plot('Z_Z2_order', figsize=figsize,
        caption="order(feature) vs order(predicted feat.)") as pylab:
        pylab.plot(Z_order, Zpred_order, 'b.', markersize=0.7)
        pylab.ylabel('predicted $\\hat{z}$')
        pylab.xlabel('observed $z$') 
        pylab.xticks([0, 1], ['-1', '-1'])
        pylab.yticks([0, 1], ['-1', '+1'])
        pylab.axis([-0.1, 1.1, -0.1, 1.1])
        
        pylab.gca().yaxis.set_label_coords(0, 0.5)
        pylab.gca().xaxis.set_label_coords(0.5, -0.02)
        


    r.last().add_to(f)
        

def get_rgb(field, colors, **kwargs):
    ''' Returns a dict with values 'rgb' (rgb in [0,1]), 'colorbar', etc.. '''
    properties = {}
    if colors == 'posneg':
        rgb = posneg(field, properties=properties, **kwargs) / 255.0
    elif colors == 'scale':
        rgb = scale(field, properties=properties, **kwargs) / 255.0
    elif colors == 'cmap':
        rgb = filter_colormap(field,
                              properties=properties, **kwargs) / 255.0
    else:
        raise ValueError('No known colors %r. ' % colors)
    
    properties['rgb'] = rgb
    return properties


@contract(center='seq[2](number)', radius='>0')
def plot_circle(pylab, center, radius, *args, **kwargs):
    theta = np.linspace(0, 2 * np.pi, 200)
    pylab.plot(radius * np.cos(theta) + center[0],
               radius * np.sin(theta) + center[1], *args, **kwargs)

