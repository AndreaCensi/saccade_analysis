from contracts import contract, new_contract
from numpy.testing.utils import assert_allclose
from reprep import Report
from saccade_analysis.density.report_models import scale_score_norm, \
    plot_rate_bars, scale_score
from saccade_analysis.markov import fit_dtype
import itertools
import numpy as np
from collections import namedtuple

@contract(y_L='array[N]', y_R='array[N]')
def estimate_stimulus_naive(y_L, y_R):
    L_order = scale_score_norm(y_L)
    R_order = scale_score_norm(y_R)
               
    M = 0.5 * (L_order + 1 - R_order)
    c = 0.5 # TODO
    phi = 2 * (M - c)
    return phi


#fit_dtype = [
#     ('lower', float),
#     ('upper', float),
#     ('mean', float),
#     ('confidence', float),
#     ('skewed', float) # only used for binomial
#]

estimate_stimulus_return = namedtuple('estimate_stimulus_return',
                                      'L_order R_order order z'
                                      )
@contract(y_L='array[N]', y_R='array[N]', returns=estimate_stimulus_return)
def estimate_stimulus(y_L, y_R):
    ''' Assumes that both y_L and y_R have a dtype with upper and lower.
        Considers uniform probability in upper/lower. 
        
        Returns the order as a fit_dtype.
    ''' 
    z = np.ndarray(y_L.shape, fit_dtype)
    order = np.ndarray(y_L.shape, fit_dtype)
    
    T = 1000
    perc = 1
    L_order = estimate_order_by_simulation(y_L, T=T, perc=perc)
    R_order = estimate_order_by_simulation(y_R, T=T, perc=perc, inverse=True)
    
    L_var = L_order['upper'] - L_order['lower']
    R_var = R_order['upper'] - R_order['lower']
    
    # slight shortcut for var == 0
    L_var += 0.1
    R_var += 0.1
    
    L_inf = 1.0 / L_var
    R_inf = 1.0 / R_var
    
    order_mean = (L_inf * L_order['mean'] + R_inf * R_order['mean']) / (L_inf + R_inf)
    order_var = 1 / (L_inf + R_inf)
    order_upper = order_mean + 3 * np.sqrt(order_var)
    order_lower = order_mean - 3 * np.sqrt(order_var)
    
    order['mean'] = order_mean 
    order['upper'] = order_upper
    order['lower'] = order_lower
    
    f = lambda x: 2 * (x / y_L.size - 0.5) 
    z['mean'] = f(order_mean)
    z['upper'] = f(order_upper)
    z['lower'] = f(order_lower) 
    
    return estimate_stimulus_return(L_order=L_order,
                                    R_order=R_order,
                                    order=order,
                                    z=z)

Comp = namedtuple('Comparison', 'gt eq lt desc')
def opposite(c1):
    return Comp(c1.lt, c1.eq, c1.gt, '%s (opposite)' % c1.desc)
def same(c1, c2):
    return np.allclose(c1[:3], c2[:3])

@new_contract
def valid_comp(c):
    assert 0 <= c.lt <= 1
    assert 0 <= c.eq <= 1
    assert 0 <= c.gt <= 1
    assert_allclose(c.gt + c.eq + c.lt, 1)
        
@contract(b1='x', u1='>=x', b2='y', u2='>=y', returns='valid_comp')
def probability_larger(b1, u1, b2, u2):
    ''' Returns a Comp tuple. '''
    b1 = float(b1)
    u1 = float(u1)
    b2 = float(b2)
    u2 = float(u2)
    assert b1 <= u1
    assert b2 <= u2
    # let's get rid of degenerate cases
#    if b1 == u1: return 1.0 if b2 <= b1 <= u2 else 0.0
#    if b2 == u2: return 0.0 if b1 <= b2 <= u1 else 1.0
#    
    def res(p1, peq, p2, case):
        assert 0 <= p1 <= 1, p1
        assert 0 <= peq <= 1, peq
        assert 0 <= p2 <= 1, p2
        assert_allclose(p1 + peq + p2, 1)
        return Comp(p1, peq, p2, case)
    
    # Disjoint
    if u1 < b2:
        return res(0.0, 0.0, 1, 'u1<b2')
    
    if b1 > u2: 
        return res(1, 0.0, 0.0, 'b1>u2')
    
    if (u1 == b1) and (u2 == b2):
        return res(0.0, 1, 0.0, 'b1>u2')
#    
#    if u1 == b1:
#        y1 = u1
#        if y1 > b 
#    
    L1 = u1 - b1 
    L2 = u2 - b2
        
    # Contained
    # y1 inside y2
    if u2 != b2 and (b1 >= b2 and u1 <= u2):
        m1 = 0.5 * (b1 + u1)
        assert L2 > 0
        p = (u2 - m1) / L2
        return res(1 - p, 0.0, p, 'y1 in y2')
    
    # y2 inside y1
    if u1 != b1 and (b2 >= b1 and u2 <= u1):
        m2 = 0.5 * (b2 + u2) 
        assert L1 > 0
        p = (u1 - m2) / L1
        return res(p , 0.0, 1 - p, 'y2 in y1')
    
    # Mixed
    A = L1 * L2
    assert A > 0
    
    if b1 <= b2 <= u1 <= u2:
        p = 0.5 * ((u1 - b2) ** 2) / A
        return res(p, 0, 1 - p, "b1 <= b2 <= u1 <= u2")
    
    if b2 <= b1 <= u2 <= u1:
        p = 0.5 * ((u2 - b1) ** 2) / A
        return res(p, 0, 1 - p, " b2 <= b1 <= u2 <= u1")
    
    
    assert False

def probability_larger_test():
    cases = [
      ((0.0, 0.0, +0.0, +0.0), Comp(0.0, 1.0, 0.0, ""), ""),
      ((0.0, 0.0, -1.0, +0.0), Comp(1.0, 0.0, 0.0, ""), ""),
      ((0.0, 0.0, -1.0, +1.0), Comp(0.5, 0.0, 0.5, ""), ""),
      ((0.0, 0.0, +1.0, +1.0), Comp(0.0, 0.0, 1.0, ""), ""),
      ((0.0, 0.0, +1.0, +2.0), Comp(0.0, 0.0, 1.0, ""), ""),
      ((0.0, 0.0, -1.0, -0.5), Comp(1.0, 0.0, 0.0, ""), ""),
      ((0.1, 0.1, 0, 1), Comp(0.1, 0.0, 0.9, ""), ""),
      ((0.3, 0.3, 0, 1), Comp(0.3, 0.0, 0.7, ""), ""),
      ((0.3, 0.7, 0, 1), Comp(0.5, 0.0, 0.5, ""), ""),
      ((0.4, 0.6, 0, 1), Comp(0.5, 0.0, 0.5, ""), ""),
      
      ((0, 1, 0, 1), Comp(0.5, 0.0, 0.5, ""), ""),
    ]
    # add symmetries
    cases2 = list(cases)
    for p, res, desc in cases:
        p2 = [x - 10 for x in p]
        desc2 = '%s (-10)' % desc
        cases2.append((p2, res, desc2))
    
    for p, res, desc in cases:
        p2 = [x * 5 for x in p]
        desc2 = '%s (*5)' % desc
        cases2.append((p2, res, desc2))
    
    
    for p, res, desc in cases:
        res2 = opposite(res)
        desc2 = '%s (opposite)' % desc
        b1, u1, b2, u2 = p
        p2 = (b2, u2, b1, u1)
        cases2.append((p2, res2, desc2))
        
    for p, expected, desc in cases2:
        res = probability_larger(*p)
        b1, u1, b2, u2 = p
        if not same(res, expected):
            err_msg = ('y1: [%g,%g] y2: [%g,%g] %s ' % 
                        (b1, u1, b2, u2 , desc))
            err_msg += '\nExpected: %s' % str(expected)
            err_msg += '\nobtained: %s' % str(res)
            raise Exception(err_msg)
        print('%15s  %s %s' % (desc, str(p), expected))
        
    
@contract(y='array[N]')
def estimate_order(y):
    ''' Estimates bounds for order[y]. 
        y is assumed to be independent samples with
        uniform distribution in y['upper'][i] and y['lower'][i].
    '''
    
    # Define P[i,j] as the probability that y_i >= y_j 
    n = y.size
    P = np.zeros((n, n))
    for i, j in itertools.product(range(n), range(n)):
        b1 = y[i]['lower']
        u1 = y[i]['upper']
        b2 = y[j]['lower']
        u2 = y[j]['upper']
        res = probability_larger(b1, u1, b2, u2)
        P[i, j] = res.gt #+ res.eq 
        assert 0 <= P[i, j] <= 1, res
    # Variance of such binomial probabilities
    Var = P * (1 - P)
    
    M = np.zeros((n, n))
    res = np.ndarray(n, fit_dtype)
    for i in range(n):
        mean = P[i, :].sum()
        var = Var[i, :].sum()
        std = np.sqrt(var)
        upper = mean + 3 * std
        lower = mean - 3 * std
        res[i]['mean'] = mean 
        res[i]['upper'] = upper
        res[i]['lower'] = lower
        
        M[i, :] = 0
        M[i, 0] = 1
        def shift(x):
            n = x.size
            assert x[-1] == 0, 'P=%s' % P.tolist()
            y = np.zeros(x.size)
            y[1:] = x[:-1]
            y[0] = 0
            return y
        
        for j in range(n):
            if i == j: continue
            p = P[i, j]
            M[i, :] = p * shift(M[i, :]) + (1 - p) * M[i, :]
            assert_allclose(M[i, :].sum(), 1)
            
        M[i, :] = np.cumsum(M[i, :])
    
    return res, M
    

@contract(y='array[N]')
def estimate_order_by_simulation(y, T=100, perc=5, inverse=False):
    n = y.size 
    def simulate():
        lower = y['lower']
        upper = y['upper']
        x = np.random.uniform(lower, upper)
        if inverse:
            x = -x
        return x
    
    ord = np.zeros((n, T))
    for k in range(T):
        ord[:, k] = scale_score(simulate())
    
    order_sim = np.ndarray(n, fit_dtype) 
    for i in range(n):
        order_sim[i]['mean'] = np.mean(ord[i, :])
        l, u = np.percentile(ord[i, :], [perc, 100 - perc])
        order_sim[i]['upper'] = u
        order_sim[i]['lower'] = l
    return order_sim

def main():
    
    np.seterr(all='warn')
    
    n = 100
    z = np.linspace(-1, 1, n)
    z_order = np.array(range(n))
    alpha = 0.2
    alpha = 0.1
    base = 0.3
    noise = 0.1
    noise_eff = noise / 2
    f_L = lambda z: np.exp(-np.abs(1 - np.maximum(z, 0)) / alpha) + base
    f_R = lambda z: np.exp(-np.abs(-1 - np.minimum(z, 0)) / alpha) + base
    
    rate_L0 = f_L(z) 
    rate_R0 = f_R(z) 
    
    simulate_L = lambda: f_L(z) + np.random.uniform(-1, 1, n) * noise_eff 
    simulate_R = lambda: f_R(z) + np.random.uniform(-1, 1, n) * noise_eff
    
    rate_L = simulate_L()
    rate_R = simulate_R()
    
    print('Simulation')
    T = 100
    ord = np.zeros((n, T))
    for k in range(T):
        ord[:, k] = scale_score(simulate_L())
    print('Done')
    order_L_sim = np.ndarray(n, fit_dtype) 
    for i in range(n):
        order_L_sim[i]['mean'] = np.mean(ord[i, :])
        l, u = np.percentile(ord[i, :], [5, 95])
        order_L_sim[i]['upper'] = u
        order_L_sim[i]['lower'] = l
        
    

    rate_L_est = np.ndarray(n, fit_dtype) 
    rate_L_est['upper'] = rate_L + noise
    rate_L_est['lower'] = rate_L - noise
    rate_R_est = np.ndarray(n, fit_dtype) 
    rate_R_est['upper'] = rate_R + noise
    rate_R_est['lower'] = rate_R - noise 

    # estimate according to naive procedure
    z_naive = estimate_stimulus_naive(rate_L, rate_R)
    
    res = estimate_stimulus(rate_L_est, rate_R_est)
    L_order = res.L_order
    R_order = res.R_order

        
    scale_rate = max(rate_L.max(), rate_R.max()) * 1.2
    cL = 'r'
    cR = 'b'
    
    r = Report()
    f = r.figure(cols=4)
    with r.data_pylab('noiseless') as pylab:
        pylab.plot(z, rate_L0, '%s-' % cL)
        pylab.plot(z, rate_R0, '%s-' % cR)
        pylab.axis((-1, 1, 0.0, scale_rate))
    r.last().add_to(f, caption='noiseless rates')
    
    with r.data_pylab('observed_rates') as pylab:
        pylab.plot(z, rate_R0, '%s-' % cR)
        pylab.plot(z, rate_L0, '%s-' % cL)
        plot_rate_bars(pylab, z, rate_L_est, '%s' % cL)
        plot_rate_bars(pylab, z, rate_R_est, '%s' % cR)
#
#        pylab.plot(z, rate_L, '%s.' % cL)
#        pylab.plot(z, rate_R, '%s.' % cR)
        pylab.axis((-1, 1, 0.0, scale_rate))
    r.last().add_to(f, caption='true_rates')
  
    with r.data_pylab('M') as pylab:
        pylab.plot(z, rate_L0, '%s-' % cL)
        pylab.plot(z, rate_R0, '%s-' % cR)
        pylab.axis((-1, 1, 0.0, scale_rate))
        
    with r.data_pylab('z_naive') as pylab:
        pylab.plot(z_naive, rate_L, '%s.' % cL)
        pylab.plot(z_naive, rate_R, '%s.' % cR)
        pylab.axis((-1, 1, 0.0, scale_rate))
    r.last().add_to(f, caption='Stimulus estimated in naive way.')
    
    
    with r.data_pylab('simulated_order_stats') as pylab:
        pylab.plot([0, 0], [n, n], 'k-')
        pylab.plot([0, n], [n, 0], 'k-')
        pylab.plot(z_order, order_L_sim['mean'], '%s.' % cL)
        plot_rate_bars(pylab, z_order, order_L_sim, '%s' % cL)
        pylab.axis((0, n, -n / 10, n * 1.1))
        pylab.axis('equal')
    r.last().add_to(f, caption='Orders as found by simulation')
  
    
    with r.data_pylab('estimated_order') as pylab:
        pylab.plot(z, L_order['mean'], '%s.' % cL)
        pylab.plot(z, R_order['mean'], '%s.' % cR)
        pylab.axis((-1, 1, -n / 2, n * 3 / 2))
    r.last().add_to(f, caption='estimated_order')
  
    with r.data_pylab('estimated_order_order') as pylab:
        
        pylab.plot([0, 0], [n, n], 'k-')
        plot_rate_bars(pylab, z_order, L_order, '%s' % cL)
        plot_rate_bars(pylab, z_order, R_order, '%s' % cR)
        pylab.plot([0, 0], [n, n], 'k-')
        pylab.axis((0, n, -n / 10, n * 1.1))
        pylab.axis('equal')
    r.last().add_to(f, caption='estimated_order_order')
  
    with r.data_pylab('estimated_order_bar') as pylab:
        pylab.plot(z, L_order['mean'], '%s.' % cL)
        pylab.plot(z, R_order['mean'], '%s.' % cR)
        plot_rate_bars(pylab, z, L_order, '%s' % cL)
        plot_rate_bars(pylab, z, R_order, '%s' % cR)     
        pylab.axis((-1, 1, -n / 2, n * 3 / 2))
    r.last().add_to(f, caption='estimated_order_bar')
#  

    with r.data_pylab('estimated_order_both') as pylab:
        pylab.plot([0, 0], [n, n], 'g-')
        pylab.plot(z_order, res.z['mean'], 'k.')
        plot_rate_bars(pylab, z_order, res.z, 'k')
        pylab.axis((0, n, -n / 10, n * 1.1))
        pylab.axis('equal')
    r.last().add_to(f, caption='estimated_order_order')
#    cvalue = 0.05
#    vR = np.logical_and(res.MR > cvalue, res.MR < 1 - cvalue) 
#    vL = np.logical_and(res.ML > cvalue, res.ML < 1 - cvalue)
#    
#    r.data('MR', res.MR).display('scale', max_value=1, min_value=0)
#    r.last().add_to(f, caption='MR')
#    r.data('ML', res.ML).display('scale', max_value=1, min_value=0)
#    r.last().add_to(f, caption='ML')
#    r.data('vR', vR).display('scale', max_value=1, min_value=0)
#    r.last().add_to(f, caption='vR')
#    r.data('vL', vL).display('scale', max_value=1, min_value=0)
#    r.last().add_to(f, caption='vL')
#  


    with r.data_pylab('z_better') as pylab:
        pylab.plot(res.z['mean'], rate_L, '%s.' % cL)
        pylab.plot(res.z['mean'], rate_R, '%s.' % cR)
#        pylab.axis((-1, 1, 0.0, scale_rate))
    r.last().add_to(f, caption='Stimulus estimated in a better way.')
    
  
    filename = 'order_estimation.html' 
    print('Writing to %r.' % filename)
    r.to_html(filename)
    
    
if __name__ == '__main__':
    main()
