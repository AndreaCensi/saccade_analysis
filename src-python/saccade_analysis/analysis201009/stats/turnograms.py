
from reprep import Report
from saccade_analysis.analysis201009.stats.utils import iterate_over_samples, \
    attach_description
from saccade_analysis.analysis201009.stats.math_utils import xcorr
import numpy

description = """
These figures show in a compact way the sequence of
left/right saccades. 

Blue=left, Red=right. A white line separates the samples.
One line comprises %{width} saccades.
"""

def group_turnogram(group, configuration, saccades, image_width=250, zoom=8):
    r = Report()
    attach_description(r, description.format(width=image_width))
        
    num_saccades = 0
    num_samples = 0
    signs = []
    for sample, saccades_for_sample in iterate_over_samples(saccades): #@UnusedVariable
        num_samples += 1
        num_saccades += len(saccades_for_sample)
        signs.append(saccades_for_sample['sign'])

    colors = {-1: [0, 0, 255, 255], 1: [255, 0, 0, 255]}
    chunks = []
    
    for i in range(num_samples):
        sign = signs[i]
        num_lines = int(numpy.ceil(len(sign) * 1.0 / image_width))
        num_lines *= 2
        chunk = numpy.ndarray(shape=(num_lines, image_width, 4) , dtype='uint8')
        # white transparent
        chunk[:, :, 0:3] = 255 
        chunk[:, :, 3] = 0
        for k in range(len(sign)):
            x = k % image_width
            y = ((k - x) / image_width) * 2
            chunk[y, x, :] = colors[sign[k]] 
        chunks.append(chunk)
        # add empty chunk
        chunk = numpy.ndarray((2, image_width, 4), dtype='uint8')
        chunk[:, :, 0:3] = 255 
        chunk[:, :, 3] = 0
        chunks.append(chunk)
        
    img = numpy.vstack(chunks)

    img_zoomed = zoom_rgb(img, zoom)

    r.data_rgb('turnogram', img_zoomed)
    return r


def zoom_rgb(a, zoom=2):
    slices = []
    for i in range(a.shape[2]):
        original = numpy.squeeze(a[:, :, i])
        zoomk = numpy.ones((zoom, zoom), dtype='uint8')
        zoomed = numpy.kron(original, zoomk)
        slices.append(zoomed)
    return numpy.dstack(slices)
    
    
    
    
