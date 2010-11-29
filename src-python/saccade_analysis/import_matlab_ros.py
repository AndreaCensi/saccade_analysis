from optparse import OptionParser
import os

from flydra_db import FlydraDB
import numpy
import scipy.io
from geometric_saccade_detector.structures import saccade_dtype
from flydra_render.main_filter_meat import straighten_up_theta
from saccade_analysis.constants import EXP_DATA_TABLE, SACCADES_TABLE

description = "Imports the saccade data from Ros' Matlab files to FlydraDB."
 

def main():
    parser = OptionParser(usage=description)
    parser.add_option("--saccade_data", help="Main data directory", 
                      default='saccade_data')
    parser.add_option("--flydra_db", help='Location of output db.',
                      default='saccade_data_flydradb')
        
    (options, args) = parser.parse_args() #@UnusedVariable
    
    verbose = True
    
    flydra_db = FlydraDB(options.flydra_db, create=True)
    
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
            
            sample = file[file.index('_')+1:file.index('.')]
            
            if verbose:
                print("  - Considering sample {0}".format(sample.__repr__()))
        
            if not flydra_db.has_sample(sample):
                flydra_db.add_sample(sample)
            
            filename = os.path.join(group_dir, file)
            
            exp_data, attributes = read_raw_data(filename)
            
            consider_importing_processed(flydra_db, sample, exp_data, attributes)
            
            flydra_db.set_attr(sample, 'species', attributes['species'])
            flydra_db.set_attr(sample, 'background', attributes['background'])
            
            flydra_db.set_table(sample, EXP_DATA_TABLE, exp_data)
            flydra_db.add_sample_to_group(sample, group)
            flydra_db.add_sample_to_group(sample, 'ros')
            
    flydra_db.close()
# 
#        processed_dir = os.path.join(group_dir, 'processed')
#        if not os.path.exists(processed_dir):
#            if verbose:
#                print "No processed data found for %s." % group
#            pass
#            
#        else:
#            for conf in os.listdir(processed_dir):                
#                saccades = os.path.join(processed_dir, conf, 'saccades.mat')
#                if os.path.exists(saccades): 
#                    group_record.configurations[conf] = saccades
#                    # add to general list
#                    self.configurations.add(conf)
##                    else:
##                        conf_dir = os.path.join(processed_dir, conf)
##                        for file in [file for file in os.listdir(conf_dir) 
##                            if file.startswith('processed_data_') and file.endswith('.mat')]: 
##                                  id = file[5:-7]
#
#            # if we don't have exp data, get list of samples from
#            # processed data
#            if group_record.configurations and \
#                not group_record.has_experimental_data:
#                saccades = saccades_read_mat(saccades)
#                group_record.samples = set(numpy.unique(saccades['sample']))
#                for sample in group_record.samples:
#                    self.sample2group[sample] = group
#
#        if len(group_record.samples)> 0:
#            self.groups[group] = group_record
#                
#            print "has it", group, group_record.has_experimental_data
#        

def read_raw_data(filename):
    ''' Read .mat file from Ros. Returns table, attributes. '''
    data = scipy.io.loadmat(filename, squeeze_me=True)
    
    data = data['magno']
    
    # convert from array to hash
    assert isinstance(data, numpy.ndarray)
    data = dict(map(lambda field: (field, data[field]), data.dtype.fields))
    # convert from array to string
    for k in list(data.keys()):
        # maybe this only for ROS :(
        if data[k].dtype == numpy.dtype('object'):
            data[k] = data[k].item()
        if data[k].dtype.char == 'U':
            data[k] = str(data[k])
            print 'converted attribute to %r' % data[k]
        
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
            
    filters = ['unfiltered', 'filt_butter_default', 
               'filt_butter_challis', 'filt_kalman'];
               
    for f in filters:
        if not f in data:
            continue
        
        d = data[f]
        if d.dtype == numpy.dtype('object'):
            d = d.item()
        
        for threshold1 in d.dtype.fields.keys():
            d1 = d[threshold1].item()
            if d1.dtype.fields is None: # empty object
                continue
            for threshold2 in d1.dtype.fields.keys():
                d2 = d1[threshold2].item()
                saccades = convert_saccades_from_ros_format(sample,exp_data, d2)
                configuration='%s-%s-%s' % (f,threshold1,threshold2)
                print '    configuration %s' % configuration
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
    sac_index = d['sac_index'].item()
    sac_peak_vel = d['sac_peak_vel'].item()
    # sac_peak_index = d['sac_peak_index'].item()
    sac_dur = d['sac_dur'].item()
    int_sac_dur = d['int_sac_dur'].item()

    saccades = numpy.ndarray(dtype=saccade_dtype, shape=(len(sac_amp)-1,))
    for i in range(1, len(sac_amp)):
        k = i-1
        saccades[k]['sign'] = numpy.sign(sac_amp[i])
        saccades[k]['amplitude'] = numpy.abs(sac_amp[i])
        
        index_start = sac_index[0,i]-1 # this is matlab
        index_stop = sac_index[1,i] -1 
        
        saccades[k]['time_start'] = timestamp[index_start]
        saccades[k]['time_stop'] = timestamp[index_stop]
        saccades[k]['duration'] = sac_dur[i] / 1000
        saccades[k]['time_passed'] = int_sac_dur[i-1] / 1000
        saccades[k]['orientation_start'] = orientation[index_start]
        saccades[k]['orientation_stop'] = orientation[index_stop]
        saccades[k]['top_velocity'] = sac_peak_vel[i]
        saccades[k]['sample'] = sample
    return saccades

if __name__ == '__main__':
    main()