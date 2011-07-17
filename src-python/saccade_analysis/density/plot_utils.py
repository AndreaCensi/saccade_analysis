 
from reprep import posneg, scale 
import itertools
import numpy as np


def plot_image(r, f, nid, d_edges, a_edges, field, caption=None, scale_params={},
               use_posneg=False):
    
    if use_posneg:
        rgb = posneg(field, **scale_params) / 255.0
    else:
        rgb = scale(field, **scale_params) / 255.0
         
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
        pl.yticks(tick_pos, tick_label)
        pl.axis((a_edges[0], a_edges[-1], tick_pos[1], len(d_edges) - 1))
    r.last().add_to(f, caption=caption)
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
