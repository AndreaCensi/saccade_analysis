from saccade_analysis.markov.tests_rates.simulate import simulate_system
from contracts import contract
import numpy as np
from saccade_analysis.markov import fit_poisson_multiple

def test_estimation_rates1():
    cases = [
        dict(rates=[1.], refractory=0.),
        dict(rates=[1.], refractory=1.),
        dict(rates=[1., 1.], refractory=0.),
        dict(rates=[1., 1.], refractory=1.),
        dict(rates=[1., 10.], refractory=1.),
    ]
    
    T = 100000.0
    
    algorithms = [estimate_rates_simple, estimate_rates_indep, fit_poisson_multiple] 
    for case in cases:
        rates = case['rates']
        refractory = case['refractory']
        count = simulate_system(rates, refractory, T)
        
        for algo in algorithms:

            rates_est = algo(count, T, refractory)
            err = np.linalg.norm(np.log(rates) - np.log(rates_est))
            ok = ":-)" if err < 0.1 else " X "
            w = lambda r: ", ".join("%8g e/s" % ri for ri in r) 
            msg = ("""%25s err %-7.3g %s ref %10g actual: %s  estim: %s  """ % 
                   (algo.__name__, err, ok, refractory, w(rates), w(rates_est)))
            print(msg)


@contract(T='float,>0', refractory='>=0', count='array[K](int32),K>0',
          returns='array[K](>=0)')
def estimate_rates_simple(count, T, refractory): #@UnusedVariable
    ''' Naive '''
    return count / T
    

def estimate_rates_indep(count, T, refractory):
    ''' Independent of each other. '''
    n = len(count)
    res = np.zeros(n)
    for i in range(n):
        res[i] = solve_rate(count[i], T, refractory)
    return res


@contract(num='int,>=0', refractory='float,>=0', interval='float,>0',
          returns='float,>=0')
def solve_rate(num, interval, refractory):
    return num / (interval - num * refractory)

#
#@contract(num='int,>=0', refractory='float,>=0', interval='float,>0',
#          returns='float,>=0')
#def solve_rate_wrong(num, interval, refractory):
#    ''' Solves the equation   
#            
#            x = N / (L- x tau)
#        
#        which can be written as 
#        
#            L x  - tau x**2 = N
#            
#        that is
#        
#            tau x**2 + L x - N = 0
#            
#            x = (-b +- sqrt(b^2 - 4 ac)) / 2a
#            
#        with 
#        
#            a = tau
#            b = L
#            c = -N
#            
#        because we want a positive solution, only take 
#        the + solution.
#            
#    '''
#    tau = float(refractory)
#    L = float(interval)
#    N = float(num)
#    
#    if tau == 0:
#        return N / L
#     
#    a = tau
#    b = L
#    c = -N
#    
#    x = (-b + np.sqrt(b * b - 4 * a * c)) / (2 * a) 
#            
#    assert x >= 0
#    return x



if __name__ == '__main__':
    test_estimation_rates1()
