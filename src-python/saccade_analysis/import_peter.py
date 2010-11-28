import os
import numpy
from numpy import degrees, radians
import cPickle as pickle
from optparse import OptionParser
import datetime

from flydra_render.main_filter_meat import straighten_up_theta
from flydra_db.db import  safe_flydra_db_open

from saccade_analysis.constants import EXP_DATA_TABLE

description = """

This scripts takes the data in Peter Weir's logs and
writes the data in the FlydraDB.

"""

def main():
    parser = OptionParser(usage=description)
    parser.add_option("--peters_pickle", 
                      help="Peter's pickle file", default='weir.pkl')
    parser.add_option("--flydra_db", help="FlydraDB directory", default='flydra_db')
     
    (options, args) = parser.parse_args()
     
    if args:
        raise Exception('Extraneous arguments: %r' % args)

    if not os.path.exists(options.peters_pickle):
        raise Exception('File %r does not exist. ' % options.peters_pickle)
    
    
    print "Loading file %r ..." % options.peters_pickle
    data = pickle.load(open(options.peters_pickle, 'rb'))
    print "...done."

    
    with safe_flydra_db_open(options.flydra_db, create=True) as flydra_db:
        for experiment, flies in data.items():
            experiment = experiment.replace('/','')
            for fly, fly_data in flies.items(): 
                import_sample(flydra_db, experiment, fly, fly_data)
            
            
def import_sample(flydra_db, experiment, fly, fly_data):
    times = fly_data.pop('times')
    
    date = datetime.datetime.fromtimestamp(times[0])            
    timestamp = date.strftime('%Y%m%d-%H%M%S')
    sample_id = '%s_%s' % (experiment, timestamp)
  

    #
    # first fix orientation
    #
    exp_orientation = fly_data.pop('orientations')
    
    problematic, = numpy.nonzero(
                    numpy.logical_not(numpy.isfinite(exp_orientation)))
    
    print problematic, exp_orientation[problematic]
    
    # just replace with the previous one
    for i in problematic:
        exp_orientation[i] = exp_orientation[i-1]

    # renormalize so it's easier to visualize
    exp_orientation = degrees(straighten_up_theta(radians(exp_orientation))) 
    
    #
    # now fix timestamps
    # 
    dt_guess = (times[-1]-times[0]) / len(times)
    # recompute the timestamps
    exp_timestamps = times[0] + dt_guess * numpy.array(range(0, len(times)))
    
    max_var = numpy.abs(exp_timestamps-times).max()
    
    print "Estimated real dt: %f  corresponding to %.2f FPS" % (dt_guess,
                                                                1/dt_guess)
    print "Maximum deviation: %fs" % max_var
    
    print "Length: %d seconds " % (exp_timestamps[-1]-exp_timestamps[0])


    dtype = [('timestamp', 'float64'),
              ('orientation', 'float64')]
    table = numpy.ndarray(shape=(len(exp_timestamps),), dtype=dtype)
    table['timestamp'][:] = exp_timestamps[:]
    table['orientation'][:] = exp_orientation[:]
    
    #
    # other fields
    # 
    attributes = {
        'experiment': experiment,
        'species': 'Dmelanogaster',
        'sample': sample_id, 
        'dt_guess': dt_guess,
        'fps_guess': 1/dt_guess
    }
    
    # put other fields specific to Peter
    for k, v in fly_data.items(): 
        if k == 'background':
            if v is None:
                v = []
            if isinstance(v, numpy.ndarray):
                print v.dtype
                if str(v.dtype) == 'object' or len(v) == 1:
                    v = []
                     
        attributes[k] = v
    
    if not flydra_db.has_sample(sample_id):
        flydra_db.add_sample(sample_id)
    
    flydra_db.add_sample_to_group(sample_id, experiment)
    flydra_db.add_sample_to_group(sample_id, 'peter')
        
    flydra_db.set_table(sample=sample_id, table=EXP_DATA_TABLE,
                        data=table)
    
    attributes.pop('x')
    attributes.pop('y')
    attributes.pop('background')
    
    for k,v in attributes.items():
        try:
            flydra_db.set_attr(sample_id, k, v)
        except:
            print "Can't set attribute %r of class %s" % (k, v.__class__)

