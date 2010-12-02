from optparse import OptionParser
import os
import numpy
import scipy.io

from flydra_db import FlydraDB
from geometric_saccade_detector.structures import saccade_dtype
from flydra_render.main_filter_meat import straighten_up_theta
from saccade_analysis.constants import EXP_DATA_TABLE, SACCADES_TABLE

description = "Exports the saccade data to Ros' format"

def main():
    parser = OptionParser(usage=description)
    parser.add_option("--out", help="Output data directory", 
                      default='flydra2ros')
    parser.add_option("--db", help='Location of input Flydra db.',
                      default='flydra_db')
        
    (options, args) = parser.parse_args() #@UnusedVariable
    
    verbose = True
    
    db = FlydraDB(options.db, create=False)
    
    
    configuration = 'use_for_report'
    
    for sample in db.list_samples():
        if not db.has_table(sample, table=SACCADES_TABLE, version=configuration):
            continue
        
        magno = {}
        
        table = db.get_table(sample, SACCADES_TABLE, configuration)
    
    
        db.release_table(table)
        
        groups = db.list_groups_for_sample(sample)
        # choose the smallest
        key=lambda group: len(db.list_samples_for_group(group))
        sorted_groups = sorted(groups, key=key)
        group = sorted_groups[0]
        
        output_dir = os.path.join(options.out, group)
        filename = os.path.join(output_dir, 'magno_%s.mat' % sample)
        
        print "writing to %s" % filename
        
        # put species and sample
    db.close()

if __name__ == '__main__':
    main()
    
    