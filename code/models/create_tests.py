
class Saccade:
    def __init__(self, interval, sign):
        self.interval = interval
        self.sign = sign

class SaccadeSequenceGenerator:
    ''' Interface for saccade sequence generator'''
    def generate_sequence(time_interval):
        ''' Returns a list of Saccade objects '''
        raise TypeError, 'Implement this function'

# Single-generators models
#   For these models, we assume

# Time generators:
class SaccadeIntervalGenerator:

# Model: crossing of a barrier + hard reset
# Parameters: gaussian noise, threshold (probably not independent)
...

# Model: sample from exponential (maybe implemented by something else)
#   that is, poisson process
...

# Model: 


# Sign generators

class IndependentModel(SaccadeSequenceGenerator):
    def __init__(self, interval_generator, sign_generator):
        self.interval_generator = interval_generator
        self.sign_generator = sign_generator
        
    def generate_sequence(time_interval):
        current_time = 0
        
        pass



        