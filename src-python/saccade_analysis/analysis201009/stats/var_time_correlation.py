import numpy
import scipy.stats
import itertools
from reprep import Report
from saccade_analysis.analysis201009.stats.turnograms import zoom_rgb
from reprep.graphics.posneg import posneg
from reprep.graphics.scale import scale
from saccade_analysis.analysis201009.stats.utils import attach_description

def get_correlation_matrix(saccades, vars, delays, type):
    ''' Returns Correlation, p-value, labels.
    
        type can be 'pearson', 'spearman', 
     '''
    maximum_delay = numpy.max(delays)    
    
    labels = []
    xs = []
    for delay in delays:
        
        for i, var in enumerate(vars):
            label = "%s[%+d]" % (var.letter, -delay) if delay > 0 else \
                var.letter + ''
            labels.append(label)
            
            x = saccades[var.field]
            T = len(x)
            
            x_delayed = x[delay:]
            target_length = T - maximum_delay
            if len(x_delayed) > target_length:
                # keep the last
                x_cut = x_delayed[0:target_length]
            else:
                x_cut = x_delayed
                
            # if delay != 0:
            #    assert x_cut[0] != x[0]
            
            #print var.field, x[:10]
            #print "delayed", delay, x_cut[:10]
            
            assert len(x_cut) == target_length
            
            xs.append(x_cut)
    
    N = len(xs)
    R = numpy.ndarray((N, N), dtype='float64')
    P = numpy.ndarray((N, N), dtype='float64')
    
    types = {'kendall': scipy.stats.kendalltau,
             'pearson': scipy.stats.pearsonr,
             'spearman': scipy.stats.spearmanr}
    if not type in types:
        raise ValueError('Unknown correlation type "%s". Try: %s' % 
                         (type, types.keys()))
    function = types[type]

    for i, j in itertools.product(range(N), range(N)):
        r, p = function(xs[i], xs[j])
        R[i, j] = r
        P[i, j] = p
    return R, P, labels
        

def group_var_time_correlation(
        group, configuration, saccades,
        variables, delays, type='pearson'):
    
    # all together
    R, P, labels = get_correlation_matrix(saccades, variables, delays,
                                          type)
    
    #  Significance 
    S = P < 0.01 
    
    nvars = len(variables)
    Rhalf = R[:nvars, :]
    Phalf = P[:nvars, :]
    Shalf = S[:nvars, :]
    
    ylabels = labels[:nvars]
    
    r = Report()
        
    attach_description(r, create_description(variables, delays, type))
    
    with r.data_pylab('correlation') as pylab:
        draw_correlation_figure(pylab, labels, ylabels, Rhalf)
        
    rshow = lambda x: "%+.2f" % x
    r.table('correlation_values', values_to_strings(Rhalf, rshow),
            cols=labels, rows=ylabels, caption="%s coefficient" % type)    
    r.table('pvalues', values_to_strings(Phalf, pvalue_format),
            cols=labels, rows=ylabels, caption="p-values")    

    with r.data_pylab('significance') as pylab:
        draw_significance_figure(pylab, labels, ylabels, Shalf)
            
    
    return r
    
def pvalue_format(p):
    s = "%.3f" % p
    if p < 0.01:
        s = "**" + s
    elif p < 0.05:
        s = "*" + s
    
    return s

def sample_var_time_correlation(
        sample, expdata, configuration, saccades,
        variables, delays, type='pearson'):
    
    # all together
    R, P, labels = get_correlation_matrix(saccades, variables, delays,
                                          type)
    
    #  Significance 
    S = P < 0.01 
    
    nvars = len(variables)
    Rhalf = R[:nvars, :]
    Phalf = P[:nvars, :]
    Shalf = S[:nvars, :]
    
    ylabels = labels[:nvars]
    
    r = Report()
    attach_description(r, create_description(variables, delays, type))
    with r.data_pylab('correlation') as pylab:
        draw_correlation_figure(pylab, labels, ylabels, Rhalf)

    rshow = lambda x: "%+.2f" % x
    r.table('correlation_values', values_to_strings(Rhalf, rshow),
            cols=labels, rows=ylabels, caption="%s coefficient" % type)    
    r.table('pvalues', values_to_strings(Phalf, pvalue_format),
            cols=labels, rows=ylabels, caption="p-values")    

    with r.data_pylab('significance') as pylab:
        draw_significance_figure(pylab, labels, ylabels, Shalf)
    
    return r


    
def values_to_strings(M, format):
    l = []
    for i in range(M.shape[0]):
        r = []
        for j in range(M.shape[1]):
            r.append(format(M[i, j]))
        l.append(r)
    return l
    
    
def draw_matrix_and_labels(pylab, xlabels, ylabels, rgb):
    zoomed = zoom_rgb(rgb, zoom=64)

    if False:
        m = numpy.flipud(zoomed)
    else:
        m = zoomed
        ylabels = list(ylabels)
        ylabels.reverse()
    pylab.imshow(m, extent=(0, len(xlabels), 0, len(ylabels)))
    
    ax = pylab.gca() 
    ax.set_xticks(numpy.array(range(len(xlabels))) + 0.5)
    ax.set_xticklabels(xlabels)
    ax.set_yticks(numpy.array(range(len(ylabels))) + 0.5)
    ax.set_yticklabels(ylabels)
    
    for tick in pylab.gca().xaxis.iter_ticks():
        tick[0].label2On = True
        tick[0].label1On = False


def draw_correlation_figure(pylab, xlabels, ylabels, R):
    rgb = posneg(R, max_value=1)
    draw_matrix_and_labels(pylab, xlabels, ylabels, rgb)    


def draw_significance_figure(pylab, xlabels, ylabels, P):
    def format(p):
        return 1 if p else 0
    # x = numpy.array(values_to_strings(P, format))
    
    rgb = scale(P * 1.0, max_color=[0, 1, 0])
    #print x
    #print rgb
    draw_matrix_and_labels(pylab, xlabels, ylabels, rgb)    


def create_description(variables, delays, type):
    description = """
    
These figures show the correlation analysis among the
various saccade variables:

"""

    for var in variables:
        description += """
- **{var.letter}**: {var.name}        
  
""".format(var=var)


    description += """

These variables are compared with themselves, and themselves
delayed by {lag} step. Several figures are shown next:

""".format(lag=delays[-1])

    type_description = {
'kendall': '''
* `Kendall's  tau rank correlation coefficient 
  <http://en.wikipedia.org/wiki/Kendall_tau_rank_correlation_coefficient>`_,
  as a picture and as a table.
* The associated p-value, as a table, and as a picture, where
  green means the correlation is significant.

''',
'pearson': ''' 

* `Pearson's correlation coefficient 
  <http://en.wikipedia.org/wiki/Pearson_product-moment_correlation_coefficient>`_, 
  as a picture and as a table.
* The associated p-value, as a table, and as a picture, where
  green means the correlation is significant.

''',
'spearman': '''

* `Spearman's rank correlation coefficient
  <http://en.wikipedia.org/wiki/Spearman%27s_rank_correlation_coefficient>`_, 
  as a picture and as a table.
* The associated p-value, as a table, and as a picture, where
  green means the correlation is significant.


'''}
    
    description += type_description[type]
 
    return description

