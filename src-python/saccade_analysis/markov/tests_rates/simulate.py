from contracts import contract
import numpy as np

@contract(rates='seq[K,>0](>0)', refractory_interval='>=0', T='>=0',
          returns='array[K](>=0)')
def simulate_system(rates, refractory_interval, T):
    n = len(rates)
    count = np.zeros(n, 'int32')
    t = 0 
    while t < T:
        next_event = np.zeros(n)
        for i in range(n):
            next_event[i] = np.random.exponential(scale=1.0 / rates[i])
        happened = np.argmin(next_event)
        count[happened] += 1
        t += next_event[happened] 
        t += refractory_interval
        
    return count

    
