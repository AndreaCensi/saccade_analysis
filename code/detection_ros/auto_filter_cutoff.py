import numpy as np
from scipy.signal import filtfilt, butter, fftconvolve
from scipy.optimize import fmin
import scipy

def abp(arr,order=2,disp=1):
    arr = np.array(arr)
    f = 0.5 # start freq
    def calc_err(f):
        butter_b,butter_a = butter(order,f)
        farr = filtfilt(butter_b,butter_a,arr)
        r = farr-arr
        a_func = fftconvolve(r,r[::-1]) # correlate in freq. domain
        a_func = a_func/a_func[len(r)-1] # normalize so autocorrelation at t=0 is 1
        R_SS_L = a_func[len(r)-1:]
        err = np.sum(R_SS_L[1:]**2)
        print '  error at %s: %s'%(f,err)
        return err
    xopt=fmin(calc_err,f,
              xtol=0.001,
              disp=disp)

    ## xopt,extras=fmin(calc_err,f,
    ##                  xtol=0.001,
    ##                  disp=disp,
    ##                  full_output=True,
    ##                  retall=True)
    ## fopt,iter,funcalls,warnflag,allvecs = extras

    ## print 'warnflag',warnflag
    ## print 'fopt',fopt
    assert len(xopt)==1
    return xopt[0]
