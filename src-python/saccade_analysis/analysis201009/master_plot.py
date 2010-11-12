import sys, os 
from optparse import OptionParser

from reprep import Report
from reprep.table import Table
from compmake  import set_namespace, comp, compmake_console, batch_command
from compmake.jobs.syntax.parsing import parse_job_list

from expdb.db import  read_samples_db
# The various plots
from saccade_analysis.analysis201009.master_plot_gui import create_gui, \
    create_main_gui
from saccade_analysis.analysis201009.master_plot_vars import variables
from saccade_analysis.analysis201009.stats import \
    fairness, independence, levy_exp, plot_raw_trajectories, \
    plot_simulated_sample_trajectories, group_sign_xcorr, group_sign_hist, \
    plot_detected_saccades, sample_var_hist, group_var_xcorr, group_var_hist, \
    group_var_percentiles, group_var_joint, sample_var_joint, raw_theta_hist, \
    group_saccade_count, group_saccade_density, group_turnogram, \
    group_var_time_correlation, sample_var_time_correlation

import itertools
prod = itertools.product


class Plot:
    def __init__(self, id, command, args={}, desc=None):
        self.id = id
        self.command = command
        assert isinstance(args, dict)
        self.args = args
        if desc is None:
            desc = id
        self.description = desc
    def __str__(self):
        return 'Plot(%s)' % str(self.__dict__)

group_plots = [
    Plot('saccade_count', group_saccade_count,
         desc="Number of detected saccades (raw count)"),
         
    Plot('saccade_density', group_saccade_density,
         desc="Saccade frequency (saccades/second)"),
         
    Plot('sign_hist', group_sign_hist,
         desc="Number of left/right turns"),
         
    Plot('turnogram', group_turnogram,
         desc="Sequence of left/right saccades as a picture"),
         
    Plot('sign_xcorr', group_sign_xcorr,
         desc="Autocorrelation left/right turns"),
         
    Plot('fairness', fairness,
         desc="Statistical tests for balanced left/right"),
         
    Plot('independence', independence,
         desc="Statistical tests for independence of successive turns"),
         
    Plot('levy_vs_exp', levy_exp,
         desc="Levy and exponential fits for saccade interval")
]

sample_saccades_plots = [
    Plot('simulated_trajectories', plot_simulated_sample_trajectories,
         desc="Plots of simulated trajectories (using saccades)"),
]

    
var_group = [v for v in variables if v.percentiles]

for delays, type in prod([[0, 1], [0, 2]],
                         ['pearson', 'spearman', 'kendall']):
    # kendall is very slow and not that important 
    #, 'kendall']:
    
    name = 'timecorr%d%d%s' % (delays[0], delays[1], type)
    desc = 'Correlation analysis (%s, delay: %d)' % (type, delays[-1])
    args = {'variables': var_group, 'delays': delays,
            'type': type}
    
    group_plots.append(Plot(name, group_var_time_correlation, args, desc))
    sample_saccades_plots.append(Plot(name, sample_var_time_correlation, args, desc))
            

for var in variables:
    group_plots.append(Plot('hist_%s' % var.id, group_var_hist, {'variable': var},
                            desc="Histograms of %s" % var.name))
    if var.percentiles:
        group_plots.append(Plot('percentiles_%s' % var.id,
                        group_var_percentiles, {'variable': var},
                        desc="Percentile plots of %s" % var.name))
        
        group_plots.append(Plot('xcorr_%s' % var.id, group_var_xcorr,
                                {'variable': var},
                                desc="Autocorrelation of %s" % var.name))
        
for i, var1 in enumerate(variables):
    for j, var2 in enumerate(variables):
        if i < j and var1.percentiles and var2.percentiles:
            group_plots.append(Plot('joint_%s_%s' % (var1.id, var2.id),
                        group_var_joint, {'var1': var1, 'var2': var2,
                                          'delay1': 0, 'delay2': 0},
                        desc="Joint distribution of %s and %s." % 
                            (var1.name, var2.name)))
            
            sample_saccades_plots.append(Plot('joint_%s_%s' % (var1.id, var2.id),
                        sample_var_joint, {'var1': var1, 'var2': var2,
                                          'delay1': 0, 'delay2': 0},
                        desc="Joint distribution of %s and %s." % 
                            (var1.name, var2.name)))

for var1, var2 in prod(variables, variables):
    if  not var1.percentiles or not var2.percentiles:
        continue
    
    name = 'joint_%s_%s_delayed' % (var1.id, var2.id)
    vars = {'var1': var1, 'var2': var2, 'delay1': 0, 'delay2': 1}
    desc = "Joint distribution of %s at time k " \
           "and %s at k-1." % (var1.name, var2.name)
    group_plots.append(Plot(name, group_var_joint, vars, desc))
    
    name = 'joint_%s_%s_delayed' % (var1.id, var2.id)
    vars = {'var1': var1, 'var2': var2, 'delay1': 0, 'delay2': 1}
    desc = "Joint distribution of %s at time k and %s at k-1." % \
            (var1.name, var2.name)
            
    sample_saccades_plots.append(Plot(name, group_var_joint, vars, desc))
        
        
sample_expdata_plots = [
    Plot('raw_theta_hist', raw_theta_hist,
         desc="Histogram of raw orientation"),
         
    Plot('raw_trajectories', plot_raw_trajectories,
         desc="Plot of simulated trajectories (from raw orientation data)"),
]


for var in variables:
    sample_saccades_plots.append(
        Plot('hist_%s' % var.id, sample_var_hist, {'variable': var},
             desc="Histograms of %s" % var.name))

sample_fullscreen_plots = [
    Plot('saccade_detection', plot_detected_saccades,
         desc="Plot of each and every detected saccade")
]


# define group order and give descriptions
all_groups_description = [   
    ('Dananassae', 'D. ananassae (Ros)'),
    ('Darizonae', 'D. arizonae (Ros)'),
    ('Dhydei', 'D. hydei (Ros)'),
    ('Dmojavensis', 'D. mojavensis (Ros)'),
    ('Dpseudoobscura', 'D. pseudoobscura (Ros)'),
    ('Dmelanogaster', 'D. melanogaster (Ros)'),
    
    ('mamaramanoposts', 'D. melanogaster (Mamarama, no posts)'),
    ('mamaramaposts', 'D. melanogaster (Mamarama, with posts)'),
    
    ('indoorhalogen', 'D. melanogaster (Peter, indoor/halogen)'),
    ('blueFilter', 'D. melanogaster (Peter, blue filter)'),
    ('circularPolarizer', 'D. melanogaster (Peter, circ. polarizer)'),
    ('circularPolarizercloudy', 'D. melanogaster (Peter, circ. polarizer, cloudy)'),
    ('grayFilter', 'D. melanogaster (Peter, gray filter)'),
    ('grayFiltercloudy', 'D. melanogaster (Peter, gray filter, cloudy)'),
    ('noFilter', 'D. melanogaster (Peter, no filter)'),
    ('noFiltercloudy', 'D. melanogaster (Peter, no filter, cloudy)'),
]   

def order_groups(groups):
    ''' yields group, group_desc according to the order
        defined in all_groups_description.
        Note that groups might contain entries not present in all_groups_description. '''
        
    # these are the ones we know a priori
    known_groups = map(lambda t: t[0], all_groups_description)
    # these are the ones that we know and see
    seen = [x for x in known_groups if  x in groups]
    # these are the extra 
    others = [x for x in groups if not x in known_groups]
    order = seen + others
  
    group2desc = dict(all_groups_description)
    # use id as description if not known
    for x in others:
        group2desc[x] = x
        
    for group in order:
        yield group, group2desc[group]
 
description = """ Main script to plot everything. """
 
def main():
    parser = OptionParser(usage=description)
    parser.add_option("--data", help="Main data directory",
                      default='saccade_data')
    parser.add_option("--interactive", action="store_true",
                      default=False,
                      help="Starts an interactive compmake session.")
    parser.add_option("--report", help="Saccade report directory",
                      default='saccade_report')
    parser.add_option("--groups", help="Which groups to consider",
                      default=None)
    parser.add_option("--configurations", help="Which configurations to consider",
                      default=None)
        
    (options, args) = parser.parse_args() #@UnusedVariable
    
    db = read_samples_db(options.data, verbose=True)
    
    if options.groups:
        groups = options.groups.split(', ')
        groupset = "_".join(groups)
    else:
        groups = db.list_groups()
        groupset = 'all' 
        
    if options.configurations:
        configurations = options.configurations.split(',')
        confset = "_".join(configurations)
    else:
        configurations = db.list_all_configurations()
        confset = "all"
        
    combination = '%s_%s' % (groupset, confset)
    output_dir = os.path.join(options.report, combination)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    set_namespace('master_plot_%s' % combination)
        
    
    # we maintain several indices
    
    # key = (group, configuration, plot)
    index_group_plots = {}
    # key = (sample, plot)
    index_sample_expdata_plots = {}
    # key = (sample, configuration, plot)
    index_sample_saccades_plots = {}
    
    configurations_for_group = {}
    
    for group in groups:     
        
        configurations_for_group[group] = \
            set(configurations).intersection(db.list_configurations(group))
        
        for configuration in configurations_for_group[group]:
            
            for plot in group_plots:
                job_id = '%s-%s-%s' % (group, configuration, plot.id)
                
                index_group_plots[(group, configuration, plot.id)] = \
                    comp(wrap_group_plot, options.data, group,
                         configuration, plot.command, plot.args,
                         job_id=job_id)    

            for sample, plot in prod(db.list_samples(group), sample_saccades_plots):
                job_id = '%s-%s-%s' % (sample, configuration, plot.id)
                index_sample_saccades_plots[(sample, configuration, plot.id)] = \
                    comp(wrap_sample_saccades_plot, options.data,
                         sample, configuration, plot.command, plot.args,
                         job_id=job_id)    

        if db.group_has_experimental_data(group):
            for sample, plot in prod(db.list_samples(group), sample_expdata_plots):
                job_id = '%s-%s' % (sample, plot.id)
                index_sample_expdata_plots[(sample, plot.id)] = \
                    comp(wrap_sample_expdata_plot, options.data,
                         sample, plot.command, plot.args, job_id=job_id)    

    # now we create the indices 
    # fix configuration, function; iterate groups
    for configuration, plot in itertools.product(configurations, group_plots):
        subs = []; descs = [];
    
        page_id = "%s.%s" % (configuration, plot.id)
        
        for group, group_desc in order_groups(groups):
            if not configuration in configurations_for_group[group]:
                continue
            
            descs.append(group_desc)
            subs.append(index_group_plots[(group, configuration, plot.id)])
    
        job_id = page_id
        comp(combine_reports, subs, descs, page_id, output_dir,
             job_id=job_id) 
    
    comp(create_gui,
         filename=os.path.join(output_dir, 'group_plots.html'),
         menus=[
                  ('Detector', configurations, configurations),
                  ('Plot/table', map(lambda x:x.id, group_plots),
                    map(lambda x:x.description, group_plots))
        ])
    
    
    # fix group, function; iterate samples
    for group in groups:
        if db.group_has_experimental_data(group):    
            for plot in sample_expdata_plots:
                subs = []; descs = [];
                for sample in db.list_samples(group):
                    descs.append(sample)
                    subs.append(index_sample_expdata_plots[(sample, plot.id)])
                    
                page_id = "%s.%s" % (group, plot.id)
                
                job_id = page_id
                comp(combine_reports, subs, descs, page_id, output_dir,
                     job_id=job_id) 

    # get the ordered group lists and desc
    ordered_groups = map(lambda t: t[0], order_groups(groups))
    ordered_groups_desc = map(lambda t: t[1], order_groups(groups))
    
    comp(create_gui,
         filename=os.path.join(output_dir, 'expdata_plots.html'),
         menus=[
                  ('Group', ordered_groups, ordered_groups_desc),
                  ('Plot/table', map(lambda x:x.id, sample_expdata_plots),
                        map(lambda x:x.description, sample_expdata_plots))
        ])
    
    # fix configuration, group, function; iterate samples
    for configuration in configurations:

        for group in groups:
            if not configuration in configurations_for_group[group]:
                for plot in  sample_saccades_plots:
                    page_id = "%s.%s.%s" % (configuration, group, plot.id)
                    comp(write_empty, page_id, output_dir,
                         'Group %s has not been processed with algorithm "%s".' % 
                         (group, configuration),
                         job_id=page_id)
                continue
                
            for plot  in sample_saccades_plots:
                
                subs = []; descs = [];
                for sample in db.list_samples(group):
                    descs.append(sample)
                    r = index_sample_saccades_plots[(sample, configuration, plot.id)]
                    subs.append(r)
                    
                page_id = "%s.%s.%s" % (configuration, group, plot.id)
                
                job_id = page_id
                comp(combine_reports, subs, descs, page_id, output_dir,
                     job_id=job_id) 

    comp(create_gui,
         filename=os.path.join(output_dir, 'saccade_plots.html'),
         menus=[
                  ('Detector', configurations, configurations),
                  ('Group', ordered_groups, ordered_groups_desc),
                  ('Plot/table', map(lambda x:x.id, sample_saccades_plots),
                                 map(lambda x:x.description, sample_saccades_plots))
        ])
    
    # fix configuration, sample; plot fullsscreen
    
    all_samples = db.list_all_samples()
    
    for configuration in configurations:
        for sample in all_samples:
            group = db.get_group_for_sample(sample)
            # XXX make it clenaer
            if not configuration in configurations_for_group[group]:
                for plot in  sample_fullscreen_plots:
                    page_id = '%s.%s.%s' % (sample, configuration, plot.id)
                    comp(write_empty, page_id, output_dir,
                         'Group %s has not been processed with algorithm "%s".' % 
                         (group, configuration),
                         job_id=page_id)
                #print "skipping sample %s group %s config %s" %\
                #     (sample,group, configuration)
                continue
            
            if not db.group_has_experimental_data(group):
                for plot in  sample_fullscreen_plots:
                    page_id = '%s.%s.%s' % (sample, configuration, plot.id)
                    comp(write_empty, page_id, output_dir,
                         'Group %s does not have raw experimental data.' % 
                         (group),
                         job_id=page_id)
                continue    

            for plot  in  sample_fullscreen_plots:
  
                job_id = '%s-%s-%s' % (sample, configuration, plot.id)
                
                job = comp(wrap_sample_saccades_plot, options.data,
                         sample, configuration, plot.command, plot.args,
                         job_id=job_id)    
                    
                page_id = '%s.%s.%s' % (sample, configuration, plot.id)
                comp(write_report, job, output_dir, page_id,
                     job_id=job_id + '-write_report')

    
    comp(create_gui,
         filename=os.path.join(output_dir, 'sample_fullscreen_plots.html'),
         menus=[
            ('Sample', all_samples, all_samples),
            ('Detector', configurations, configurations),
            ('Plot/table', map(lambda x:x.id, sample_fullscreen_plots),
                           map(lambda x:x.description, sample_fullscreen_plots))
        ])
    
    tabs = [
        
        ("group_plots", "By group",
         "This set displays one plot/table for each group of samples. "
         "You have the further choice of detection algorithm and plot/table to display."),
        
        ("saccade_plots", "By sample",
         "This set displays one plot/table for each individual sample. "
         "You have the further choice of which group to consider, which " 
         "detection algorithm, and which plot/table to display."),
        
        ("expdata_plots", "By sample (raw)",
         "This set displays one plot/table for each individual sample, "
         " produced from the raw data (no saccade detection, so no choice of detector). "
         "You have the further choice of which group to consider, " 
         "and which plot/table to display."
         " Note that some samples might be missing; for example, we don't use "
         " raw orientation data for the Mamarama samples."),
        
        ("sample_fullscreen_plots", "By sample, single page",
         "This set displays one entire page for each sample. "
         "You have the further choice of sample, " 
         "detection algorithm, and which plot/table to display."),
    ]
    
    
    comp(create_main_gui, tabs, filename=os.path.join(output_dir, 'main.html'))
     
    if options.interactive:
        # start interactive session
        compmake_console()
    else:
        # batch mode
        # try to do everything
        batch_command('make all')
        # start the console if we are not done
        # (that is, make all failed for some reason)
        todo = list(parse_job_list('todo')) 
        if todo:
            print('Still %d jobs to do.' % len(todo))
            sys.exit(-2)

     
extra_css = """
h { display: none !important; }

.report-figure, .report-node {
    border: 0 !important;
}   
.datanode { display: none !important; }

div.textnode span.textid { display: none; }
div.textnode { max-width: 40em; }
"""

def combine_reports(subs, descs, page_id, output_dir):
    r = Report(page_id)
    comp(combine_reports, subs, page_id)
    
    # look if we have a description
    if 'description' in subs[0].childid2node:
        description = subs[0].childid2node['description']
        r.add_child(description)
    
    for example_node in subs[0].children:
        plot_id = example_node.id
        if plot_id == 'description':
            continue

        if isinstance(example_node, Table):
            
            for i, sub in enumerate(subs):
                node = sub.childid2node[plot_id] 
                node.id = None
                node.caption = descs[i]
                r.add_child(node)
            
        else: # images -> use figures
            
            f = r.figure(example_node.id, shape=(5, 4))
            for i, sub in enumerate(subs):
                node = sub.childid2node[plot_id]
                node.id = None
                r.add_child(node)
                f.sub(node.id, caption=descs[i])
    
    
    resources_dir = os.path.join(output_dir, 'images')
    filename = os.path.join(output_dir, "%s.html" % page_id)
    print "Writing to %s" % filename
    r.to_html(filename, resources_dir, extra_css=extra_css)

def write_empty(page_id, output_dir, reason):
    filename = os.path.join(output_dir, "%s.html" % page_id)
    print "Writing to %s" % filename
    with open(filename, 'w') as f:
        f.write("""
<html>
<head><title>Not available</title>
<style type="text/css">
p { font-weight: bold; text-align: center; }
span { font-family: monospace; }
</style>
</head>
<body>
    <p> Page <span>%s</span> not available: %s </p>
</body>
</html>
""" % (page_id, reason))
    
     
def write_report(report, output_dir, page_id):
    # very important, otherwise images are in the same ns
    report.id = page_id
    filename = os.path.join(output_dir, page_id + '.html')
    resources_dir = os.path.join(output_dir, 'images')
    print "Writing to %s" % filename
    report.to_html(filename, resources_dir, extra_css=extra_css)
    
def wrap_group_plot(data_dir, group, configuration, plot_func, function_args):
    """  def plot_func(group, configuration, saccades) """
    db = read_samples_db(data_dir)
    saccades = db.get_saccades_for_group(group, configuration)
    return plot_func(group, configuration, saccades, **function_args)

def wrap_sample_saccades_plot(data_dir, sample, configuration,
                               plot_func, function_args):
    """  def plot_func(sample, configuration, exp_data, saccades) """
    db = read_samples_db(data_dir)
    if db.has_experimental_data(sample):
        exp_data = db.get_experimental_data(sample)
    else:
        exp_data = None
    saccades = db.get_saccades_for_sample(sample, configuration)
    return plot_func(sample, exp_data, configuration, saccades, **function_args)

def wrap_sample_expdata_plot(data_dir, sample, plot_func, function_args):
    """  def plot_func(sample, exp_data) """
    db = read_samples_db(data_dir)
    exp_data = db.get_experimental_data(sample)
    return plot_func(sample, exp_data, **function_args)


if __name__ == '__main__':
    main()
