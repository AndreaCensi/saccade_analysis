import sys
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.transforms as mtransforms
import datetime
import pytz
import random
import glob
from scipy.signal import filtfilt, butter, fftconvolve

def get_idx_of_change_to_one(arr):
    arr = np.array(arr)
    cond1 = arr[1:]==1 # indices of elements that are one
    cond2 = (arr[1:]-arr[:-1]) != 0 # indices of changed elements
    cond = cond1 & cond2
    return np.nonzero(cond)[0]+1

def test_get_idx_of_change_to_one():
    a = [0,0,0,1,1,1,0,0,1,1,1,1,0,1]
    actual = get_idx_of_change_to_one(a)
    expected = [3,8,13]
    assert np.allclose(actual,expected)

def detect_saccades( ori_vel, n_sigma=2 ):
    zero_mean = ori_vel - np.mean(ori_vel)
    sigma = np.std(ori_vel)
    locs = (abs(zero_mean) > n_sigma*sigma)
    idxs = get_idx_of_change_to_one(locs)
    return idxs

def fix_xax(ax):
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(format_date))
    for label in ax.get_xticklabels():
        label.set_rotation(30)
        label.set_horizontalalignment('right')

def make_hist_line(vals, bins, zero=0):
    assert len(bins) == len(vals)+1
    xs = []
    ys = []
    for i in range(len(bins)-1):
        xs.append( bins[i] )
        ys.append( zero )
        xs.append( bins[i] )
        ys.append( vals[i] )

        xs.append( bins[i+1] )
        ys.append( vals[i] )
        xs.append( bins[i+1] )
        ys.append( zero )
    return np.array(xs), np.array(ys)

def saccade_hist(ax,saccade_times,color):
    print 'saccade_hist not implemented'
    bins = np.arange(0,1.0,0.05)
    ISIs = saccade_times[1:]-saccade_times[:-1]
    vals,bin_edges = np.histogram( ISIs, bins=bins, new=True )
    x,y = make_hist_line( vals, bins )
    print vals
    print bin_edges
    print vals.shape
    print bin_edges.shape

    print 'vals',vals
    ax.plot( x,y, color )

global h2_ax1, h2_ax2, h2_ax3, h2_ax4
h2_ax1, h2_ax2, h2_ax3, h2_ax4 = None,None,None,None

def saccade_hist2(fig,saccade_idxs,color):
    global h2_ax1, h2_ax2, h2_ax3, h2_ax4
    ISIs = saccade_idxs[1:]-saccade_idxs[:-1]

    bins = np.arange(1,500)
    vals,bin_edges = np.histogram( ISIs, bins=bins, new=True )
    b2 = (bin_edges[:-1]+bin_edges[1:])*0.5

    log10_geometric_bins = np.linspace(0,3,20)
    geometric_bins = 10**log10_geometric_bins
    LB_vals, geometric_bin_edges = np.histogram( ISIs, bins=geometric_bins, new=True )

    #################
    h2_ax1 = fig.add_subplot(2,3,1,
                             sharex=h2_ax1,
                             frameon=False,
                             label='%s'%random.random())
    h2_ax1.plot(b2,vals,color+'.',ms=7)

    #################
    h2_ax2 = fig.add_subplot(2,3,2,
                             sharex=h2_ax2,
                             frameon=False,
                             label='%s'%random.random())
    h2_ax2.plot( np.log10(b2), np.log10(vals), color+'.', ms=7)

    #################
    h2_ax3 = fig.add_subplot(2,3,3,
                             sharex=h2_ax3,
                             frameon=False,
                             label='%s'%random.random())
    h2_ax3.plot( log10_geometric_bins[:-1], np.log10(LB_vals), color+'.', ms=7)

    #################
    h2_ax4 = fig.add_subplot(2,3,4,
                             sharex=h2_ax4,
                             frameon=False,
                             label='%s'%random.random())
    h2_ax4.plot( log10_geometric_bins[:-1], np.log10(LB_vals/geometric_bins[:-1]), color+'.', ms=7)
    h2_ax4.set_xlim((0,3.0))

pacific = pytz.timezone('US/Pacific')
def format_date(x, pos=None):
    date_time_str = str(datetime.datetime.fromtimestamp(x,pacific))
    time_str = date_time_str.split()[1]
    return time_str

def main():
    # path = sys.argv[1]
    # filenames = glob.glob('%s/*.mat'%(path ,))
    filenames = glob.glob('*.mat')
    print filenames
    filenames.sort()

    for file_enum,filename in enumerate(filenames):
 
        print filename

        ## if file_enum!=3:
        ##     continue

        if filename != 'data_Dmelanogaster-20080704-154647.mat':
            continue

        print filename
        a=scipy.io.loadmat(filename,
                           struct_as_record=True)
        data=a['data']
        ts = data['exp_timestamps'][0,0][0,:]
        ori = data['exp_orientation'][0,0][0,:]

        if 0:
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.plot(ts[1:]-ts[:-1])

        dt = 1./100

        order = 2
        if 0:
            best_f = None
            best_err = None
            for f in np.linspace(0.15,0.35,10):
                butter_b,butter_a = butter(order,f)
                fori = filtfilt(butter_b,butter_a,ori)
                r = fori-ori
                a_func = fftconvolve(r,r[::-1]) # correlate in freq. domain
                a_func = a_func/a_func[len(r)-1] # normalize so autocorrelation at t=0 is 1
                R_SS_L = a_func[len(r)-1:]
                err = np.sum(R_SS_L[1:]**2)
                print 'f,err',f,err
                plt.plot( a_func, label='%s: %s'%(f,err) )
                if best_err is None or err < best_err:
                    best_err = err
                    best_f = f
            plt.plot( [len(r)-1,len(r)-1], [-10,10], 'k:' )
            plt.legend()
        elif 1:
            import auto_filter_cutoff
            best_f = auto_filter_cutoff.abp(ori)
	    print best_f
        else:
            prev = {'data_Dmelanogaster-20080410-174953.mat':0.64375, # high
                    'data_Dmelanogaster-20080626-151946.mat':0.18671875,
                    'data_Dmelanogaster-20080626-174721.mat':0.3984375, # high
                    'data_Dmelanogaster-20080627-154223.mat':0.33203125, # ?
                    'data_Dmelanogaster-20080627-162448.mat':0.3125, # ?
                    'data_Dmelanogaster-20080627-172709.mat':0.6453125, # high
                    'data_Dmelanogaster-20080702-151655.mat':0.1640625,
                    'data_Dmelanogaster-20080702-175038.mat':0.23828125,
                    'data_Dmelanogaster-20080703-165245.mat':0.31796875,
                    'data_Dmelanogaster-20080703-175708.mat':0.25390625,
                    'data_Dmelanogaster-20080704-154647.mat':0.28984375,
                    'data_Dmelanogaster-20080704-165040.mat':0.29296875,
                    'data_Dmelanogaster-20080708-154007.mat':0.35859375, #?
                    'data_Dmelanogaster-20080708-163736.mat':0.2625,
                    'data_Dmelanogaster-20080708-171906.mat':0.38359375, # high
                    }

            best_f = prev.get(filename,0.25) # did above
            best_f = .3
        natural_frequency = best_f
        print 'natural_frequency',natural_frequency
        butter_b,butter_a = butter(order,best_f)

        fori = filtfilt(butter_b,butter_a,ori)

        ori_vel = (ori[2:]-ori[:-2])/(2*dt)
        fori_vel = (fori[2:]-fori[:-2])/(2*dt)


        ori = ori[1:-1]
        fori = fori[1:-1]
        ts = ts[1:-1]

        saccade_idxs = detect_saccades( ori_vel, n_sigma=2 )
        fsaccade_idxs = detect_saccades( fori_vel, n_sigma=2 )
        saccade_times = ts[saccade_idxs]
        fsaccade_times = ts[fsaccade_idxs]

        if 1:
            # timeseries plot
            fig = plt.figure()
            fig.text(0,0,filename)
            ax1 = fig.add_subplot(2,1,1)
            ax1.plot(ts,ori%360.0,'r-')
            ax1.plot(ts,fori%360,'b-')
            dot_transform= mtransforms.blended_transform_factory(ax1.transData,
                                                                 ax1.transAxes)
            line,=ax1.plot(saccade_times,0.95*np.ones_like(saccade_times),'r.',ms=6)
            line.set_transform(dot_transform)
            line,=ax1.plot(fsaccade_times,0.90*np.ones_like(fsaccade_times),'b.',ms=6)
            line.set_transform(dot_transform)
            fix_xax(ax1)

            ax2 = fig.add_subplot(2,1,2,sharex=ax1)
            ax2.plot(ts,ori_vel,'r-')
            ax2.plot(ts,fori_vel,'b-')
            ax2.xaxis.set_major_formatter(mticker.FuncFormatter(format_date))
            dot_transform= mtransforms.blended_transform_factory(ax2.transData,
                                                                 ax2.transAxes)
            line,=ax2.plot(saccade_times,0.95*np.ones_like(saccade_times),'r.',ms=6)
            line.set_transform(dot_transform)
            line,=ax2.plot(fsaccade_times,0.90*np.ones_like(fsaccade_times),'b.',ms=6)
            line.set_transform(dot_transform)
            fix_xax(ax2)
            fig.subplots_adjust(left=.16,bottom=.17,hspace=0.4)

        if 0:
            fig = plt.figure()
            fig.text(0,0,filename)
            ax1 = fig.add_subplot(1,1,1)
            saccade_hist(ax1,saccade_times,'r')
            ax2 = fig.add_subplot(1,1,1,sharex=ax1,frameon=False)
            saccade_hist(ax2,fsaccade_times,'b')
            ax1.set_xlabel('ISI (s)')
            ax1.set_ylabel('N')

        if 1:
            # Various plots to estimate mu (from Sims)
            fig = plt.figure()
            fig.text(0,0,'%s: cutoff freq %s'%(filename,best_f))

            #ax1 = fig.add_subplot(1,1,1)
            saccade_hist2(fig,saccade_idxs,'r')
            #ax2 = fig.add_subplot(1,1,1,sharex=ax1,frameon=False)
            saccade_hist2(fig,fsaccade_idxs,'b')
            fig.savefig('%s-stats.png'%filename)
    plt.show()

if __name__=='__main__':
    main()

