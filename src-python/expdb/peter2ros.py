import os
import numpy
from numpy import degrees, radians
import cPickle as pickle
from optparse import OptionParser

from flydra_render.filtering import straighten_up_theta
import datetime
import scipy.io

description = """

This scripts takes the data in Peter Weir's logs and
writes the data out according to Ros's convention for
organizing files.

"""

def main():
    parser = OptionParser(usage=description)
    parser.add_option("--peters_pickle", 
                      help="Peter's pickle file", default='weir.pkl')
    parser.add_option("--data", help="Main data directory", default='.')
    
    parser.add_option("--nocache", action='store_true',
                      default=False, help="Do not skip files if already present.")
    
    booleans = {'yes':True,'no':False}
    parser.add_option("--write_matlab", help="Writes out Matlab files.",
                      default='yes', type='choice', choices=booleans.keys())
    parser.add_option("--write_pickle", help="Writes out pickle files",
                      default='no', type='choice', choices=booleans.keys())
    
    (options, args) = parser.parse_args()
    
    options.write_matlab = booleans[options.write_matlab]
    options.write_pickle = booleans[options.write_pickle]

    if args:
        raise Exception('Extraneous arguments: %s' % args.__repr__())

    if not os.path.exists(options.peters_pickle):
        raise Exception('File %s does not exist. ' % options.peters_pickle)
    
    
    print "Loading file %s ..." % options.peters_pickle
    data = pickle.load(open(options.peters_pickle, 'rb'))
    print "...done."

    for experiment, flies in data.items():
        experiment = experiment.replace('/','')
        for fly, fly_data in flies.items(): #@UnusedVariable
            
            times = fly_data.pop('times')
            
            date = datetime.datetime.fromtimestamp(times[0])            
            timestamp = date.strftime('%Y%m%d-%H%M%S')
            sample_id = '%s_%s' % (experiment, timestamp)
          
            dirname = os.path.join(options.data, experiment)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            pickle_filename = os.path.join(dirname, 'data_' + sample_id +'.pickle')
            mat_filename = os.path.join(dirname, 'data_' + sample_id +'.mat')

            if not options.nocache and \
                (os.path.exists(pickle_filename) or not options.write_pickle) and \
                (os.path.exists(mat_filename) or not options.write_matlab):
                print "Skipping %s" % sample_id
                continue


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
            
            #dt = numpy.diff(times)
            # there are a few big errors, and many low errors
            #dt_guess = numpy.percentile(dt, 80)
            
            dt_guess = (times[-1]-times[0]) / len(times)
            
            
            # recompute the timestamps
            exp_timestamps = times[0] + dt_guess * numpy.array(range(0, len(times)))
            
            max_var = numpy.abs(exp_timestamps-times).max()
            
            print "Estimated real dt: %f  corresponding to %.2f FPS" % (dt_guess,
                                                                        1/dt_guess)
            print "Maximum deviation: %fs" % max_var
            
            print "Length: %d seconds " % (exp_timestamps[-1]-exp_timestamps[0])

            #
            # other fields
            #
            
            
            
            data = {
                'experiment': experiment,
                'species': 'Dmelanogaster',
                'sample': sample_id, 
                'exp_orientation': exp_orientation,
                'exp_timestamps': exp_timestamps,
                'dt_guess': dt_guess,
                'fps_guess': 1/dt_guess
            }
            
            # put other fields specific to Peter
            for k, v in fly_data.items():
#                if v is None or \
#                    (isinstance(v, numpy.ndarray) and (v[0] is None)):
#                    # cannot represent this in matlab
#                    v = 'none'
                if k == 'background':
                    if v is None:
                        v = []
                    if isinstance(v, numpy.ndarray):
                        print v.dtype
                        if str(v.dtype) == 'object' or len(v) == 1:
                            v = []
                             
                data[k] = v
            
            
          
            if options.write_pickle:                
                if os.path.exists(pickle_filename) and not options.nocache:
                    print "File %s already exists; not re-writing." % pickle_filename
                else:            
                    print "Writing ID %s to %s " %( sample_id, pickle_filename)
                    with open(pickle_filename, 'wb') as f:
                        pickle.dump(data, f)
                    
            
            if options.write_matlab:
                if os.path.exists(mat_filename) and not options.nocache:
                    print "File %s already exists; not re-writing." % mat_filename
                else:
                    print "Writing ID %s to %s " %( sample_id, mat_filename)
                    try:
                        scipy.io.savemat(mat_filename, {'data': data}, oned_as='row', 
                                 do_compression=True)
                    except Exception as e:
                        print "ERROR: Could not write to %s: %s" % (mat_filename,e)
                        
                        