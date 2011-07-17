 
from reprep import posneg, scale 
import itertools
import numpy as np


def plot_image(r, fig, nid, cells, field, caption=None, scale_params={},
               use_posneg=False, scale_format='%4g'):
    
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
        pl.title(nid if caption is None else caption)
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
            pl.imshow(colorbar,
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
#
#def plot_image_nonscaled(r, f, nid, d_edges, a_edges, field, caption=None, skim=0):
#    
#    rgb = scale(field, skim=skim) / 255.0
#         
#    with r.data_pylab(nid) as pl:
#        pl.title(nid)
#        pl.xlabel('axis angle (deg)')
#        pl.ylabel('distance from wall')
#        for a, d in itertools.product(range(len(a_edges) - 1),
#                                      range(len(d_edges) - 1)):
#            a_min = a_edges[a]
#            a_max = a_edges[a + 1] 
#            d_min = d_edges[d]
#            d_max = d_edges[d + 1]   
#            quatx = [a_min, a_min, a_max, a_max]
#            quaty = [d_min, d_max, d_max, d_min] 
#            pl.fill(quatx, quaty, color=rgb[d, a, :])
#        pl.axis((a_edges[0], a_edges[-1], d_edges[0], d_edges[-1]))
#    r.last().add_to(f, caption=caption)
#   
