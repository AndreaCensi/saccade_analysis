import os, numpy
from optparse import OptionParser

from flydra_db import FlydraDB
from geometric_saccade_detector.io import saccades_read_mat

from .constants import SACCADES_TABLE

description = "Imports the saccade data from Andrea's Matlab files to FlydraDB."
 
def main():
    parser = OptionParser(usage=description)
    parser.add_option("--saccade_data", help="Main data directory",
                      default='saccade_data')
    parser.add_option("--db", help="FlydraDB directory")
     
    parser.add_option("--verbose", help='Verbose output',
                      default=False, action="store_true")
        
    (options, args) = parser.parse_args() #@UnusedVariable
    
    if not options.db:
        raise Exception('Please define FlydraDB directory using `--db`.')
    
    def printv(s):
        if options.verbose:
            print(s)
        
    flydra_db = FlydraDB(options.db, create=True)
    
    matlab_dir = options.saccade_data
    for group in os.listdir(matlab_dir):
        group_dir = os.path.join(matlab_dir, group)
        if not os.path.isdir(group_dir):                
            continue
        
        printv("Opening {0}".format(group))
        
#        
#            
#            exp_data, attributes = read_raw_data(filename)
#            
#            consider_importing_processed(flydra_db, sample, exp_data, attributes)
#            
#            flydra_db.set_attr(sample, 'species', attributes['species'])
#            flydra_db.set_attr(sample, 'background', attributes['background'])
#            
#            flydra_db.set_table(sample, EXP_DATA_TABLE, exp_data)
#            flydra_db.add_sample_to_group(sample, group)
#            flydra_db.add_sample_to_group(sample, 'ros')
#            
    
        processed_dir = os.path.join(group_dir, 'processed')
        
        if not os.path.exists(processed_dir):
            printv("No processed data found for group %r." % group)
            continue
        
        for conf in os.listdir(processed_dir):
            # first look for saccades.mat
            saccades_file = os.path.join(processed_dir, conf, 'saccades.mat')
            if os.path.exists(saccades_file):
                printv('Loading from file %r.' % saccades_file)
                saccades = saccades_read_mat(saccades_file)
                samples = numpy.unique(saccades['sample'])
                for sample in samples:
                    if not flydra_db.has_sample(sample):
                        flydra_db.add_sample(sample)
                    flydra_db.add_sample_to_group(sample, group)
                    sample_saccades = saccades[saccades[:]['sample'] == sample]
                    flydra_db.set_table(sample=sample, table=SACCADES_TABLE,
                                        version=conf, data=sample_saccades)
#            else:
#                prefix = 'data_'
#        suffix = '.mat'
#        for file in [file for file in os.listdir(group_dir) 
#            if (file.startswith(prefix)) and file.endswith(suffix)]:
#            
#            sample = file[len(prefix):file.index('.')]
#            
#            if verbose:
#                print("  - Considering sample {0}".format(sample.__repr__()))
#        
#            if not flydra_db.has_sample(sample):
#                flydra_db.add_sample(sample)
#            
#            filename = os.path.join(group_dir, file)
# 
# 
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
    flydra_db.close()


if __name__ == '__main__':
    main()
