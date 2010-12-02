import numpy
from optparse import OptionParser

from flydra_db import FlydraDB
from .constants import SACCADES_TABLE


def main():
    parser = OptionParser()
    
    parser.add_option("--db", default='flydra_db', help="FlydraDB directory")
    
    (options, args) = parser.parse_args() #@UnusedVariable
        

    db = FlydraDB(options.db)  
    
    official = 'use_for_report'
    choices = {
      'Dpseudoobscura': 'threshold16',
     'Dananassae': 'threshold10',
     'Dhydei': 'threshold7',
     'Dmelanogaster': 'threshold1',
     'Darizonae': 'threshold9',
     'Dmojavensis': 'threshold7',
     
     'peter': 'peters_conf'
    }
    
    for group, version in choices.items():
        print "Group %r" % group
        samples = db.list_samples_for_group(group)
        for sample in samples:
            print " sample %r" % sample
            table = db.get_table(sample, SACCADES_TABLE, version=version) 
            
            copy = numpy.array(table, dtype=table.dtype)
            db.set_table(sample=sample, table=SACCADES_TABLE, 
                         version=official, data=copy)
            db.release_table(table)


    db.close()
    
if __name__ == '__main__':
    main()
