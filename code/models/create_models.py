from create_tests import IndependentModel, BernouilliSign, Exponential, \
    ParallelIndependentModel, Uniform, ParallelModel



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
        + 1: Exponential(2),
         0: Exponential(1),
        - 1: Exponential(0.5)
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

    return models
