from optparse import OptionParser
from expdb.db import SamplesDB
import numpy



description = """

This script shows the content of the db.

"""

def main():
    parser = OptionParser(usage=description)
    parser.add_option("--data", help="Main data directory", default='.')
        
    (options, args) = parser.parse_args()
    
    db = SamplesDB(options.data)
    
    groups = db.list_groups()
    
    groups = ['Dananassae', 'indoorhalogen']
    
    for group in groups:
        print "Group: %s" % group
        for sample in db.list_samples(group):
            exp_data = db.get_experimental_data(sample)
            
            theta = exp_data['exp_orientation']
            time  = exp_data['exp_timestamps']

            T = exp_data['exp_timestamps']
        
            length = T[-1]-T[0]

            print "- sample %s,  length %fs " % (sample, length)
            print "  - orientation ", theta.dtype, theta.shape
            print "  - time        ", time.dtype, time.shape

if __name__ == '__main__':
    main()