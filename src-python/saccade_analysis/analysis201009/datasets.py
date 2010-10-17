import os
import cPickle as pickle
from saccade_analysis import logger
from geometric_saccade_detector.io import saccades_read_mat
import numpy
datasets_description = '''
---
id: Dmojavensis
species: D. Mojavensis
experiment: tethered
version: use_for_report
---
id: Dhydei
species: D. Hydei
experiment: tethered
version: use_for_report
---
id: Dmelanogaster
species: D. Melanogaster
experiment: tethered
version: use_for_report
---
id: Dpseudoobscura
species: D. Pseudoobscura
experiment: tethered
version: use_for_report
---
id: Darizonae
species: D. Arizonae
experiment: tethered
version: use_for_report
---
id: Dananassae
species: D. Ananassae
experiment: tethered
version: use_for_report  
---
id: mamaramanoposts
species: D. Melanogaster
experiment: mamarama
description: Logs without posts.
version: use_for_report
---
id: mamaramaposts
species: D. Melanogaster
experiment: mamarama
description: Logs with posts.
version: use_for_report
#---
#id: mamarama
#species: D. Melanogaster
#experiment: mamarama
#description: All mamarama data.
#version: use_for_report
''' 

def load_datasets(data_dir='.'):
    cache = os.path.join(data_dir, 'datasets.pickle')
    if os.path.exists(cache):
        logger.info('Using cache %s' % cache)
        datasets = pickle.load(open(cache)) 
        return datasets
    
    import yaml
    datasets = list(yaml.load_all(datasets_description))

    for dataset in datasets:
        id = dataset['id']
        version = dataset['version']
        filename = os.path.join(data_dir, id, 'processed', version, 'saccades.mat')
        
        logger.info('Reading from file %s.' % filename)
        saccades = saccades_read_mat(filename)
        
        add_sample_num(saccades)
            
        dataset['saccades'] = saccades
    
    
    logger.info('Writing cache %s' % cache)
    pickle.dump(datasets, open(cache, 'w'))

    return datasets


def add_sample_num(saccades):
    ''' Computs the ``sample_num`` based on the ``sample`` field. '''
    samples = sorted(numpy.unique(saccades['sample']))
    for i, sample in enumerate(samples):
        which = saccades['sample'] == sample
        saccades['sample_num'][ which] = i 


