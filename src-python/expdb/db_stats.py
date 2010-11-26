from optparse import OptionParser
from expdb.db import SamplesDB, read_samples_db
import time

description = """

This script shows the content of the db.

"""

def main():
    parser = OptionParser(usage=description)
    parser.add_option("--data", help="Main data directory", 
                      default='saccade_data')
    parser.add_option("--rescan", help="Rescan the data directory for new files.")
        
    (options, args) = parser.parse_args() #@UnusedVariable
    
    start = time.time()
    db = read_samples_db(options.data, verbose=True, rescan=options.rescan)
    print "DB indexed in %.2f seconds." % (time.time()-start)
    
    groups = db.list_groups()
    
#    groups = ['Dananassae', 'indoorhalogen']

    start = time.time()
    
    for group in groups:
        print "Group: %s" % group
        print "  Configurations: %s. " %  db.list_configurations(group)
        print "  Samples: %s" % db.list_samples(group)
        print "  Has exp data: %s" % db.group_has_experimental_data(group)
        
    
    for group in groups:
        print "Group: %s" % group
        for configuration in db.list_configurations(group):
            saccades = db.get_saccades_for_group(group, configuration)
            print " - group saccades:  %6d  (%s)" % (len(saccades), configuration) 
        
        for sample in db.list_samples(group):
            print "- sample %s " % (sample)
            if db.has_experimental_data(sample):
                exp_data = db.get_experimental_data(sample)
            
                theta = exp_data['exp_orientation']
                T = exp_data['exp_timestamps']
        
                length = T[-1]-T[0]

                print "  - length: %d minutes" % (length/60)
                print "  - orientation ", theta.dtype, theta.shape
                print "  - time        ", T.dtype, T.shape
                
            for configuration in db.list_configurations(group):
                saccades = db.get_saccades_for_sample(sample, configuration)
                print " - saccades:  %6d  (%s)" % (len(saccades), configuration) 
            
            

    print "Database read in %d seconds. " % (time.time() - start)

if __name__ == '__main__':
    main()