import os
import cPickle
import scipy.io
import numpy 
from geometric_saccade_detector.io import saccades_read_mat
from expdb.natsort import natsorted



class SamplesDB:
    
    def __init__(self, data, verbose=False):
        ''' data: base directory '''
        
        if not os.path.exists(data) or not os.path.isdir(data):
            raise Exception()
        
        self.data = data
        self.group2samples = {}
        # maps id to .mat file
        self.sample2expmat = {}
        # maps id to .pickle file
        self.sample2exppickle = {}
        # maps id to actual loaded data (cached
        self.sample2exp = {}
        # maps group -> list of configurations
        self.group2configurations = {}
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
            
            self.group2samples[group] = set()
            
            for file in [file for file in os.listdir(group_dir) 
                if file.startswith('data_') and file.endswith('.mat')]:
                id = file[5:-4]
                self.group2samples[group].add(id)
                self.sample2expmat[id] =  os.path.join(group_dir,file)
                self.sample2group[id] = group
                
            for file in [file for file in os.listdir(group_dir) 
                if file.startswith('data_') and file.endswith('.pickle')]: 
                id = file[5:-7]
                self.group2samples[group].add(id)
                self.sample2exppickle[id] = os.path.join(group_dir,file)
                self.sample2group[id] = group

        
            if not self.group2samples[group]:
                # print 'Empty group "%s".' % group
                del self.group2samples[group]
                
            self.group2configurations[group] = {}
            
            processed_dir = os.path.join(group_dir, 'processed')
            if not os.path.exists(processed_dir):
                if verbose:
                    print "No processed data found for %s." % group
                pass
                
            else:
                for conf in os.listdir(processed_dir):                
                    saccades = os.path.join(processed_dir, conf, 'saccades.mat')
                    if os.path.exists(saccades): 
                        self.group2configurations[group][conf] = saccades
                    
                        # add to general list
                        self.configurations.add(conf)
                
    
    def list_groups(self):
        return natsorted(list(self.group2samples.keys()))
    
    def list_samples(self, group):
        return natsorted(list(self.group2samples[group]))
    
    def list_all_configurations(self):
        return natsorted(self.configurations)
        
    def list_configurations(self, group):
        """ Lists the configurations for the given group. """
        return natsorted(list(self.group2configurations[group].keys()))
    
    def get_group_for_sample(self, sample):
        """ Returns the sample associated to the group. """
        return self.sample2group[sample]
    
    def get_saccades_for_group(self, group, configuration):
        """ Returns the saccades for the given group and configuration. 
            If configuration is not passed, we use the default.
        """
        filename   = self.group2configurations[group][configuration]
        return saccades_read_mat(filename)

    def get_saccades_for_sample(self, sample, configuration):
        """ Returns the saccades for the given group and configuration. 
            If configuration is not passed, we use the default.
        """
        group = self.get_group_for_sample(sample)
        group_saccades  = self.get_saccades_for_group(group, configuration) 
        
        mine = group_saccades['sample'] == sample
        
        saccades = group_saccades[mine]
        
        if len(saccades) == 0:
            raise Exception('No saccades found for %s' % sample)
        
        return saccades
        
    def get_experimental_data(self, sample):
        if sample in self.sample2exp:
            return self.sample2exp[sample]
        
                
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
        
        # cache disabled
        # self.sample2exp[sample] = data
        
        return data
        