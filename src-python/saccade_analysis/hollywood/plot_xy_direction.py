import numpy
from optparse import OptionParser
from matplotlib import pylab
from geometric_saccade_detector.compact_data import h5_read_saccades

def plot_saccades_xy_directions(saccades, pylab, figure):
    for saccade in saccades:    
        x = saccade['x']
        y = saccade['y']
        theta1 = numpy.radians(saccade['orientation_start'])
        theta2 = numpy.radians(saccade['orientation_stop'])
    
        L = 0.01
        x1 = x - numpy.cos(theta1) * L
        y1 = y - numpy.sin(theta1) * L
        
        x2 = x + numpy.cos(theta2) * L
        y2 = y + numpy.sin(theta2) * L
        
        pylab.plot([x1, x], [y1, y], 'r-', linewidth=0.1)
        pylab.plot([x2, x], [y2, y], 'g-', linewidth=0.1)

    pylab.axis('equal')
    pylab.axis('off') 

def main():
    parser = OptionParser()
    parser.add_option("--output", help="Output filename")
    (options, args) = parser.parse_args()
    
    filename = args[0]
    saccades = h5_read_saccades(filename) 
    
    #saccades = saccades[0:100]
    figure = pylab.figure(figsize=(8, 8))
    plot_saccades_xy_directions(saccades, pylab, figure)
    pylab.savefig(options.output)
    
    
if __name__ == '__main__':
    main()
