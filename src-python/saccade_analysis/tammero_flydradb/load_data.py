import numpy as np
from contracts import contract 
from flydra_db import safe_flydra_db_open

from geometric_saccade_detector.well_formed_saccade import check_saccade_is_well_formed
from ..tammero.tammero_analysis import add_position_information
from . import logger

@contract(interval='tuple( (>=0, a), >a )')
def get_saccades(flydra_db_directory, db_group, interval):
    
    with safe_flydra_db_open(flydra_db_directory) as db:
        
        saccades = db.get_table_for_group(db_group, 'saccades')
        logger.info('Found %d saccades for group %r.' % (len(saccades), db_group))
        if len(saccades) == 0:
            raise Exception('No saccades found for group %r.' % db_group)
           
        # make sure we use array
        saccades = np.array(saccades)
        
        for s in saccades:
            check_saccade_is_well_formed(s)
            
        saccades = add_position_information(saccades) # XXX: using default arena size
       
       
        def test(saccade):
            return (saccade['distance_from_wall'] >= interval[0] and
                    saccade['distance_from_wall'] <= interval[1])
        include = map(test, saccades)
        select = saccades[np.array(include)]
    
        logger.info(' of which %d saccades are in interval %g <= d <= %g.' % 
                    (len(select), interval[0], interval[1]))
        
        if len(select) == 0:
            raise Exception('No saccades in interval %g <= d <= %g' %
                            interval )
      
        return select