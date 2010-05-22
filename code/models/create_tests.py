import numpy

class Saccade:
    def __init__(self, time_passed, time_start, duration, sign):
        ''' Sign: +/- 1
           Interval: time since last saccade. '''
           
        assert time_passed > 0
        assert duration > 0
        assert sign == -1 or sign == +1
        
        self.time_passed = time_passed
        self.time_start = time_start
        self.duration = duration
        self.time_stop = self.time_start + duration 
        self.sign = sign
        
    def __str__(self):
        return '<Saccade time_start=%.3f time_passed=%.3f  duration=%.3f sign=%s>' % \
            (self.time_start, self.time_passed, self.duration, self.sign)

def saccades_to_ndarray(saccades, species='model', sample='0'):
    ''' Converts an iterable containing saccade objects to a ndarray '''
    saccades = list(saccades)
    dtype = [('time_start', 'float64'),
             ('time_passed', 'float64'),
             ('time_stop', 'float64'),
             ('duration', 'float64'),
             ('sign', 'int'),
             ('amplitude', 'float64'),
             ('orientation_start', 'float64'),
             ('orientation_stop', 'float64'),
             ('top_velocity', 'float64'),
             ('species', 'S32'),
             ('sample', 'S32')] 
             
    shape = len(saccades)
    a = numpy.ndarray(shape=shape, dtype=dtype)
    for i, saccade in enumerate(saccades):
        a[i]['time_start'] = saccade.time_start
        a[i]['time_passed'] = saccade.time_passed
        a[i]['time_stop'] = saccade.time_stop
        a[i]['duration'] = saccade.duration
        a[i]['sign'] = saccade.sign 
        a[i]['amplitude'] = 90
        a[i]['orientation_start'] = 0
        a[i]['orientation_stop'] = 0
        a[i]['top_velocity'] = 1
        a[i]['species'] = species
        a[i]['sample'] = sample
        
        
    return a


class SaccadeSequenceGenerator:
    ''' Interface for saccade sequence generator'''
    def sample_saccade(self, time_interval):
        ''' Returns a list of Saccade objects '''
        raise TypeError, 'Implement this function'

    def sample_saccade_sequence(self, time_interval):
        ''' Samples a sequence of saccades up until the given time interval'''
        last_saccade = None
        while True:
            saccade = self.sample_saccade()
            if last_saccade is not None:
                A = last_saccade.time_stop + saccade.time_passed
                B = saccade.time_start
                msg = "I was expecting %s = time_stop %s + time_passed %s = time_start %s. \n%s\n%s " % \
                    (last_saccade.time_stop + saccade.time_passed, last_saccade.time_stop, saccade.time_passed, saccade.time_start,
                     last_saccade, saccade)
                
                assert abs(A - B) < 1e-4, msg
            if saccade.time_stop > time_interval:
                break
            
            last_saccade = saccade
            #print saccade
            yield saccade
            


class Uniform:
    def __init__(self, min, max):
        self.min = min
        self.max = max
        
    def sample(self):
        return self.min + (self.max - self.min) * numpy.random.rand()

class BernouilliSign:
    def __init__(self, prob_plus):
        self.prob_plus = prob_plus
        
    def sample(self):
        sample = numpy.random.binomial(n=1, p=self.prob_plus)
        if sample > 0:
            return + 1
        else:
            return - 1

class Exponential:
    def __init__(self, rate):
        self.rate = rate
        
    def sample(self):
        return numpy.random.exponential(scale=1.0 / self.rate)

# Model: crossing of a barrier + hard reset
# Parameters: gaussian noise, threshold (probably not independent)
#...

# Model: sample from exponential (maybe implemented by something else)
#   that is, poisson process
#...

# Model: 


# Sign generators

class IndependentModel(SaccadeSequenceGenerator):
    ''' This model generates saccades using two independent
        generators for the interval and for the sign '''
    def __init__(self, interval, sign, duration):
        self.interval = interval
        self.sign = sign
        self.duration = duration
        # end of the saccade
        self.end_of_last_saccade = 0
        
    def sample_saccade(self):
        
        time_passed = self.interval.sample()
        sign = self.sign.sample() 
        duration = self.duration.sample()
        
        time_start = self.end_of_last_saccade + time_passed
        
        saccade = Saccade(time_passed=time_passed, sign=sign,
                       time_start=time_start, duration=duration)

        self.end_of_last_saccade = time_start + duration        
        
        return saccade

class ParallelIndependentModel(SaccadeSequenceGenerator):
    ''' This model generates saccades using two independent
        generators for left and right saccades.
    '''
    def __init__(self, left, right, duration):
        self.left = left
        self.right = right
        self.duration = duration
        
        left_next_interval = self.left.sample()
        self.left_next_time = left_next_interval
        right_next_interval = self.right.sample()
        self.right_next_time = right_next_interval     
        self.last_time = 0
        
    def sample_saccade(self):
        if self.left_next_time < self.right_next_time:
            time_start = self.left_next_time
            interval = self.left_next_time - self.last_time 
            assert interval > 0
            sign = +1
            duration = self.duration.sample() 
            assert duration > 0        
            
            left_next_interval = self.left.sample()
            assert  left_next_interval > 0 
            self.left_next_time += duration + left_next_interval 
        else:
            time_start = self.right_next_time
            interval = self.right_next_time - self.last_time
            assert interval > 0
            sign = -1
            duration = self.duration.sample() 
            assert duration > 0
        
            right_next_interval = self.right.sample()
            assert  right_next_interval > 0
            self.right_next_time += duration + right_next_interval
                     
        saccade = Saccade(time_passed=interval, duration=duration, sign=sign,
                          time_start=time_start)
        
        self.last_time = time_start + duration
        
        if self.last_time > self.left_next_time:
            self.left_next_time = self.last_time + self.left.sample() 

        if self.last_time > self.right_next_time:
            self.right_next_time = self.last_time + self.right.sample()
             
        return saccade


class ParallelModel(SaccadeSequenceGenerator):
    ''' This model generates saccades using two 
        generators for left and right saccades
        that influence each other `
    '''
    def __init__(self, left, right, duration, same_effect, other_effect):
        '''
            left and right must be two dict with keys -1,0,1, indicating
            which generator to use when excited,normal,inhibited
            
            same_effect: -1,0,1  the effect on itself
            other_effect: -1,0,1 the effect on the other side
        '''
        assert same_effect in [-1, 0, 1]
        assert other_effect in [-1, 0, 1]
        self.same_effect = same_effect
        self.other_effect = other_effect
        
        assert isinstance(left, dict)
        assert (-1 in left) and (0 in left) and (+1 in left)
        assert isinstance(right, dict) 
        assert (-1 in right) and (0 in right) and (+1 in right)
        
        self.duration = duration

        self.signs = [-1, +1]
        self.generators = [right, left]
        self.last_side = 0 # arbitrary 
        
        self.next_time = [0, 0]
        
        self.last_time = 0
        for side in [0, 1]:
            which_one = self.which_should_I_use(side=side)
            self.next_time[side] = self.generators[side][which_one].sample() 
            
        
    def which_should_I_use(self, side):
        ''' returns -1,0,1 meaning the inhibition status of side '''
        if self.last_side == side:
            effect = self.same_effect 
        else:
            effect = self.other_effect
        return effect
        
    def sample_saccade(self):
        # we generate the saccade that comes first
        side = self.next_time.index(min(self.next_time))
        
        time_start = self.next_time[side]
        interval = time_start - self.last_time
        assert interval > 0, 'last: %.3f  start: %.3f' % (self.last_time, time_start) 
        
        sign = self.signs[side]
        duration = self.duration.sample()
        
        saccade = Saccade(time_passed=interval, duration=duration, sign=sign,
                          time_start=time_start)
        
        self.last_time = time_start + duration
        self.last_side = side

        # compute next one
        which_one = self.which_should_I_use(side=side)
        self.next_time[side] = time_start + duration + \
            self.generators[side][which_one].sample()
            
        
        # this is the other side
        other_side = 1 - side
        
        # make sure they don't overlap
        if self.last_time > self.next_time[other_side]:
            which_one = self.which_should_I_use(side=other_side)
            self.next_time[other_side] = time_start + duration + \
                self.generators[other_side][which_one].sample()

             
        return saccade
        
