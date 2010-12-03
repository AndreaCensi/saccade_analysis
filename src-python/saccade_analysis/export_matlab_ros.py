import os, numpy, scipy.io
from optparse import OptionParser

from flydra_db import FlydraDB

from .constants import EXP_DATA_TABLE, SACCADES_TABLE

description = "Exports the saccade data to Ros' format"

def main():
    parser = OptionParser(usage=description)
    parser.add_option("--out", help="Output data directory",
                      default='flydra2ros')
    parser.add_option("--db", help='Location of input Flydra db.',
                      default='flydra_db')
        
    (options, args) = parser.parse_args() #@UnusedVariable
    
    verbose = True
    def printv(s):
        if verbose:
            print(s)
    
    db = FlydraDB(options.db, create=False)
    
    
    configuration = 'use_for_report'
    
    for sample in db.list_samples():
        if not db.has_table(sample, table=SACCADES_TABLE, version=configuration):
            continue
        
        group = guess_group(db, sample)
        magno = {}
        
        table = db.get_table(sample, SACCADES_TABLE, configuration)
    
        species = db.get_attr(sample, 'species', 'Dmelanogaster')
    
        magno['species'] = species
        magno['sample'] = sample#_name
        
        if db.has_table(sample, EXP_DATA_TABLE):
            exp_data = db.get_table(sample, EXP_DATA_TABLE)
            print exp_data.dtype
            timestamp = exp_data[:]['timestamp']
        else:
            timestamp = None
        
        magno['use_for_report'] = convert_saccades_to_ros(table, timestamp) 
        
        db.release_table(table)
        if timestamp is not None:
            db.release_table(exp_data)
        
        output_dir = os.path.join(options.out, group)
        filename = os.path.join(output_dir, 'magno_%s.mat' % sample)
        
        printv("writing to %s" % filename)
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        scipy.io.savemat(filename, {'magno':magno}, oned_as='row')
        
        # put species and sample
    print "closing"
    db.close()


def guess_group(db, sample):
    groups = db.list_groups_for_sample(sample)
    # choose the smallest
    key = lambda group: len(db.list_samples_for_group(group))
    sorted_groups = sorted(groups, key=key)
    group = sorted_groups[0]
    return group


def convert_saccades_to_ros(saccades, timestamp):
    n = len(saccades)
    
    ros = {}
    ros['sac_amp'] = sac_amp = numpy.zeros(n)
    ros['sac_index'] = sac_index = numpy.zeros(shape=(2, n), dtype='int')
    ros['sac_peak_vel'] = sac_peak_vel = numpy.zeros(n)
    ros['sac_peak_index'] = sac_peak_index = numpy.zeros(n)
    ros['sac_dur'] = sac_dur = numpy.zeros(n)
    ros['int_sac_dur'] = int_sac_dur = numpy.zeros(n)
        
    for i, saccade in enumerate(saccades):
        sac_amp[i] = saccade['sign'] * saccade['amplitude']
        sac_index[0, i] = 1 + timestamp2index(timestamp, saccade['time_start'])
        sac_index[1, i] = 1 + timestamp2index(timestamp, saccade['time_stop'])
        middle = 0.5 * (saccade['time_start'] + saccade['time_stop'])
        sac_peak_index[i] = 1 + timestamp2index(timestamp, middle)
        int_sac_dur[i] = saccade['time_passed'] * 1000
        sac_dur[i] = saccade['duration'] * 1000
        sac_peak_vel[i] = saccade['top_velocity']
        
    return ros

def timestamp2index(timestamp, t):
    ''' Returns -1 if timestamp not available '''
    if timestamp is None:
        return - 1
    else:
        n = len(timestamp)
        k = (t - timestamp[0]) / (timestamp[-1] - timestamp[0]) # [0,1]
        k = numpy.floor(k * n) # [0,n]
        if k == n:
            k = n - 1
        return k
        

if __name__ == '__main__':
    main()
    
    
