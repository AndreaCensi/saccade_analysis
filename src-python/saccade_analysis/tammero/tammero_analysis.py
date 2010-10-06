from optparse import OptionParser
from geometric_saccade_detector.io import saccades_read_h5
import numpy
from geometric_saccade_detector.math_utils import merge_fields, normalize_pi
from reprep import Report
from saccade_analysis.tammero.approach_angle import compute_approach_angle



def main():
    
    parser = OptionParser()
    parser.add_option("--saccades", help="Saccades file (.h5 created by geo_sac_compact)")
    parser.add_option("--output", help="Output directory", default='sequence_analysis_output')

    (options, args) = parser.parse_args()

    if options.saccades is None:
        raise Exception('Please specify data with --saccades')

    saccades = saccades_read_h5(options.saccades)
    saccades = add_position_information(saccades)
    subsets = divide_into_subsets(saccades)
    report = create_report(subsets)
    write_report(report)
    
def divide_into_subsets(saccades):
    close_threshold = 0.65
    subsets = [
     ('all', 'All saccades', lambda x: True),
     ('close_to_center', 'Close to center', lambda x: x['distance_from_center'] < close_threshold),
     ('close_to_wall', 'Close to wall', lambda x: x['distance_from_center'] > close_threshold),
     ]
    
    for id, desc, test in subsets:
        include = map(test, saccades)
        select = saccades[numpy.array(include)]
        print len(select)
        yield id, desc, select
    

def create_report(subsets):
    report = Report('tammero_analysis')
    for id, desc, saccades in subsets:
        node = create_report_subset(id, desc, saccades)
        report.add_child(node)
    return report

def create_report_subset(id, desc, saccades):
    report = Report(id)
    description = '''

Subset: %s

It contains %d saccades.

''' % (desc, len(saccades)) 
 
    saccade_angle = saccades['saccade_angle']
    approach_angle = saccades['approach_angle']
           
    with report.data_pylab('distance_from_center') as pylab:
        distance = saccades['distance_from_center']
        pylab.hist(distance, 100)
        pylab.xlabel('meters')
        pylab.ylabel('number of saccades')
        pylab.title('Distance from center (%s)' % id)
        a = pylab.axis()
        pylab.axis([0, 1, 0, a[3]])
        
    with report.data_pylab('saccade_angle') as pylab:
        pylab.hist(saccade_angle, range(-180, 185, 5))
        pylab.xlabel('degrees')
        pylab.ylabel('number of saccades')
        pylab.title('Saccade angle (%s)' % id)
        a = pylab.axis()
        pylab.axis([-180, 180, 0, a[3]])
    
    with report.data_pylab('approach_angle') as pylab:
        pylab.hist(approach_angle, range(-60, 65, 5))
        pylab.xlabel('degrees')
        pylab.ylabel('number of saccades')
        pylab.title('Approach angle (%s)' % id)
        a = pylab.axis()
        pylab.axis([-60, 60, 0, a[3]])
    
    with report.data_pylab('approach_vs_saccade') as pylab:
        pylab.plot(approach_angle, saccade_angle, '.')
        pylab.xlabel('approach angle (deg)')
        pylab.ylabel('saccade angle (deg)')
        pylab.title('Approach vs saccade angle (%s)' % id)
        a = pylab.axis()
        pylab.axis([-60, 60, -180, 180])
    
    
    # compute probabili
    approach, probability_left = \
        compute_turning_probability(approach_angle=approach_angle,
                                    saccade_angle=saccade_angle)
    
    probability_right = -probability_left + 1
    
    with report.data_pylab('turning_probability') as pylab:
        pylab.plot(approach, probability_left, 'gx-', label='left')
        pylab.plot(approach, probability_right, 'rx-', label='right')
        pylab.xlabel('approach angle (deg)')
        pylab.ylabel('probability of turning')
        pylab.title('Probability of turning (%s)' % id)
        a = pylab.axis()
        pylab.plot([0, 0], [0.2, 0.8], 'k--')
        pylab.axis([-60, 60, 0, 1])
        pylab.legend()
 
    
        
    f = report.figure(shape=(3, 3))
    f.sub('distance_from_center', caption='Distance from center')
    f.sub('saccade_angle', caption='Saccade angle')
    f.sub('approach_angle', caption='Approach angle')
    f.sub('approach_vs_saccade', caption='Approach vs saccade angle')
    f.sub('turning_probability', caption='Probability of turning')
    return report

def compute_turning_probability(approach_angle, saccade_angle):
    spacing = 5
    approach = range(-45, 45 + spacing, spacing)
    probability_left = []
    for a in approach:
        inbin = numpy.logical_and(a - spacing <= approach_angle,
                                   approach_angle <= a + spacing)
        angles = saccade_angle[inbin]
        num_left = (angles > 0).astype('int').sum()
        prob = num_left * 1.0 / len(angles) 
        probability_left.append(prob)
    return approach, numpy.array(probability_left)


def write_report(report):
    report.to_html('tammero_analysis/index.html')

def add_position_information(saccades, arena_center=[0.1, 0.5], arena_radius=1.0):
    info_dtype = [
        ('distance_from_wall', 'float64'),
        ('distance_from_center', 'float64'),
        ('approach_angle', 'float64'), # degrees
        ('saccade_angle', 'float64'), # degrees
    ]
    
    info = numpy.zeros(dtype=info_dtype, shape=(len(saccades),))
    
    for i, saccade in enumerate(saccades):
        x = saccade['x']
        y = saccade['y']
        ax = x - arena_center[0]
        ay = y - arena_center[1]
        
        distance_from_center = numpy.hypot(ax, ay)
        
        distance_from_wall = arena_radius - distance_from_center
        assert distance_from_wall > 0
        
        # XXX temporary fix
        saccade_angle = -saccade['sign'] * saccade['amplitude']
        # NOTE that Tammero's definition is different than ours
        #saccade_angle = 180 - saccade['sign'] * saccade['amplitude']
        #saccade_angle = numpy.degrees(normalize_pi(numpy.radians(saccade_angle)))
        
        theta = numpy.radians(saccade['orientation_start'])
        approach_angle = compute_approach_angle(ax, ay, theta, radius=arena_radius)
        
        info[i]['distance_from_center'] = distance_from_center
        info[i]['distance_from_wall'] = distance_from_wall
        info[i]['saccade_angle'] = saccade_angle
        info[i]['approach_angle'] = numpy.degrees(approach_angle)
        
    return merge_fields(saccades, info)
    
