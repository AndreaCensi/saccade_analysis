import glob, os, yaml, sys

from create_report_data import *

def create_comments_files(images_dir, comments_dir):
    """ Creates a .yaml file in  $2 for each image in $1 """
    
    # where to look for the images
    join = os.path.join 
#    report_dir = join(data_dir, 'report')
    
    # where to put the comments
 #   comments_dir = join(data_dir, 'comments')
    
    # obtain files in data_dir/report ending in .eps
    eps_files = glob.glob(join(images_dir, '*.eps'))
    
    if len(eps_files) == 0:
        sys.stderr.write('Warning, could not find any file in "%s"\n' % images_dir)
        sys.exit(-1)
    
    
    basenames = images_list(images_dir)
    
    print 'Basename: ', basenames
    
    # for each basename, create a file in data_dir/comments/ if it doesn't exist
    for b in basenames:
        comments_file = join(comments_dir, b + '.tex')
        if not os.path.exists(comments_file):
            print 'Creating file %s ' % comments_file
            f = open(comments_file, 'w')
            # data = { 'comments': ''}
            # f.write(yaml.dump(data, default_flow_style=False))
            f.close()


if __name__ == '__main__':
    
    images_dir = sys.argv[1]
    comments_dir = sys.argv[2]
    
    create_comments_files(images_dir, comments_dir)
    
    