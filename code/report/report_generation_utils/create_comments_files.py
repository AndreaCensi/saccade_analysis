import glob, os, yaml, sys

def create_comments_files(data_dir):
    """ Creates a .yaml file in  $1/comments for each image in $1/report """
    
    # where to look for the images
    join = os.path.join 
    report_dir = join(data_dir, 'report')
    
    # where to put the comments
    comments_dir = join(data_dir, 'comments')
    
    # obtain files in data_dir/report ending in .eps
    eps_files = glob.glob(join(report_dir, '*.eps'))
    
    if len(eps_files) == 0:
        sys.stderr.write('Warning, could not find any file in "%s"' % report_dir)
        sys.exit(-1)
    
    # obtain the basename
    def get_basename(x):
        dirname, basename = os.path.split(x)
        basename, extension = os.path.splitext(basename)
        return basename
    
    basenames = [ get_basename(x) for x in eps_files ]
    
    # for each basename, create a file in data_dir/comments/ if it doesn't exist
    for b in basenames:
        comments_file = join(comments_dir, b + '.yaml')
        if not os.path.exists(comments_file):
            print 'Creating file %s ' % comments_file
            f = open(comments_file, 'w')
            data = { 'priority': 1, 'comments': ''}
            f.write(yaml.dump(data, default_flow_style=False))
            f.close()


if __name__ == '__main__':
    
    data_dir = sys.argv[1]
    create_comments_files(data_dir)