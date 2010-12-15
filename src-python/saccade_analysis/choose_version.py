import numpy
from optparse import OptionParser

from flydra_db import FlydraDB

from .constants import SACCADES_TABLE


def main():
    parser = OptionParser()
    
    parser.add_option("--db", help="FlydraDB directory")
    
    (options, args) = parser.parse_args() #@UnusedVariable
        
    if not options.db:
        raise Exception('Please define the FlydraDB directory using `--db`.')
    
    db = FlydraDB(options.db)  
    
    choose = {                 
        'andrea_detector': {
         'Dpseudoobscura': 'threshold16',
         'Dananassae': 'threshold10',
         'Dhydei': 'threshold7',
         'Dmelanogaster': 'threshold1',
         'Darizonae': 'threshold9',
         'Dmojavensis': 'threshold7',
         'peter': 'peters_conf',
         'mamaramaposts': 'use_for_report',
         'mamaramanoposts': 'use_for_report'
        },
        'ros_detector': {
         'Dpseudoobscura': 'filt_kalman-amp_th_10-th_4',
         'Dananassae': 'filt_kalman-amp_th_10-th_4',
         'Dhydei': 'filt_kalman-amp_th_10-th_4',
         'Dmelanogaster': 'filt_kalman-amp_th_10-th_4',
         'Darizonae': 'filt_kalman-amp_th_10-th_4',
         'Dmojavensis': 'filt_kalman-amp_th_10-th_4'
        }
    }
    
    for official, choices in choose.items():
        for group, version in choices.items():
            print("Group %r: %r -> %r" % (group, version, official))
            samples = db.list_samples_for_group(group)
            for sample in samples:
                print(" sample %r" % sample)
                table = db.get_table(sample, SACCADES_TABLE, version=version) 
                
                copy = numpy.array(table, dtype=table.dtype)
                db.set_table(sample=sample, table=SACCADES_TABLE,
                             version=official, data=copy)
                db.release_table(table)


    db.close()
    
if __name__ == '__main__':
    main()
