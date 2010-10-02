import os
import pickle
from saccade_analysis import logger
from geometric_saccade_detector.io import saccades_read_mat
import numpy
datasets_description = '''
Dananassae:
   species: D. Ananassae
   experiment: tethered
   version: use_for_report  
Dmelanogaster:
   species: D. Melanogaster
   experiment: tethered
   version: use_for_report
Dmojavensis:
   species: D. Mojavensis
   experiment: tethered
   version: use_for_report
Dpseudoobscura:
   species: D. Pseudoobscura
   experiment: tethered
   version: use_for_report
Dhydei:
   species: D. Mojavensis
   experiment: tethered
   version: use_for_report
mamarama:
   species: D. Melanogaster
   experiment: mamarama
   description: All mamarama data.
   version: use_for_report
mamaramanoposts:
   species: D. Melanogaster
   experiment: mamarama
   description: Logs without posts.
   version: use_for_report
mamaramaposts:
   species: D. Melanogaster
   experiment: mamarama
   description: Logs with posts.
   version: use_for_report
''' 

def load_datasets(data_dir='.'):
    cache = os.path.join(data_dir, 'datasets.pickle')
    if os.path.exists(cache):
        logger.info('Using cache %s' % cache)
        datasets = pickle.load(open(cache))
        for name, data in datasets.items():
            add_sample_num(data['saccades'])
        return datasets
    
    import yaml
    datasets = yaml.load(datasets_description)

    for name, info in datasets.items():
        use = info['version']
        filename = os.path.join(data_dir, name, 'processed', use, 'saccades.mat')
        
        logger.info('Reading from file %s.' % filename)
        saccades = saccades_read_mat(filename)
        
        add_sample_num(saccades)
            
        info['saccades'] = saccades
    
    
    logger.info('Writing cache %s' % cache)
    pickle.dump(datasets, open(cache, 'w'))

    return datasets


def add_sample_num(saccades):
    ''' Computs the ``sample_num`` based on the ``sample`` field. '''
    samples = sorted(numpy.unique(saccades['sample']))
    for i, sample in enumerate(samples):
        which = saccades['sample'] == sample
        saccades['sample_num'][ which] = i 


