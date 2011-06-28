from reprep import Report
import numpy as np

from saccade_analysis.markov.first_order import binofit
from .report_axis_angle import create_report_axis_angle

def create_report_subset(id, desc, saccades):
    report = Report('subset_' + id)
    report.text('description', '''%s\n%d saccades total.''' % (desc, len(saccades)))
    
    #f = report.figure(cols=3)
 
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
        
    #report.last().add_to(f)
    
    with report.data_pylab('distance_from_wall') as pylab:
        distance = saccades['distance_from_wall']
        pylab.hist(distance, 100)
        pylab.xlabel('meters')
        pylab.ylabel('number of saccades')
        pylab.title('Distance from center (%s)' % id)
        a = pylab.axis()
        pylab.axis([0, 1, 0, a[3]])
        
    #report.last().add_to(f)
  
    with report.data_pylab('saccade_angle') as pylab:
        pylab.hist(saccade_angle, range(-180, 185, 5))
        pylab.xlabel('degrees')
        pylab.ylabel('number of saccades')
        pylab.title('Saccade angle (%s)' % id)
        a = pylab.axis()
        pylab.axis([-180, 180, 0, a[3]])
    
    #  report.last().add_to(f)
  
    with report.data_pylab('approach_angle') as pylab:
        pylab.hist(approach_angle, range(-60, 65, 5))
        pylab.xlabel('degrees')
        pylab.ylabel('number of saccades')
        pylab.title('Approach angle (%s)' % id)
        a = pylab.axis()
        pylab.axis([-60, 60, 0, a[3]])
    
    #  report.last().add_to(f)
  
    with report.data_pylab('approach_vs_saccade') as pylab:
        pylab.plot(approach_angle, saccade_angle, '.')
        pylab.xlabel('approach angle (deg)')
        pylab.ylabel('saccade angle (deg)')
        pylab.title('Approach vs saccade angle (%s)' % id)
        a = pylab.axis()
        pylab.axis([-60, 60, -180, 180])
    
    #  report.last().add_to(f)
  
    
    # compute probability
    approach, probability_left, probability_right, margin_left, margin_right = \
        compute_turning_probability(approach_angle=approach_angle,
                                    saccade_angle=saccade_angle)
    with report.data_pylab('turning_probability') as pylab:
        n = len(approach)
        el = np.zeros((2,n))
        el[0,:] = +(margin_left[0,:]-probability_left)
        el[1,:] = -(margin_left[1,:]-probability_left)
        pylab.errorbar(approach, probability_left, el,None, None,
                       ecolor='g', label='left',  capsize=8, elinewidth=1)
        er = np.zeros((2,n))
        er[0,:] = +(margin_right[0,:]-probability_right)
        er[1,:] = -(margin_right[1,:]-probability_right)
        pylab.errorbar(approach, probability_right, er, None, None,
                       ecolor='r', label='right',   capsize=8, elinewidth=1)

        pylab.plot(approach, probability_left, 'g-', label='left')
        pylab.plot(approach, probability_right, 'r-', label='right')
        pylab.xlabel('approach angle (deg)')
        pylab.ylabel('probability of turning')
        pylab.title('Probability of turning (%s)' % id)
        a = pylab.axis()
        pylab.plot([0, 0], [0.2, 0.8], 'k--')
        pylab.axis([-60, 60, 0, 1])
        pylab.legend()
 
    #   report.last().add_to(f)
 
    bin_size = 10
    saccade_bin_centers = np.array(range(-180, 185, bin_size))
    n = len(saccade_bin_centers)
    saccade_bins = np.zeros(shape=(n + 1))
    saccade_bins[0:n] = saccade_bin_centers - bin_size
    saccade_bins[n] = saccade_bin_centers[-1]
    
    bin_centers = np.array(range(-50, 55, 5))
    bin_size = 15
    distributions = []
    for angle in bin_centers:
        indices, = np.nonzero(
                    np.logical_and(
                        approach_angle > angle - bin_size,
                        approach_angle < angle + bin_size
                    ))
        x = saccade_angle[indices]
        if len(indices) > 0:
            # Otherwise histogram divides by 0
            hist, edges = np.histogram(x, bins=saccade_bins, normed=True) #@UnusedVariable
        else:
            hist, edges = np.histogram(x, bins=saccade_bins, normed=False) #@UnusedVariable
        
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
    
    f = report.figure(cols=3)
    f.sub('distance_from_center', caption='Distance from center')
    f.sub('saccade_angle', caption='Saccade angle')
    f.sub('approach_angle', caption='Approach angle')
    f.sub('approach_vs_saccade', caption='Approach vs saccade angle')
    f.sub('turning_probability', caption='Probability of turning')
    f.sub('distribution_vs_approach2', caption='Saccade distribution vs approach angle')
    f.sub('distribution_vs_approach', caption='Saccade distribution vs approach angle')
    
    return report
    
def create_report_randomness(id, desc, saccades): #@UnusedVariable
    report = Report(id)
   
    f = report.figure(cols=3)
     

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
        
    report.last().add_to(f)
 
    
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
  
    report.last().add_to(f)

 
    with report.data_pylab('axisangle_vs_distance_l') as pylab:
        # 
        pylab.plot(axis_angle[left], distance_from_wall[left], 'b.', markersize=ms)
        pylab.xlabel('axis angle (deg)')
        pylab.ylabel('distance from wall  (m)')
        pylab.title('only left saccades  (%s)' % id)
        pylab.axis([-180, 180, 0, 1])
        
    report.last().add_to(f)
 
 
    with report.data_pylab('axisangle_vs_distance_r') as pylab:
        pylab.plot(axis_angle[right], distance_from_wall[right], 'r.', markersize=ms)
        #
        pylab.xlabel('axis angle (deg)')
        pylab.ylabel('distance from wall  (m)')
        pylab.title('only right saccades  (%s)' % id)
        pylab.axis([-180, 180, 0, 1])
 
    report.last().add_to(f)
 
    with report.data_pylab('axisangle_vs_distance_rm') as pylab:
        pylab.plot(-axis_angle[right], distance_from_wall[right], 'r.', markersize=ms)
        #
        pylab.xlabel('axis angle (deg)')
        pylab.ylabel('distance from wall  (m)')
        pylab.title('only right saccades (mirror) (%s)' % id)
        pylab.axis([-180, 180, 0, 1])
        
    report.last().add_to(f)
 
    
    with report.data_pylab('approachangle_vs_distance_lr') as pylab:
        pylab.plot(approach_angle[right], distance_from_wall[right], 'r.', markersize=ms)
        pylab.plot(approach_angle[left], distance_from_wall[left], 'b.', markersize=ms)
        pylab.xlabel('approach angle (deg)')
        pylab.ylabel('distance from wall  (m)')
        pylab.title('left and right saccades  (%s)' % id)
        pylab.axis([-60, 60, 0, 1])
 
    report.last().add_to(f)
    
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
    bin_size = 15
    approach = range(-45, 45 + spacing, spacing)
    probability_left = []
    probability_right = []
    margin_left = []
    margin_right = []
    for a in approach:
        inbin = np.logical_and(a - bin_size <= approach_angle,
                                   approach_angle <= a + bin_size)
        angles = saccade_angle[inbin]
        
        num = len(angles) * 1.0
        num_left = (angles > 0).astype('int').sum()
        num_right = num - num_left
        
        alpha = 0.01
        margin_left.append(binofit(num_left, num, alpha))
        margin_right.append(binofit(num_right, num, alpha))
        
        
        if num == 0:
            probability_left.append(np.NaN)
            probability_right.append(np.NaN)
        else:
            probability_left.append(num_left / num)
            probability_right.append(num_right / num)
        
    return (approach, 
        np.array(probability_left), 
        np.array(probability_right),
        np.array(margin_left).T,
        np.array(margin_right).T )
