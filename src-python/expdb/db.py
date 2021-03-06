import os
import cPickle
import scipy.io
import numpy 
from geometric_saccade_detector.io import saccades_read_mat
from expdb.natsort import natsorted
import shelve
import pickle
from flydra_db  import FlydraDB

class Group:
    def __init__(self):
        self.samples = set()
        # configuration -> saccades.mat file
        self.configurations = {}
        self.has_experimental_data = False

class SamplesDB:
    
    def __init__(self, data, verbose=False):
        ''' data: base directory '''
        
        if not os.path.exists(data) or not os.path.isdir(data):
            raise Exception('Could not open directory %s' % data)
        
        self.data = data
        
        # self.use_cache = True
        self.use_cache = False
        self.use_flydra_db = True
         
        
        if self.use_cache:
            self.open_shelve()
        
        if self.use_flydra_db:
            self.open_flydra_db()
            
        
        self.groups = {}
        
        #self.group2samples = {}
        # maps id to .mat file
        self.sample2expmat = {}
        # maps id to .pickle file
        self.sample2exppickle = {}
        # list of all configurations
        self.configurations = set()
        # maps sample -> group
        self.sample2group = {}
        
        #print "Loading data in %s" % data
        
        for group in os.listdir(data):
            group_dir = os.path.join(data, group)
            if not os.path.isdir(group_dir):                
                continue
            
            # print "Reading group %s" % group
            group_record = Group()
            
            for file in [file for file in os.listdir(group_dir) 
                if file.startswith('data_') and file.endswith('.mat')]:
                id = file[5:-4]
                group_record.samples.add(id)
                self.sample2expmat[id] =  os.path.join(group_dir,file)
                self.sample2group[id] = group
                
                
            for file in [file for file in os.listdir(group_dir) 
                if file.startswith('data_') and file.endswith('.pickle')]: 
                id = file[5:-7]
                group_record.samples.add(id)
                self.sample2exppickle[id] = os.path.join(group_dir,file)
                self.sample2group[id] = group

            group_record.has_experimental_data = len(group_record.samples) > 0
            
            
            processed_dir = os.path.join(group_dir, 'processed')
            if not os.path.exists(processed_dir):
                if verbose:
                    print "No processed data found for %s." % group
                pass
                
            else:
                for conf in os.listdir(processed_dir):                
                    saccades = os.path.join(processed_dir, conf, 'saccades.mat')
                    if os.path.exists(saccades): 
                        group_record.configurations[conf] = saccades
                        # add to general list
                        self.configurations.add(conf)
#                    else:
#                        conf_dir = os.path.join(processed_dir, conf)
#                        for file in [file for file in os.listdir(conf_dir) 
#                            if file.startswith('processed_data_') and file.endswith('.mat')]: 
#                                  id = file[5:-7]

                # if we don't have exp data, get list of samples from
                # processed data
                if group_record.configurations and \
                    not group_record.has_experimental_data:
                    saccades = saccades_read_mat(saccades)
                    group_record.samples = set(numpy.unique(saccades['sample']))
                    for sample in group_record.samples:
                        self.sample2group[sample] = group

            if len(group_record.samples)> 0:
                self.groups[group] = group_record
                    
                print "has it", group, group_record.has_experimental_data
            
    def open_shelve(self):
        shelve_fname = os.path.join(self.data, 'shelve')
        self.shelve = shelve.open(shelve_fname, protocol=pickle.HIGHEST_PROTOCOL)
    
    def open_flydra_db(self):
        self.flydra_db = FlydraDB(os.path.join(self.data, 'sac_flydra_db'))
        
    def list_groups(self):
        """ Returns a list of the groups. """
        return natsorted(list(self.groups.keys()))
    
    def list_all_samples(self):
        """ Returns a list of all samples for all groups. """
        return natsorted(list(self.sample2group.keys()))
    
    def list_samples(self, group):
        """ Lists the samples in the given group. """
        return natsorted(list(self.groups[group].samples))
    
    def list_all_configurations(self):
        """ Lists all the configurations present in the data. """
        return natsorted(self.configurations)
        
    def list_configurations(self, group):
        """ Lists the configurations for the given group. """
        return natsorted(list(self.groups[group].configurations.keys()))
    
    def get_group_for_sample(self, sample):
        """ Returns the sample associated to the group. """
        return self.sample2group[sample]
    
    def get_saccades_for_group(self, group, configuration):
        """ Returns the saccades for the given group and configuration. 
            If configuration is not passed, we use the default.
        """
        if self.use_flydra_db:
            table = 'groupsaccades_%s' % configuration
            if self.flydra_db.has_sample(group) and \
               self.flydra_db.has_table(group, table):
                t = self.flydra_db.get_table(group, table)
                #value = t.copy()
                value = t
                #self.flydra_db.release_table(t)
                return value 
            
        if self.use_cache:
            key = str(('get_saccades_for_group', group, configuration))
            if key in self.shelve:
                return self.shelve[key]
    
        filename = self.groups[group].configurations[configuration]
        saccades = saccades_read_mat(filename)
        
        
        if self.use_flydra_db:
            if not self.flydra_db.has_sample(group):
                self.flydra_db.add_sample(group)
            self.flydra_db.set_table(group, table, saccades)
            
        if self.use_cache:
            self.shelve[key] = saccades
            
        return saccades
    
    def group_has_experimental_data(self, group):
        """ Returns true if this group has the raw orientation data.
            (mamarama has only saccades data. ) """
        return self.groups[group].has_experimental_data
    
    def has_experimental_data(self, sample):
        """ Returns true if this sample has the raw orientation data. """
        return sample in self.sample2expmat or sample in self. sample2exppickle

    def get_saccades_for_sample(self, sample, configuration):
        """ Returns the saccades for the given group and configuration. 
            If configuration is not passed, we use the default.
        """
        if self.use_flydra_db:
            table = 'saccades_%s' % configuration
            if self.flydra_db.has_sample(sample) and \
               self.flydra_db.has_table(sample, table):
                t = self.flydra_db.get_table(sample, table)
                #value =  t.copy()
                value = t
                #self.flydra_db.release_table(t)
                return value 
            
        if self.use_cache:
            key = str(('get_saccades_for_sample', sample, configuration))
            if key in self.shelve:
                return self.shelve[key]
    
        group = self.get_group_for_sample(sample)
        group_saccades  = self.get_saccades_for_group(group, configuration) 

        print group_saccades[0].dtype
#        with open('tmp.pickle','w') as f:
#            pickle.dump(f, group_saccades)        
        mine = group_saccades[:]['sample'] == sample
        
        saccades = group_saccades[mine]
        
        if len(saccades) == 0:
            raise Exception('No saccades found for %s' % sample)
        
        
        if self.use_flydra_db:
            if not self.flydra_db.has_sample(sample):
                self.flydra_db.add_sample(sample)

            self.flydra_db.set_table(sample, table, saccades)
            
        if self.use_cache:
            self.shelve[key] = saccades
        
        return saccades
        
    def get_experimental_data(self, sample):
#        if self.use_flydra_db:
#            table = 'tethered_data'
#            if self.flydra_db.has_sample(sample) and \
#               self.flydra_db.has_table(sample, table):
#                t = self.flydra_db.get_table(sample, table)
#                #value =  t.copy()
#                value = t
#                #self.flydra_db.release_table(t)
#                return value 
#        
        if self.use_cache:
            if sample in self.shelve:
                return self.shelve[sample]
                
        if sample in self.sample2expmat:
            data = scipy.io.loadmat(self.sample2expmat[sample], squeeze_me=True)
            data = data['data']
            # convert from array to hash
            assert isinstance(data, numpy.ndarray)
            data = dict(map(lambda field: (field, data[field]), data.dtype.fields))
            # convert from array to string
            for k in list(data.keys()):
                if data[k].dtype.char == 'U':
                    data[k] = str(data[k])
                
            # make sure everything is 1d array
            def as1d(x):  
                if x.dtype == 'object':
                    x = x.tolist()
                return x.reshape(len(x))
            data['exp_orientation'] = as1d(data['exp_orientation'])
            data['exp_timestamps'] = as1d(data['exp_timestamps'])
            
        elif sample in self.sample2exppickle:
            with open(self.sample2exppickle[sample], 'rb') as f:
                data = cPickle.load(f)      
            
        else:
            raise Exception('no data for sample %s found' % sample)
        
#        if self.use_flydra_db:
#            if not self.flydra_db.has_sample(sample):
#                self.flydra_db.add_sample(sample)
#
#            self.flydra_db.set_table(sample, table, data)
            
        if self.use_cache:
            self.shelve[sample] = data
        
        return data
    
    def __getstate__(self):
        # do not pickle the shelve
        all = dict(self.__dict__)
        all['shelve'] = None
        all['flydra_db'] = None
        return all
        
def read_samples_db(data, verbose=False, rescan=False):
    cache = os.path.join(data, 'index.pickle')
    if os.path.exists(cache) and not rescan:
        # print "Using cache %s" % cache
        db = cPickle.load(open(cache))
        # reopen shelve if it was used
        if db.use_cache:
            db.open_shelve()
        if db.use_flydra_db:
            db.open_flydra_db()
        return db
    else:
        db = SamplesDB(data, verbose)
        # print "Writing to cache %s" % cache
        with open(cache, 'wb') as f:
            cPickle.dump(db, f)   
        return db
    
    