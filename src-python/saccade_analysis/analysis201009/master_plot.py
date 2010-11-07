import sys 
from optparse import OptionParser

from reprep import Report
from compmake  import set_namespace, comp, compmake_console, batch_command
from compmake.jobs.syntax.parsing import parse_job_list

from expdb.db import SamplesDB
from saccade_analysis.analysis201009.plots_trajectories import plot_raw_trajectories,\
    plot_sample_hist_group, plot_simulated_sample_trajectories
import os
from saccade_analysis.analysis201009.master_plot_gui import create_gui,\
    create_main_gui


group_plots = [
    ('sample_hist_group', plot_sample_hist_group),
]

sample_expdata_plots = [
    ('raw_trajectories', plot_raw_trajectories),
]

sample_saccades_plots = [
    ('simulated_trajectories', plot_simulated_sample_trajectories),
]


description = """ Main function to plot everything. """
 
def main():
    parser = OptionParser(usage=description)
    parser.add_option("--data", help="Main data directory", default='saccade_data')
    parser.add_option("--interactive", action="store_true",default=False,
                      help="Starts an interactive compmake session.")
    parser.add_option("--report", help="Saccade report directory", 
                      default='saccade_report')
    parser.add_option("--groups", help="Which groups to consider", 
                      default=None)
    parser.add_option("--configurations", help="Which configurations to consider", 
                      default=None)
        
    (options, args) = parser.parse_args()
    
    db = SamplesDB(options.data, verbose=True)
    
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
        
    set_namespace('master_plot_%s_%s' % (groupset, confset))
        
    
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
            
            for id, function in group_plots:
                job_id = '%s-%s-%s' % (group, configuration, id)
                
                index_group_plots[(group,configuration,id)] = \
                    comp(wrap_group_plot, options.data, group, configuration, function,
                         job_id=job_id)    

            for sample in db.list_samples(group):
                for id, function in sample_saccades_plots:
                    job_id = '%s-%s-%s' % (sample, configuration, id)
                    index_sample_saccades_plots[(sample,configuration,id)] = \
                        comp(wrap_sample_saccades_plot, options.data, 
                             sample, configuration, function,
                             job_id=job_id)    

        for sample in db.list_samples(group):
            for id, function in sample_expdata_plots:
                job_id = '%s-%s' % (sample,  id)
                index_sample_expdata_plots[(sample,id)] = \
                    comp(wrap_sample_expdata_plot, options.data, 
                         sample,  function, job_id=job_id)    

    # now we create the indices
    
    output_dir = options.report
     
    # fix configuration, function; iterate groups
    for configuration in configurations:
        for function_id, function in group_plots:
        
            subs = []; descs = [];
        
            page_id = "%s.%s" % (configuration, id)
            
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
        for id, function in sample_expdata_plots:
            subs = []; descs = [];
            for sample in db.list_samples(group):
                descs.append(sample)
                subs.append(index_sample_expdata_plots[(sample,id)])
                
            page_id = "%s.%s" % (group, id)
            
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
                
            for id, function in  sample_saccades_plots:
                
                subs = []; descs = [];
                for sample in db.list_samples(group):
                    descs.append(sample)
                    r = index_sample_saccades_plots[(sample,configuration,id)]
                    subs.append(r)
                    
                page_id = "%s.%s.%s" % (configuration,group,id)
                
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

 
def combine_reports(subs, descs, page_id, output_dir):
    r = Report(page_id)
    comp(combine_reports, subs, page_id)
    
    for id, dummy in subs[0].childid2node.items():
        f = r.figure(id, shape=(5,4))
        
        for i, sub in enumerate(subs):
            node = sub.childid2node[id]
            node.id = sub.id
            r.add_child(node)
            f.sub(node.id, caption=descs[i])
    
    
    resources_dir = os.path.join(output_dir, 'images')
    filename = os.path.join(output_dir, "%s.html" % page_id)
    print "Writing to %s" % filename
    r.to_html(filename, resources_dir)
                    
def wrap_group_plot(data_dir, group, configuration, plot_func):
    """  def plot_func(group, configuration, saccades) """
    db = SamplesDB(data_dir)
    saccades = db.get_saccades_for_group(group, configuration)
    return plot_func(group, configuration, saccades)

def wrap_sample_saccades_plot(data_dir, sample, configuration, plot_func):
    """  def plot_func(sample, configuration, exp_data, saccades) """
    db = SamplesDB(data_dir)
    exp_data = db.get_experimental_data(sample)
    saccades = db.get_saccades_for_sample(sample, configuration)
    return plot_func(sample, exp_data, configuration, saccades)

def wrap_sample_expdata_plot(data_dir, sample, plot_func):
    """  def plot_func(sample, exp_data) """
    db = SamplesDB(data_dir)
    exp_data = db.get_experimental_data(sample)
    return plot_func(sample, exp_data)


if __name__ == '__main__':
    main()