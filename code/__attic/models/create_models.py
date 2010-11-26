from models import IndependentModel, BernouilliSign, Exponential, \
    ParallelIndependentModel, Uniform, ParallelModel
from numpy import array
from markov import Markov



def create_models():
        
    models = []
    
    
    interval_generator = Exponential(1)
    sign_generator = BernouilliSign(0.5)
    duration = Uniform(0.1, 0.2)
    basic = IndependentModel(interval_generator, sign_generator, duration)
    
    models.append(('basic', basic))
    
    
    left_generator = Exponential(1)
    right_generator = Exponential(1)
    duration = Uniform(0.1, 0.2)
    parallel = ParallelIndependentModel(left_generator, right_generator, duration)
    
    
    models.append(('parallel_indep', parallel))
    
    
    generators = {
        + 1: Exponential(4),
         0: Exponential(1),
        - 1: Exponential(0.25)
    } 
    
    for same in [-1, 0, +1]:
        for other in [-1, 0, +1]:
            duration = Uniform(0.1, 0.2)
            model = ParallelModel(left=generators, right=generators,
                                  duration=duration,
                                  same_effect=same, other_effect=other)
    
            names = {-1:'I', 0:'N', +1:'E'}
            name = 'par%s%s' % (names[same], names[other])
            models.append((name, model))

    E, I, N = (0.7, 0.3, 0.5) 
    probabilities = [
        ('markov_independent', N, N),
        ('markov_selfexcite', E, E),
        ('markov_selfinhibit', I, I),
        ('markov_excite_left', E, N),
        ('markov_inhibit_left', I, N)
    ]

    for name, alpha, beta in probabilities:
        P = array([[alpha, 1 - beta], [1 - alpha, beta]])
        print P
        interval_generator = Exponential(1)
        sign_generator = Markov(array(P))
        duration = Uniform(0.1, 0.2)
        model = IndependentModel(interval_generator, sign_generator, duration)
        models.append((name, model))


    return models
