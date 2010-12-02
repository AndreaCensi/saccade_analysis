#
#import sys, numpy
#from optparse import OptionParser
#
#from rfsee.rfsee_client import ClientTCP, ClientProcess
#
#from flydra_render import logger
#from flydra_db import FlydraDB
#from flydra_db.progress import progress_bar
#
#description = """
#
#
#
#"""
#
#def main():
#    
#    
#    parser = OptionParser()
#
#    parser.add_option("--db", default='flydra_render_output',
#                      help="FlydraDB directory")
#    
#    parser.add_option("--min_linear_velocity", default=0.05, type="float",
#                      help='Minimum linear velocity to be considered'
#                      ' (do not consider when the fly is stationary)')
#    
#    (options, args) = parser.parse_args()
#    
#
#    if options.db is None:
#        logger.error('Please specify a directory using --db.')
#        sys.exit(-1)
#            
#    db = FlydraDB(options.db)
#    
#    # get a list of all samples
#    samples = db.list_samples()
#    # get the ones where we have the rows table
#    samples = filter(lambda x: db.has_rows(x), samples)
#    
#    # divide in two groups
#    posts = lambda x: db.get_attr(x, 'stimulus') != 'nopost'
#    noposts = lambda x: not posts(x)  
#    groups = {}
#    groups['posts'] = filter(posts, samples)
#    groups['noposts'] = filter(noposts, samples)
#    
#    for group_name, group_samples in groups.items():
#        stats = PolarStats()
#        for sample in group_samples:
#            rows = db.get_rows(id)
#            # get linear velocity
#            lvel = rows[:]['linear_velocity_modulus']
#            # interesting samples
#            interesting = lvel > options.min_linear_velocity  
#            position = rows[interesting]['position']
#            x = position[:, 0]
#            y = position[:, 1]
#            # position with respect to center
#            xc = x - arena_center[0]
#            yc = y - arena_center[1]
#            # angle with respect to center
#            angle = numpy.arctan2(yc, xc)
#            # fly orientation
#            
#            # angle with respect to axis
#            # axis_angle = 
#            # compute distance from wall
#            distance_from_center = numpy.hypot(xc, yc)
#            distance_from_wall = -distance_from_center + arena_radius
#            stats.update()
#
#    for i, sample_id in enumerate(do_samples):
#        
#        print 'Sample %s/%s: %s' % (i + 1, len(do_samples), sample_id)
#        
#        if not db.has_sample(sample_id):
#            raise Exception('Sample %s not found in db.' % sample_id)
#        if not db.has_rows(sample_id):
#            raise Exception('Sample %s does not have rows table.' % sample_id)
#       
#        if options.compute_mu:
#            if db.has_table(sample_id, 'nearness') and not options.nocache:
#                print 'Already computed nearness for %s; skipping' % sample_id
#                continue
#        else:
#            if db.has_table(sample_id, target) and not options.nocache:
#                print 'Already computed luminance for %s; skipping' % sample_id
#                continue
#        
#        rows = db.get_rows(sample_id)
#        stimulus_xml = rows._v_attrs.stimulus_xml
#        
#        results = render(rows, stimulus_xml, host=options.host,
#                         compute_mu=options.compute_mu, white=options.white)
#   
#        db.set_table(sample_id, target, results['luminance'])
#        
#        if options.compute_mu:
#            db.set_table(sample_id, 'nearness', results['nearness'])
#            db.set_table(sample_id, 'retinal_velocities',
#                         results['retinal_velocities'])
#            
#   
#def render(rows, stimulus_xml, host=None, compute_mu=False,
#           white=False):
#    
#    if host is not None:
#        tokens = host.split(':')
#        if len(tokens) == 2:
#            hostname = tokens[0]
#            port = tokens[1]
#        else:
#            hostname = tokens[0]
#            port = 10781
#            
#        cp = ClientTCP(hostname, port)
#    else:
#        cp = ClientProcess()
#        
#    if white: # before stimulus_xml
#        cp.config('osg_params', {'white_arena': True})
#
#
#    cp.config_stimulus_xml(stimulus_xml)    
#    cp.config_compute_mu(compute_mu)
#
#
#    num_frames = len(rows)
#    dtype = [('time', 'float64'),
#             ('obj_id', 'int'),
#             ('frame', 'int'),
#             ('value', ('float32', 1398))]
#    luminance = numpy.zeros(shape=(num_frames,), dtype=dtype)
#    
#    # copy index fields
#    copy_fields = ['time', 'frame', 'obj_id'] 
#    for field in copy_fields: 
#        luminance[field] = rows[:][field]
#    
#    if compute_mu:
#        nearness = numpy.zeros(shape=(num_frames,), dtype=dtype)
#        dtype = [('time', 'float64'),
#                 ('obj_id', 'int'),
#             ('frame', 'int'),
#             ('value', ('float32', (1398, 2)))]
#        retinal_velocities = numpy.zeros(shape=(num_frames,), dtype=dtype)
#        
#        for a in [nearness, retinal_velocities]:
#            for field in copy_fields:
#                a[field] = rows[:][field]
#     
#    #num_frames = 20
#    
#    pb = progress_bar('Rendering', num_frames)
#    
#    for i in range(num_frames):
#        pb.update(i)
#        
#        position = rows[i]['position']
#        attitude = rows[i]['attitude']
#        linear_velocity_body = rows[i]['linear_velocity_body']
#        angular_velocity_body = rows[i]['angular_velocity_body']
#        
#        def simple(x):
#            return [x[0], x[1], x[2]]
#        
#        def simple_matrix(x):
#            return [ [ x[0, 0], x[0, 1], x[0, 2]],
#                     [ x[1, 0], x[1, 1], x[1, 2]],
#                     [ x[2, 0], x[2, 1], x[2, 2]]  ]
#                     
#        res = cp.render(simple(position), simple_matrix(attitude),
#            simple(linear_velocity_body), simple(angular_velocity_body))
#
#        
#        luminance['value'][i] = numpy.array(res['luminance'])
#        
#        if compute_mu:
#            nearness['value'][i] = numpy.array(res['nearness'])
#            retinal_velocities['value'][i] = numpy.array(res['retinal_velocities'])
#    
#    res = {'luminance': luminance}
#    if compute_mu:
#        res['retinal_velocities'] = retinal_velocities
#        res['nearness'] = nearness
#    
#    cp.close()
#
#    return res
#    
#
#if __name__ == '__main__':
#    main()
