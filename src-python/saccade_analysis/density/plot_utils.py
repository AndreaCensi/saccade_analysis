from reprep import posneg, scale 
import itertools

from . import np, contract

@contract(field='array[AxB]')
def plot_image(r, fig, nid, cells, field, caption=None, scale_params={},
               use_posneg=False, scale_format='%.2f'):
    cells.check_compatible_shape(field)
    
    d_edges = cells.d_edges
    a_edges = cells.a_edges
    
    nd = len(d_edges) - 1 
    
    if use_posneg:
        rgb = posneg(field, **scale_params) / 255.0
        colorbar = None
    else:
        properties = {}
        rgb = scale(field, properties=properties, **scale_params) / 255.0
        colorbar = properties['color_bar']
    
    with r.data_pylab(nid) as pl:
        #pl.title(nid if caption is None else caption)
        pl.xlabel('axis angle (deg)')
        pl.ylabel('distance from wall (m)')
        for a, d in itertools.product(range(len(a_edges) - 1),
                                      range(len(d_edges) - 1)):
            a_min = a_edges[a]
            a_max = a_edges[a + 1] 
            d_min = d
            d_max = d + 1
            quatx = [a_min, a_min, a_max, a_max]
            quaty = [d_min, d_max, d_max, d_min] 
            pl.fill(quatx, quaty, color=rgb[d, a, :])
            
        labels_at = [0, 0.15, 0.25, 0.5, 0.75, 1]
        tick_pos = []
        tick_label = []
        for l in labels_at:
            closest = np.argmin(np.abs(d_edges - l))
            tick_pos.append(closest)
            tick_label.append('%.2f' % l)
    #    pl.yticks(tick_pos, tick_label)
       
        bar_w = 15
        bar_x = 180 + 2 * bar_w
        if colorbar is not None:
            f = 3
            ex = [bar_x - bar_w, bar_x + bar_w, f, nd - f]
            pl.imshow(colorbar, origin='lower',
                      extent=ex, aspect='auto')
            pl.fill([ex[0], ex[0], ex[1], ex[1]],
                    [ex[2], ex[3], ex[3], ex[2]], facecolor='none', edgecolor='k')
            vdist = 1.1
            pl.annotate(scale_format % properties['min_value'], (bar_x, f - vdist),
                        horizontalalignment='center')
            pl.annotate(scale_format % properties['max_value'], (bar_x, nd - f + vdist),
                        horizontalalignment='center')
        
        xt = [-180, -135, -90, -45, 0, 45, 90, 135, 180]
        pl.xticks(xt, ['%+d' % x for x in xt])
        pl.yticks(range(len(d_edges)), ['%.2f' % x for x in cells.d_edges])
        #pl.axis((a_edges[0], a_edges[-1], 0, nd))
        pl.axis((-180, bar_x + bar_w * 2, 0, nd))
        
    r.last().add_to(fig, caption=caption)

                

def plot_arena(r, fig, nid, xy_field, caption=None, scale_params={},
               use_posneg=False, scale_format='%.2f'): 
    scale_params['nan_color'] = [1, 1, 1]
    if use_posneg:
        rgb = posneg(xy_field, **scale_params) / 255.0
        colorbar = None
    else:
        properties = {}
        rgb = scale(xy_field, properties=properties, **scale_params) / 255.0
        colorbar = properties['color_bar']
    
    with r.data_pylab(nid) as pl:
        # Plot arena profile
        theta = np.linspace(0, 2 * np.pi, 100)
        pl.plot(np.cos(theta), np.sin(theta), 'k-')
        
        a = np.transpose(rgb, axes=(1, 0, 2))
        a = np.flipud(a) 
        pl.imshow(a, extent=(-1, +1, -1, +1)) 
        pl.xlabel('x (m)')
        pl.ylabel('y (m)')
         
        if colorbar is not None:
            plot_vertical_colorbar(pl, colorbar,
                                   bar_x=1.2, bar_w=0.05,
                                   bar_y_min= -0.5, bar_y_max=0.5,
                                   vdist=0.06,
                                   label_min=scale_format % properties['min_value'],
                                   label_max=scale_format % properties['max_value'])
        pl.axis('equal')
        
    r.last().add_to(fig, caption=caption)
    
    
def plot_vertical_colorbar(pl, colorbar, bar_x, bar_w, bar_y_min, bar_y_max,
                           vdist, label_min, label_max):
    ex = [bar_x - bar_w, bar_x + bar_w, bar_y_min, bar_y_max]
    pl.imshow(colorbar, origin='lower',
              extent=ex, aspect='auto')
    pl.fill([ex[0], ex[0], ex[1], ex[1]],
            [ex[2], ex[3], ex[3], ex[2]], facecolor='none', edgecolor='k')
    pl.annotate(label_min, (bar_x, bar_y_min - vdist),
                horizontalalignment='center')
    pl.annotate(label_max, (bar_x, bar_y_max + vdist),
                horizontalalignment='center') 
