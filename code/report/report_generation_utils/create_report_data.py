import glob, os, yaml, sys


# obtain the basename
def get_basename(x):
    dirname, basename = os.path.split(x)
    basename, extension = os.path.splitext(basename)
    return basename
    
    
def species_list(data_dir):
    return [ get_basename(x) for x in glob.glob(os.path.join(data_dir, 'D*')) ]

def images_list(report_dir, exclude_suffixes = []):
    """ Finds all basenames for images in the given dir """
    eps_files = glob.glob(os.path.join(report_dir, '*.eps'))
    
    if len(eps_files) == 0:
        sys.stderr.write('Warning, could not find any file in "%s"' % report_dir)
        sys.exit(-1)
    
    all_images = [ get_basename(x) for x in eps_files ]
    
    for e in exclude_suffixes:
        all_images = [x for x in all_images if not x.endswith(e)]

    def sign(x):
        if x==0.0:
            return 0
        elif x>0.0:
            return 1
        else:
            return -1

    def datesort(x,y):
        fx = os.path.join(report_dir, x + '.eps')
        fy = os.path.join(report_dir, y + '.eps')
        return sign(os.path.getmtime(fx) - os.path.getmtime(fy) )
        
    all_images.sort(datesort)
    
    return all_images


def load_all_comments(comments_dir):
    """ load all comments files, returns hash basename -> comment """
    basename2comment = {}
    files = glob.glob(os.path.join(comments_dir, '*.yaml'))
    for f in files:
        basename = get_basename(f)
        if basename == 'layout':
            continue
            
        data = yaml.load(open(f))
        
        if len(data['comments'].strip()) == 0:
            continue
        
        data['basename'] = basename
#        comments.append(data)
        basename2comment[basename] = data
    return basename2comment
    
def create_report_data(data_dir, report_filename, include_empty_descriptions):
    species = species_list(data_dir)
    
    join = os.path.join 
    splitext = os.path.splitext
    
    report_dir = join(data_dir, 'report')
    comments_dir = join(data_dir, 'comments')
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    if not os.path.exists(comments_dir):
        os.makedirs(comments_dir)
    
    # obtain files in species_dir/report ending in .eps
    all_images = images_list( join(join(data_dir, species[0]), 'report'), exclude_suffixes=['_fm','_detail'] )
    comments = load_all_comments( comments_dir )
    
    images_with_comments = list(set(all_images) & set(comments.keys()))
    
    if include_empty_descriptions:
        use_images = all_images
    else:
        use_images = images_with_comments
    
    # we now have to choose the order in which 
    # to present all of this information
    # this is contained in the file comments/layout.yaml
    layout_file = join(comments_dir, 'layout.yaml')
    if os.path.exists(layout_file):
        layout = yaml.load(open(layout_file).read())
    else:
        # create the initial layout
        layout = { 'title': 'Report', 'header': "", 'footer':"", "order": all_images }

    order = [x for x in layout['order'] if x in use_images]
    excluded = [ x for x in use_images if not x in layout['order'] ]
    unknown = [ x for x in layout['order']  if not x in use_images ]
    layout['excluded'] = excluded
    layout['unknown'] = unknown

    # save it for the user to edit
    yaml.dump(layout, open(layout_file, 'w'))

    report_file = open(join(report_dir, report_filename), 'w')
    report_file.write("""\
    \\documentclass{report}
    \\usepackage{fullpage}
    \\usepackage{float}
    \\usepackage{subfig}
    \\usepackage{xcolor}
    \\usepackage{graphicx}
    \\begin{document}
    """)

    report_file.write("""\
        \\title{%s}

        \\maketitle
        \\tableofcontents
        \\cleardoublepage
    """ % layout['title'])
    
    report_file.write(layout['header'])
    

    for i, basename in enumerate(order):
        title_path = join(join(join(data_dir, species[0]), 'report'), basename+'.title')
        if os.path.exists(title_path):
            title = open(title_path).read()
        else:
            title = None
        
        has_comments = comments.has_key(basename)
        
        if title is not None:
            section_head = title
            caption = title
        else:
            section_head = basename
            caption = ''
        
        if has_comments:
            section_head = "(*) " + section_head
        
        report_file.write("\\section{%s} \\label{sec:%s}\n\n" % (section_head, basename) )
        
        
        if has_comments:
            comment = comments[basename]['comments'].strip()
        else:
            comment = '{\small \color{gray} No comments about these plots. Edit the file \\verb|%s| to add some.}' % join(comments_dir, basename + '.yaml')
            
        report_file.write("\n\n %s \n\n" % comment)
            
        report_file.write("""\
        \\vfill
\\begin{figure}[h!]
\centering
""")

        for i, s in enumerate(species):
            report_file.write("""\
                \subfloat[%s]{\includegraphics[width=5cm]{../%s/report/%s}}
""" % (s,s,basename))
            row_len = 3
            if i%row_len == row_len-1:
               report_file.write("\n\n") 

            
        report_file.write("""\
    \caption{\label{fig:%s}%s}
\\end{figure}
""" % (basename, caption))
    
        # if i % 2 == 1:
        report_file.write("\\clearpage\\vfill\\pagebreak")
        
    report_file.write("""\
\\end{document}
""")

if __name__ == '__main__':
    
    data_dir = sys.argv[1]
    create_report_data(data_dir, report_filename='all.tex', include_empty_descriptions=True)
    #create_report_data(data_dir, report_filename='short.tex', include_empty_descriptions=False)

    f = open( data_dir + "/report/Makefile" , 'w');
    f.write("""
all: all.pdf short.pdf

%.pdf: %.dvi
\tdvipdf $<
    
%.dvi: %.tex
\tlatex $<
\tlatex $<

""")
    