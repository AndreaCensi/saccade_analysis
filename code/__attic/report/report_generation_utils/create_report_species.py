import glob, os, yaml, sys

def create_report_species(species_dir, report_filename, include_empty_descriptions):
    join = os.path.join 
    splitext = os.path.splitext
    
    report_dir = join(species_dir, 'report')
    comments_dir = join(species_dir, 'comments')
    
    report_file = open(join(report_dir, report_filename), 'w')
    report_file.write("""\
\\documentclass{report}
\\usepackage{fullpage}
\\usepackage{float}

\\usepackage{graphicx}
\\begin{document}
""")
    
    # obtain files in species_dir/report ending in .eps
    eps_files = glob.glob(join(report_dir, '*.eps'))
    
    if len(eps_files) == 0:
        sys.stderr.write('Warning, could not find any file in "%s"' % report_dir)
        sys.exit(-1)
    
    # obtain the basename
    def get_basename(x):
        dirname, basename = os.path.split(x)
        basename, extension = os.path.splitext(basename)
        return basename
    
    all_images = [ get_basename(x) for x in eps_files ]
    
    image_basenames = all_images
    exclude_post = ['_fm', '_detail']
    for e in exclude_post:
        image_basenames = [x for x in image_basenames if not x.endswith(e)]
    
    
    # load all comments files
    comments = []
    basename2comment = {}
    for f in glob.glob(join(comments_dir, '*.yaml')):
        basename = get_basename(f)
        data = yaml.load(open(f))
        data['basename'] = basename
        comments.append(data)
        basename2comment[basename] = data
    
    image_with_comments = [x['basename'] for x in comments if len(x['comments'].strip()) > 0]
    
    
    if not include_empty_descriptions:
        use = image_with_comments
    else:
        use = image_basenames
        
    for i, basename in enumerate(use):
        if basename2comment.has_key(basename):
            comments = basename2comment[basename]['comments'].strip()
            if len(comments) > 0:
                report_file.write("""\
\\textbf{Comments on Figure \\ref{fig:%s}:}
 
%s
""" % (basename, comments))
            
        report_file.write("""\
\\begin{figure}[h!]
    \includegraphics[]{%s}
    \caption{\label{fig:%s}}
\\end{figure}
""" % (basename,basename))
    
        if i % 2 == 1:
            report_file.write("\\clearpage\\vfill\\pagebreak")
        
    report_file.write("""\
\\end{document}
""")

if __name__ == '__main__':
    
    species_dir = sys.argv[1]
    create_report_species(species_dir, report_filename='all.tex', include_empty_descriptions=True)
    create_report_species(species_dir, report_filename='short.tex', include_empty_descriptions=False)