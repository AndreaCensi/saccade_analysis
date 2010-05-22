import pylab

import report_tools
from report_tools.node import ReportNode
from report_tools.figures import MultiFigure
import numpy
import scipy


def my_xcorr(v, max_lags=20):
    v = v - numpy.mean(v)
    xc = scipy.correlate(v, v, 'full')
    lags = numpy.array(range(-len(v) + 1, len(v)))
    
    some = numpy.nonzero(numpy.abs(lags) <= max_lags)
    
    xc = xc[some]
    lags = lags[some]
    
    return xc, lags
    
    
def analyze_saccades(report_id, saccades):
    sign = saccades['sign']
    
    fig1 = MultiFigure(id='fig')

    pylab.ioff()
    
    for format in ['pdf', 'png', 'eps']:
        with fig1.attach_file('sign_xcorr.%s' % format) as filename:
            pylab.figure()

            xc, lags = my_xcorr(sign, max_lags=10) 

            pylab.plot(lags, xc, 'x-') 
            pylab.xlabel('lags')
            pylab.ylabel('correlation')
            pylab.title('Sign correlation vs distance')
            pylab.savefig(filename)
            pylab.close()
    fig1.add_subfigure('sign_xcorr', caption='sign_xcorr')
    
    if 0:
        for format in ['pdf', 'png', 'eps']:
            with fig1.attach_file('sign.%s' % format) as filename:
                pylab.figure() 
                pylab.plot(sign) 
                pylab.title('Sign')
                pylab.savefig(filename)
                pylab.close()
        fig1.add_subfigure('sign', caption='sign')
    



    return ReportNode(id=report_id, children=[fig1])
