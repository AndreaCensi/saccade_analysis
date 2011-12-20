from ..markov import fit_dtype
from collections import namedtuple

from . import np, contract
 
estimate_stimulus_return = namedtuple('estimate_stimulus_return',
                                      'L_order R_order order z')


@contract(y_L='shape(x)', y_R='shape(x)', returns=estimate_stimulus_return)
def estimate_stimulus(y_L, y_R):
    ''' 
        Assumes uniform probability distribution for y_L and y_R,
        with limits y_L['lower'], y_R['upper']. 
        (Assumes that both y_L and y_R have a dtype with those fields.)
        
        Returns the order as a fit_dtype.
    ''' 
    z = np.ndarray(y_L.shape, fit_dtype)
    order = np.ndarray(y_L.shape, fit_dtype)
    
    T = 1000
    perc = 1
    L_order = estimate_order_by_simulation(y_L, T=T, perc=perc)
    R_order = estimate_order_by_simulation(y_R, T=T, perc=perc, inverse=True)
    
    # Gaussian approximation
    
    L_var = L_order['upper'] - L_order['lower']
    R_var = R_order['upper'] - R_order['lower']
    
    # slight shortcut for var == 0
    L_var += 0.1
    R_var += 0.1
    
    L_inf = 1.0 / L_var
    R_inf = 1.0 / R_var
    
    # Weighted mean 
    order_mean = ((L_inf * L_order['mean'] + R_inf * R_order['mean']) 
                  / (L_inf + R_inf))
    
    if False:
        threshold = 0.5
        better_left = L_var < R_var * threshold
        better_right = R_var < L_var * threshold
        order_mean[better_left] = L_order['mean'][better_left]
        order_mean[better_right] = R_order['mean'][better_right]
    order_var = 1 / (L_inf + R_inf)
    order_upper = order_mean + 3 * np.sqrt(order_var)
    order_lower = order_mean - 3 * np.sqrt(order_var)
    
    order['mean'] = order_mean 
    order['upper'] = order_upper
    order['lower'] = order_lower
    
    # Normalize in [-1,+1]
    order2 = scale_score(order_mean)
    f = lambda x: 2 * (x / y_L.size - 0.5) 
    z['mean'] = f(order2) #f(order_mean)
    z['upper'] = f(order_upper)
    z['lower'] = f(order_lower) 
    
    return estimate_stimulus_return(L_order=L_order,
                                    R_order=R_order,
                                    order=order,
                                    z=z)


@contract(y='array,shape(x)', returns='shape(x)')
def estimate_order_by_simulation(y, T=100, perc=5, inverse=False):
    n = y.size 
    
    lower = y['lower']
    upper = y['upper']
    diff = upper - lower
    lower2 = lower - diff / 2
    upper2 = upper + diff / 2
    
    def simulate():
        x = np.random.uniform(lower2, upper2)
        if inverse:
            x = -x
        return x
    
    order = np.zeros((n, T))
    for k in range(T):
        order[:, k] = scale_score(simulate()).flat
    
    order_sim = np.ndarray(y.shape, fit_dtype) 
    for i in range(n):
        order_sim.flat[i]['mean'] = np.mean(order[i, :])
        l, u = np.percentile(order[i, :], [perc, 100 - perc])
        order_sim.flat[i]['upper'] = u
        order_sim.flat[i]['lower'] = l
    return order_sim


def scale_score_norm(x):
    ''' Returns the score, normalized in [0,1] '''
    return scale_score(x).astype('float32') / (x.size - 1)

def scale_score(x):
    y = x.copy()
    order = np.argsort(x.flat)
    # Black magic ;-) Probably the smartest thing I came up with today. 
    order_order = np.argsort(order)
    y.flat[:] = order_order.astype(y.dtype)
    return y
