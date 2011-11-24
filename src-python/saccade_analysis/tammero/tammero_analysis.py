import numpy as np, os
from optparse import OptionParser

from reprep import Report

# XXX: remove dep
from geometric_saccade_detector.io import saccades_read_h5, saccades_write_all
from geometric_saccade_detector.math_utils import merge_fields, normalize_pi

from .approach_angle import compute_approach_angle
from contracts import contract
from contracts.main import new_contract


def main():
    
    parser = OptionParser()
    parser.add_option("--saccades",
                      help="Saccades file (.h5 created by geo_sac_compact)")
    parser.add_option("--output", help="Output directory",
                      default='tammero_analysis')

    (options, args) = parser.parse_args() #@UnusedVariable

    if options.saccades is None:
        raise Exception('Please specify data with --saccades')

    saccades = saccades_read_h5(options.saccades)
    saccades = add_position_information(saccades)
    subsets = list(divide_into_subsets(saccades))
    
    report = create_report(subsets)
    write_report(report, options.output)
    
    if False:
        print "Writing on files"
        for id, desc, sub_saccades in subsets: #@UnusedVariable
            basename = os.path.join(options.output, 'saccades-%s' % id)
            saccades_write_all(basename=basename, saccades=sub_saccades)
        
    
def divide_into_subsets(saccades):
#    close_threshold = 0.65
    close_threshold = 0.5
    subsets = [
               ('all', 'All saccades', lambda x: True), #@UnusedVariable
               ('close_to_center', 'Close to center',
                lambda x: x['distance_from_center'] < close_threshold),
               ('close_to_wall', 'Close to wall',
                lambda x: x['distance_from_center'] > close_threshold),
    ]
    
    for id, desc, test in subsets:
        include = map(test, saccades)
        select = saccades[np.array(include)]
        print desc, len(select)
        yield id, desc, select
    

def create_report(subsets):
    report = Report('tammero_analysis')
    for id, desc, saccades in subsets:
        # XXX temporary
        report.add_child(create_report_subset(id, desc, saccades))
        report.add_child(create_report_randomness(id, desc, saccades))
    return report

def create_report_subset(id, desc, saccades):
    report = Report('subset_' + id)
    report.text('description', '''

Subset: %s

It contains %d saccades.

''' % (desc, len(saccades)))
 
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
 
    bin_size = 10
    saccade_bin_centers = np.array(range(-180, 185, bin_size))
    n = len(saccade_bin_centers)
    saccade_bins = np.zeros(shape=(n + 1))
    saccade_bins[0:n] = saccade_bin_centers - bin_size
    saccade_bins[n] = saccade_bin_centers[-1]
    
    bin_centers = np.array(range(-50, 55, 10))
    bin_size = 15
    distributions = []
    for angle in bin_centers:
        indices, = np.nonzero(
                    np.logical_and(
                        approach_angle > angle - bin_size,
                        approach_angle < angle + bin_size
                    ))
        x = saccade_angle[indices]
        hist, edges = np.histogram(x, bins=saccade_bins, normed=True) #@UnusedVariable

        distributions.append(hist)
 
    with report.data_pylab('distribution_vs_approach2') as pylab:
        for k in range(len(bin_centers)):
            label = '%d' % bin_centers[k]
            pylab.plot(saccade_bin_centers, distributions[k], '-', label=label)
        #a = pylab.axis()
         
        pylab.legend()
        pylab.xlabel('saccade angle')
        pylab.ylabel('density')
 
    with report.data_pylab('distribution_vs_approach', figsize=(8, 20)) as pylab:
        # get the maximum density
        # max_density = max(map(max, distributions))
        num_plots = len(bin_centers)
        for k in range(num_plots):
            rect = [0.1, k * 1.0 / num_plots, 0.8, 1.0 / num_plots]
            pylab.axes(rect)
            label = '%d' % bin_centers[k]
            pylab.plot(saccade_bin_centers, distributions[k], '-', label=label)
            # pylab.axis([-180, 180, 0, max_density])
        #a = pylab.axis()
            pylab.legend()
        pylab.xlabel('saccade angle')
        pylab.ylabel('density') 
        
    
    f = report.figure(shape=(3, 3))
    f.sub('distance_from_center', caption='Distance from center')
    f.sub('saccade_angle', caption='Saccade angle')
    f.sub('approach_angle', caption='Approach angle')
    f.sub('approach_vs_saccade', caption='Approach vs saccade angle')
    f.sub('turning_probability', caption='Probability of turning')
    f.sub('distribution_vs_approach', caption='Saccade distribution vs approach angle')
    
    return report
    
def create_report_randomness(id, desc, saccades): #@UnusedVariable
    report = Report(id)

    axis_angle = saccades['axis_angle']
    approach_angle = saccades['approach_angle']
    distance_from_wall = saccades['distance_from_wall']


    # additional analysis
    with report.data_pylab('axisangle_vs_distance') as pylab:
        pylab.plot(axis_angle, distance_from_wall, '.', markersize=1)
        pylab.xlabel('axis angle (deg)')
        pylab.ylabel('distance from wall  (m)')
        pylab.title('axis angle vs distance  (%s)' % id)
        pylab.axis([-180, 180, 0, 1])
    
    right = saccades['sign'] < 0
    left = saccades['sign'] > 0
    
    ms = 2
    
    with report.data_pylab('axisangle_vs_distance_lr') as pylab:
        pylab.plot(axis_angle[right], distance_from_wall[right], 'r.', markersize=ms)
        pylab.plot(axis_angle[left], distance_from_wall[left], 'b.', markersize=ms)
        pylab.xlabel('axis angle (deg)')
        pylab.ylabel('distance from wall  (m)')
        pylab.title('left and right saccades  (%s)' % id)
        pylab.axis([-180, 180, 0, 1])
  
    with report.data_pylab('axisangle_vs_distance_l') as pylab:
        # 
        pylab.plot(axis_angle[left], distance_from_wall[left], 'b.', markersize=ms)
        pylab.xlabel('axis angle (deg)')
        pylab.ylabel('distance from wall  (m)')
        pylab.title('only left saccades  (%s)' % id)
        pylab.axis([-180, 180, 0, 1])
        
    with report.data_pylab('axisangle_vs_distance_r') as pylab:
        pylab.plot(axis_angle[right], distance_from_wall[right], 'r.', markersize=ms)
        #
        pylab.xlabel('axis angle (deg)')
        pylab.ylabel('distance from wall  (m)')
        pylab.title('only right saccades  (%s)' % id)
        pylab.axis([-180, 180, 0, 1])
    
    with report.data_pylab('axisangle_vs_distance_rm') as pylab:
        pylab.plot(-axis_angle[right], distance_from_wall[right], 'r.', markersize=ms)
        #
        pylab.xlabel('axis angle (deg)')
        pylab.ylabel('distance from wall  (m)')
        pylab.title('only right saccades (mirror) (%s)' % id)
        pylab.axis([-180, 180, 0, 1])
    
    with report.data_pylab('approachangle_vs_distance_lr') as pylab:
        pylab.plot(approach_angle[right], distance_from_wall[right], 'r.', markersize=ms)
        pylab.plot(approach_angle[left], distance_from_wall[left], 'b.', markersize=ms)
        pylab.xlabel('approach angle (deg)')
        pylab.ylabel('distance from wall  (m)')
        pylab.title('left and right saccades  (%s)' % id)
        pylab.axis([-60, 60, 0, 1])
  
        
    f = report.figure('randomness', shape=(3, 3))
    f.sub('axisangle_vs_distance')
    f.sub('axisangle_vs_distance_lr')
    f.sub('axisangle_vs_distance_l')
    f.sub('axisangle_vs_distance_r')
    f.sub('axisangle_vs_distance_rm')
    f.sub('approachangle_vs_distance_lr')
    
    
    smooth_displacement = saccades['smooth_displacement']
    with report.data_pylab('smooth_displacement_hist') as pylab:
        bins = range(-180, 180, 10)
        pylab.hist(smooth_displacement, bins, normed=True)
        pylab.xlabel('inter-saccade smooth displacement (deg)')
        pylab.ylabel('density')
        pylab.title('smooth displacement  (%s)' % id)
        # pylab.axis([-180, 180, 0, 700])
  
    f = report.figure('smooth')
    f.sub('smooth_displacement_hist')
  
    return report

def compute_turning_probability(approach_angle, saccade_angle):
    spacing = 5
    approach = range(-45, 45 + spacing, spacing)
    probability_left = []
    for a in approach:
        inbin = np.logical_and(a - spacing <= approach_angle,
                                   approach_angle <= a + spacing)
        angles = saccade_angle[inbin]
        num_left = (angles > 0).astype('int').sum()
        prob = num_left * 1.0 / len(angles) 
        probability_left.append(prob)
    return approach, np.array(probability_left)


def write_report(report, output_dir):
    filename = os.path.join(output_dir, 'index.html')
    print("Writing on %s..." % filename)
    report.to_html(filename)
    print("...done")

def add_position_information(saccades, arena_center=[0.15, 0.48], arena_radius=1.0):
    info_dtype = [
        ('distance_from_wall', 'float64'),
        ('distance_from_center', 'float64'),
        ('axis_angle', 'float64'),
        ('approach_angle', 'float64'), # degrees
        ('saccade_angle', 'float64'), # degrees
    ]

    info = np.zeros(dtype=info_dtype, shape=(len(saccades),))
    
    for i, saccade in enumerate(saccades):
        x = saccade['position'][0]
        y = saccade['position'][1]
        ax = x - arena_center[0]
        ay = y - arena_center[1]
        
        distance_from_center = np.hypot(ax, ay)
        
        distance_from_wall = arena_radius - distance_from_center
        assert distance_from_wall > 0
        
        saccade_angle = saccade['sign'] * saccade['amplitude']    
        theta = np.radians(saccade['orientation_start'])
        
        approach_angle = compute_approach_angle(ax, ay, theta, radius=arena_radius)

        axis_angle = compute_axis_angle(ax, ay, theta)
        
        info[i]['distance_from_center'] = distance_from_center
        info[i]['distance_from_wall'] = distance_from_wall
        info[i]['saccade_angle'] = saccade_angle
        info[i]['axis_angle'] = np.degrees(axis_angle)
        info[i]['approach_angle'] = np.degrees(approach_angle)
        
    return merge_fields(saccades, info)


def add_position_information_to_rows(rows,
                                     arena_center=[0.15, 0.48], arena_radius=1.0):
    info_dtype = [
        ('distance_from_wall', 'float64'),
        ('distance_from_center', 'float64'),
        ('axis_angle', 'float64'),
        ('approach_angle', 'float64'), # degrees 
    ]

    info = np.zeros(dtype=info_dtype, shape=(len(rows),))
    
    # let's keep track of the maximum error
    min_distance_from_wall = arena_radius
    num_outside = 0
    
    for i, row in enumerate(rows):
        x = row['position'][0]
        y = row['position'][1]
        ax = x - arena_center[0]
        ay = y - arena_center[1]
        
        distance_from_center = np.hypot(ax, ay)
        
        distance_from_wall = arena_radius - distance_from_center
        if distance_from_wall <= 0:
            num_outside += 1
            
            if distance_from_wall < min_distance_from_wall:
                msg = ('Fly is outside of arena for %d/%d (of %d) samples. '
                       'New record: %s' % 
                       (num_outside, i + 1, len(rows), distance_from_wall))
                print(msg)
#            
#            Arena: %s radius %s distance %s position %s' % 
#                    (arena_center, arena_radius, distance_from_center,
#                                         row['position']))
        
                min_distance_from_wall = distance_from_wall
            
            distance_from_wall = 0
            # also correct coordinates to put it inside:
            correct = (arena_radius - 0.01) / distance_from_center 
            ax *= correct
            ay *= correct 
        theta = row['reduced_angular_orientation']
        
        approach_angle = compute_approach_angle(ax, ay, theta,
                                                radius=arena_radius)
        axis_angle = compute_axis_angle(ax, ay, theta)

        info[i]['distance_from_center'] = distance_from_center
        info[i]['distance_from_wall'] = distance_from_wall
        info[i]['axis_angle'] = np.degrees(axis_angle)
        info[i]['approach_angle'] = np.degrees(approach_angle)
        
    return merge_fields(rows, info)  


@contract(x='float', y='float', theta='float', returns='>=-pi,<=pi')
def compute_axis_angle(x, y, theta):
    ''' x,y: coordinates with respect to center of arena.
        Returns the angle in radians. '''
    angle = np.arctan2(y, x)
    axis_angle = normalize_pi(theta - angle)
    return axis_angle
  



