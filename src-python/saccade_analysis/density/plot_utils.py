from . import scale_score_norm, ParamsEstimation, PlotParams, np, contract
from numpy.core.numeric import allclose
from reprep import filter_colormap, posneg, scale
from reprep.plot_utils import plot_horizontal_line, set_spines_look_A
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
        # left bottom width height
#        L = 0.6
#        axes2 = pl.axes([L, 0.0, 1 - L, 0.1])
#        for loc, spine in axes2.spines.iteritems():
#            spine.set_color('none') # don't draw spi
##        pl.xticks([], [])
##        pl.yticks([], [])                
#        #pl.sca(ax)
#
#        pl.axes([0, 0, L - 0.2, 1])

        #ax = pl.gca()  
        
        set_spines_look_A(pl, PlotParams.spines_outward)

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

        def putcolorbar():   
            if colorbar is not None:
                f = 3
                plot_vertical_colorbar(pl, colorbar,
                                       bar_x=bar_x, bar_w=bar_w,
                                       bar_y_min=f, bar_y_max=nd - f,
                                       vdist=0.40,
                                       min_value=properties['min_value'],
                                       max_value=properties['max_value'],
                                       scale_format=scale_format)
        
        if True:
            putcolorbar()
            pl.axis((-180, bar_x + bar_w * 4, 0, nd))
           
#            ex = [180, bar_x + bar_w * 4, 0.4, 0.5]
#            pl.fill([ex[0], ex[0], ex[1], ex[1]],
#                        [ex[2], ex[3], ex[3], ex[2]], facecolor='w', 
#                        edgecolor='none')
        else:
            pl.axis((-180, 180, 0, nd))
            putcolorbar()
#            pl.gca().set_position([0, 0, L - 0.2, 1])

#        
#        else:
#            pl.axis((-180, 180, 0, nd))
#            L = 0.8
#            pl.gca().set_position([0.125, 0.1, L, 0.9])
#
#            ax = pl.gca()
#            
#            # left bottom width height
#            axes2 = pl.axes([L, 0.0, 1 - L, 1])
#            for loc, spine in axes2.spines.iteritems():
#                spine.set_color('none') # don't draw spi
#            pl.xticks([], [])
#            pl.yticks([], [])                
# 
#            putcolorbar()
#
#            
#            pl.sca(ax)
        
        pl.xticks([-180, -135, -90, -45, 0, 45, +90, 135, 180],
                  add_deg(["-180", "", "-90", "", "0",
                           "", "+90", "", "180"])) 
                
        # pl.xlabel('axis angle \\ $\\varphi$ (deg)')
        pl.xlabel('axis angle $\\varphi$')
        pl.ylabel('distance from wall $d$ (m)')
        #pl.gca().xaxis.set_label_coords(0.38, -0.02)
        #pl.gca().yaxis.set_label_coords(-0.17, 0.5)
        
    if r != fig:
        r.last().add_to(fig)


def add_deg(labels):
    m = []
    for a in labels:
        if len(a) > 1: 
            # "0" -> "0"
            a = '%s$^\\circ$' % a        
        m.append(a)
    return m


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
        
        if False:
            pl.xlabel('$x^a$ (m)')
            pl.ylabel('$y^a$ (m)')
            pl.gca().yaxis.set_label_coords(0, 0.5)
            pl.gca().xaxis.set_label_coords(0.5, -0.02)
    
            xt = [-1, +1]
            pl.xticks(xt, ['%+.1f' % x for x in xt])
            pl.yticks(xt, ['%+.1f' % x for x in xt])
        else:                        
            pl.box('off')
            pl.xticks([], [])
            pl.yticks([], [])
                  
        # Plot arena profile
        plot_circle(pl, [0, 0], arena_radius, 'k-')

        plot_circle(pl, [0, 0],
                    arena_radius - ParamsEstimation.min_distance, 'k--',
                    linewidth=0.5)

        if colorbar is not None:
            plot_vertical_colorbar(pl, colorbar,
                                   bar_x=1.2, bar_w=0.05,
                                   bar_y_min=(-0.5), bar_y_max=0.5,
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
            
        if allclose(max_value, +1) and allclose(min_value, -1):
            scale_format = '%+d'
        
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
         
    x = pl.imshow(colorbar, origin='lower',
              extent=ex, aspect='auto',
              interpolation='nearest')
    
    x.set_clip_on(False)
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
    
    with r.plot(name, caption=caption,
                figsize=PlotParams.figsize_kernel) as pylab:
        set_spines_look_A(pylab, PlotParams.spines_outward)
        theta = np.rad2deg(directions)
        
        for i in [-1, 0, 1]:
            plot_horizontal_line(pylab, i, 'k--', linewidth=0.6)

        l = pylab.plot(theta, kernel, 'g-', linewidth=1)
        l[0].set_clip_on(False)
        
        pylab.axis([-180, 180, -1, +1])

        #pylab.xlabel('directions')
        
        #pylab.ylabel('kernel')
        xt = [-180, -90, 0, +90, 180]
        pylab.xticks(xt,
                     add_deg(['-180', '', '0', '', '+180']))
#                             add_deg(['-180', '-90', '0', '+90', '+180']))
                     
        xt = [-1, -0.5, 0, 0.5, +1]
        xtt = ['-1.0', "-0.5", "0", "0.5", '+1.0']
        pylab.yticks(xt, xtt)

        #pylab.gca().yaxis.set_label_coords(-0.05, 0.5)
        #pylab.gca().xaxis.set_label_coords(0.5, -0.05)
        
    r.last().add_to(f)
    
    
def plot_feature_comparison(r, f, Z, Zpred):
    def normalize(x):
        return x / np.abs(x).max()
    Z = normalize(Z)
    Zpred = normalize(Zpred)

    Z_order = scale_score_norm(Z) 
    Zpred_order = scale_score_norm(Zpred)

    #print Zpred_order[Z_order == 0]
    if Zpred_order[Z_order == 0] > 0.5:
        Zpred = -Zpred  
        Zpred_order = scale_score_norm(Zpred)
    #print Zpred_order[Z_order == 0]
    
    M = 1

    def lab(pylab):    
        pass
        if False:
            pylab.ylabel('predicted $\\hat{z}$')
            pylab.xlabel('observed $z$')

    def ticks(cord):
        l = ['-1', '', '0', '', '+1']
        pylab.xticks(cord, l)
        pylab.yticks(cord, l)

    with r.plot('Z_Z2', figsize=PlotParams.figsize_order,
                caption='Feature vs predicted feature') as pylab:
        set_spines_look_A(pylab, PlotParams.spines_outward)
        pylab.plot(Z, Zpred, 'ks', markersize=0.6) 
        pylab.axis([-M, M, -M, M])
        ticks([-1, -0.5, 0, 0.5, 1])
        
        lab(pylab)
        
    r.last().add_to(f)
         
    with r.plot('Z_Z2_order', figsize=PlotParams.figsize_order,
        caption="order(feature) vs order(predicted feat.)") as pylab:
        pylab.plot(Z_order, Zpred_order, 'ks', markersize=0.6)
        lab(pylab)
        set_spines_look_A(pylab, PlotParams.spines_outward)
        pylab.axis([0, 1, 0, 1])
        ticks([0, 0.25, 0.5, 0.75, 1])        
        lab(pylab)
        
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

