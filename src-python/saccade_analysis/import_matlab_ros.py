import traceback
import os
import numpy
import scipy.io
import cPickle as pickle
from optparse import OptionParser

from flydra_db import FlydraDB
# TODO: remove dependency
from geometric_saccade_detector.structures import saccade_dtype
# TODO: remove dependency
from flydra_render.main_filter_meat import straighten_up_theta

from .constants import EXP_DATA_TABLE, SACCADES_TABLE

description = "Imports the saccade data from Ros' Matlab files to FlydraDB."
 

def main():
    parser = OptionParser(usage=description)
    parser.add_option("--saccade_data", help="Main data directory",
                      default='saccade_data')
    parser.add_option("--db", help='Location of output Flydra db.')
        
    (options, args) = parser.parse_args() #@UnusedVariable
    
    if not options.db:
        raise Exception('Please define FlydraDB directory using `--db`.')
    
    verbose = True
    
    flydra_db = FlydraDB(options.db, create=True)
    
    matlab_dir = options.saccade_data
    for group in os.listdir(matlab_dir):
        group_dir = os.path.join(matlab_dir, group)
        if not os.path.isdir(group_dir):                
            continue
        
        if verbose:
            print("Opening {0}".format(group))
        
        for file in [file for file in os.listdir(group_dir) 
            if (file.startswith('magno_')) \
               and file.endswith('.mat')]:
            
            sample = file[file.index('_') + 1:file.index('.')]
            
            if verbose:
                print("  - Considering sample {0}".format(sample.__repr__()))
        
            if not flydra_db.has_sample(sample):
                flydra_db.add_sample(sample)
            flydra_db.add_sample_to_group(sample, group)
#           flydra_db.add_sample_to_group(sample, 'ros')
            
            filename = os.path.join(group_dir, file)
            
            exp_data, attributes = read_raw_data(filename)
            
            consider_importing_processed(flydra_db, sample, exp_data, attributes)
            
            flydra_db.set_attr(sample, 'species', attributes['species'])
            flydra_db.set_attr(sample, 'background', attributes['background'])            
            flydra_db.set_table(sample, EXP_DATA_TABLE, exp_data)
            
    flydra_db.close()

def read_raw_data(filename):
    ''' Read .mat file from Ros. Returns table, attributes. '''
    data = scipy.io.loadmat(filename, squeeze_me=True)
    
    data = data['magno']
    
    # convert from array to hash
    assert isinstance(data, numpy.ndarray)
    data = dict([(field, data[field]) for field in data.dtype.fields])
    # convert from array to string
    for k in list(data.keys()):
        # maybe this only for ROS :(
        if data[k].dtype == numpy.dtype('object'):
            data[k] = data[k].item()
        if data[k].dtype.char == 'U':
            data[k] = str(data[k])
            # print('converted attribute to %r' % data[k])
        
    # make sure everything is 1d array
    def as1d(x):  
        if x.dtype == 'object':
            x = x.tolist()
        return x.reshape(len(x))
    
    orientation = as1d(data.pop('exp_orientation'))
    timestamp = as1d(data.pop('exp_timestamps'))
    assert len(orientation) == len(timestamp)
    n = len(orientation)
    #dtype = [(('timestamp', 'Timestamp (seconds since the epoch)'), 'float64'),
    #         (('orientation', 'Fly orientation (degrees)'), 'float64')]
    dtype = [('timestamp', 'float64'),
             ('orientation', 'float64')]
    table = numpy.ndarray(shape=(n,), dtype=dtype)
    table['timestamp'][:] = timestamp[:]
    table['orientation'][:] = numpy.rad2deg(straighten_up_theta(orientation[:]))
    return table, data

def consider_importing_processed(flydra_db, sample, exp_data, data):
            
    filters = [
               'unfiltered',
               'filt_butter_default',
               'filt_butter_challis',
               'filt_kalman'
               ]
               
    for f in filters:
        if not f in data:
            continue
        
        d = data[f]
        if d.dtype == numpy.dtype('object'):
            d = d.item()
        
        if d.dtype == numpy.dtype('float64'):
            print("got invalid data for filter = %s  = %s" % (f, d))
            continue
        
        for threshold1 in d.dtype.fields.keys():
            d1 = d[threshold1].item()
            if d1.dtype.fields is None: # empty object
                continue
            for threshold2 in d1.dtype.fields.keys():
                d2 = d1[threshold2].item()
                configuration = '%s-%s-%s' % (f, threshold1, threshold2)
                if flydra_db.has_table(sample, table=SACCADES_TABLE,
                                       version=configuration):
                    # skip; already done
                    continue
                    #pass
                
                try:
                    saccades = \
                        convert_saccades_from_ros_format(sample, exp_data, d2)
                    
                except Exception as e:
                    traceback.print_exc()
                    print("(!) Could not convert saccade data: %s" % e)
                    dir = 'failed-imports'
                    if not os.path.exists(dir):
                        os.makedirs(dir)
                        
                    filename = 'saccades-%s-matlab.pickle' % configuration
                    filename = os.path.join(dir, filename)
                    print("(!) I'll save the data to %r so you can have a look." % 
                          filename)
                    with open(filename, 'wb') as file:
                        pickle.dump(d2, file)
                    raise
                
                print('    configuration %s' % configuration)
                flydra_db.set_table(sample=sample, table=SACCADES_TABLE,
                                    data=saccades, version=configuration)


#    
def convert_saccades_from_ros_format(sample, exp_data, d):

#    % sac_index: [2x107 double]                    % 
#    %        sac_amp: [1x107 double] % deg
#    %   sac_peak_vel: [1x107 double]
#    % sac_peak_index: [1x107 double]
#    %        sac_dur: [1x107 double] % ms
#    %    int_sac_dur: [1x106 double] (ms) int_sac(i) = 1000 * (ts(starts(i+1)) - ts(stops(i))); % now in ms
    
    timestamp = exp_data[:]['timestamp']
    orientation = exp_data[:]['orientation']
    
    sac_amp = d['sac_amp'].item()
    num = sac_amp.size
    if num <= 3:
        saccades = numpy.ndarray(dtype=saccade_dtype, shape=(0,))
        return saccades
    
    sac_index = d['sac_index'].item()
    sac_peak_vel = d['sac_peak_vel'].item()
    # sac_peak_index = d['sac_peak_index'].item()
    sac_dur = d['sac_dur'].item()
    int_sac_dur = d['int_sac_dur'].item()
    
    
    saccades = numpy.ndarray(dtype=saccade_dtype, shape=(num - 1,))
    for i in range(1, num):
        k = i - 1
        saccades[k]['sign'] = numpy.sign(sac_amp[i])
        saccades[k]['amplitude'] = numpy.abs(sac_amp[i])
        
        index_start = sac_index[0, i] - 1 # this is matlab
        index_stop = sac_index[1, i] - 1 
        
        saccades[k]['time_start'] = timestamp[index_start]
        saccades[k]['time_stop'] = timestamp[index_stop]
        saccades[k]['duration'] = sac_dur[i] / 1000
        saccades[k]['time_passed'] = int_sac_dur[i - 1] / 1000
        saccades[k]['orientation_start'] = orientation[index_start]
        saccades[k]['orientation_stop'] = orientation[index_stop]
        saccades[k]['top_velocity'] = sac_peak_vel[i]
        saccades[k]['sample'] = sample
    return saccades

if __name__ == '__main__':
    main()
    
    
