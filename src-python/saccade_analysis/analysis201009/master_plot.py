import sys, os 
from optparse import OptionParser

from reprep import Report
from reprep.table import Table
from compmake  import set_namespace, comp, compmake_console, batch_command
from compmake.jobs.syntax.parsing import parse_job_list

from expdb.db import SamplesDB, read_samples_db
# The various plots
from saccade_analysis.analysis201009.master_plot_gui import create_gui,\
    create_main_gui
from saccade_analysis.analysis201009.master_plot_vars import variables
from saccade_analysis.analysis201009.stats import \
    fairness,  independence,  levy_exp, plot_raw_trajectories, \
    plot_simulated_sample_trajectories, group_sign_xcorr, group_sign_hist, \
    plot_detected_saccades, sample_var_hist,group_var_xcorr,group_var_hist



group_plots = [
    ('sign_hist', group_sign_hist, {}),
    ('sign_xcorr', group_sign_xcorr, {}), 
    ('fairness', fairness, {}),
    ('independence', independence, {}),
    ('levy_vs_exp', levy_exp, {})
]

for var in variables:
    group_plots.append(('xcorr_%s' % var.id, group_var_xcorr, {'variable': var}))
    group_plots.append(('hist_%s' % var.id, group_var_hist, {'variable': var}))
    
sample_expdata_plots = [
    ('raw_trajectories', plot_raw_trajectories, {}),
]

sample_saccades_plots = [
    ('simulated_trajectories', plot_simulated_sample_trajectories, {}),
]

for var in variables:
    sample_saccades_plots.append(
        ('hist_%s' % var.id, sample_var_hist, {'variable': var}))

sample_fullscreen_plots = [
    ('saccade_detection', plot_detected_saccades, {})
]

description = """ Main function to plot everything. """
 
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
        configurations =options.configurations.split(', ')
        confset = "_".join(configurations)
    else:
        configurations = db.list_all_configurations()
        confset = "all"
        
    combination = '%s_%s' % (groupset, confset)
    output_dir = os.path.join(options.report, combination)
    
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
            
            for id, function, function_args in group_plots:
                job_id = '%s-%s-%s' % (group, configuration, id)
                
                index_group_plots[(group,configuration,id)] = \
                    comp(wrap_group_plot, options.data, group, 
                         configuration, function,function_args,
                         job_id=job_id)    

            for sample in db.list_samples(group):
                for id, function, function_args  in sample_saccades_plots:
                    job_id = '%s-%s-%s' % (sample, configuration, id)
                    index_sample_saccades_plots[(sample,configuration,id)] = \
                        comp(wrap_sample_saccades_plot, options.data, 
                             sample, configuration, function,function_args,
                             job_id=job_id)    

        if db.group_has_experimental_data(group):
            for sample in db.list_samples(group):
                for id, function, function_args  in sample_expdata_plots:
                    job_id = '%s-%s' % (sample,  id)
                    index_sample_expdata_plots[(sample,id)] = \
                        comp(wrap_sample_expdata_plot, options.data, 
                             sample,  function,function_args, job_id=job_id)    

    # now we create the indices 
    # fix configuration, function; iterate groups
    for configuration in configurations:
        for function_id, function, function_args in group_plots:
        
            subs = []; descs = [];
        
            page_id = "%s.%s" % (configuration, function_id)
            
            for group in groups:
                if not configuration in configurations_for_group[group]:
                    continue
                
                descs.append(group)
                subs.append(index_group_plots[(group,configuration,function_id)])
        
            job_id = page_id
            comp(combine_reports, subs, descs, page_id, output_dir,
                 job_id=job_id) 
    
    comp(create_gui,
         filename=os.path.join(output_dir, 'group_plots.html'),
         menus = [
                  ('Configuration',  configurations),
                  ('Plot/table', map(lambda x:x[0], group_plots) )
        ])
    
    
    # fix group, function; iterate samples
    for group in groups:
        if db.group_has_experimental_data(group):    
            for function_id, function, function_args  in sample_expdata_plots:
                subs = []; descs = [];
                for sample in db.list_samples(group):
                    descs.append(sample)
                    subs.append(index_sample_expdata_plots[(sample,function_id)])
                    
                page_id = "%s.%s" % (group, function_id)
                
                job_id = page_id
                comp(combine_reports, subs, descs, page_id, output_dir,
                     job_id=job_id) 

    comp(create_gui,
         filename=os.path.join(output_dir, 'expdata_plots.html'),
         menus = [
                  ('Group',  groups), 
                  ('Plot/table', map(lambda x:x[0], sample_expdata_plots) )
        ])
    
    # fix configuration, group, function; iterate samples
    for configuration in configurations:

        for group in groups:
            if not configuration in configurations_for_group[group]:
                continue
                
            for function_id, function, function_args  in  sample_saccades_plots:
                
                subs = []; descs = [];
                for sample in db.list_samples(group):
                    descs.append(sample)
                    r = index_sample_saccades_plots[(sample,configuration,
                                                     function_id)]
                    subs.append(r)
                    
                page_id = "%s.%s.%s" % (configuration,group,function_id)
                
                job_id = page_id
                comp(combine_reports, subs, descs, page_id, output_dir,
                     job_id=job_id) 

    comp(create_gui,
         filename=os.path.join(output_dir, 'saccade_plots.html'),
         menus = [
                  ('Configuration',  configurations),
                  ('Group',  groups), 
                  ('Plot/table', map(lambda x:x[0], sample_saccades_plots) )
        ])
    
    # fix configuration, sample; plot fullsscreen
    
    all_samples = db.list_all_samples()
    
    for configuration in configurations:
        for sample in all_samples:
            group = db.get_group_for_sample(sample)
            if not configuration in configurations_for_group[group]:
                #print "skipping sample %s group %s config %s" %\
                #     (sample,group, configuration)
                continue
            if not db.group_has_experimental_data(group):
                continue    

            for function_id, function, function_args  in  sample_fullscreen_plots:
  
                job_id = '%s-%s-%s' % (sample, configuration, function_id)
                
                job = comp(wrap_sample_saccades_plot, options.data, 
                         sample, configuration, function,function_args,
                         job_id=job_id)    
                    
                page_id = '%s.%s.%s' % (sample, configuration, function_id)
                comp(write_report, job, output_dir, page_id,
                     job_id=job_id+'-write_report')

    
    comp(create_gui,
         filename=os.path.join(output_dir, 'sample_fullscreen_plots.html'),
         menus = [
                  ('Sample',  all_samples),
                  ('Configuration',  configurations),                
                  ('Plot/table', map(lambda x:x[0], sample_fullscreen_plots) )
        ])
    
    
    comp(create_main_gui, filename=os.path.join(output_dir, 'main.html'))
     
    if options.interactive:
        # start interactive session
        compmake_console()
    else:
        # batch mode
        # try to do everything
        batch_command('make all')
        # start the console if we are not done
        # (that is, make all failed for some reason)
        todo = parse_job_list('todo') 
        if todo:
            print('Still %d jobs to do.' % len(todo))
            sys.exit(-2)

     
extra_css = """
h { display: none !important; }

.report-figure, .report-node {
    border: 0 !important;
}   
.datanode { display: none !important; }

"""

def combine_reports(subs, descs, page_id, output_dir):
    r = Report(page_id)
    comp(combine_reports, subs, page_id)
    
    for id, dummy in subs[0].childid2node.items():
        node = subs[0].childid2node[id]
        
        if isinstance(node, Table):
            
            for i, sub in enumerate(subs):
                node = sub.childid2node[id]
                #node.id = sub.id
                node.id = None
                r.add_child(node)
                node.caption = descs[i]
            
        else: # images -> use figures
            
            f = r.figure(id, shape=(5,4))
            for i, sub in enumerate(subs):
                node = sub.childid2node[id]
                # node.id = sub.id
                node.id = None
                r.add_child(node)
                f.sub(node.id, caption=descs[i])
    
    
    resources_dir = os.path.join(output_dir, 'images')
    filename = os.path.join(output_dir, "%s.html" % page_id)
    print "Writing to %s" % filename
    r.to_html(filename, resources_dir, extra_css=extra_css)
    
def write_report(report, output_dir, page_id):
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