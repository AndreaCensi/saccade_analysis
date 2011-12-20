from contracts import contract
from reprep import MIME_PDF, Report
from saccade_analysis.density import scale_score, plot_rate_bars
from saccade_analysis.markov import fit_dtype
import numpy as np
import os


def compute_samples(simulate, N):
    K = simulate().size
    simulations = np.zeros((K, N))
    for t in range(N):
        simulations[:, t] = simulate()
    return simulations


@contract(N='int,>0', returns='array[K]')
def estimate_bounds_by_simulations(simulate, N):
    ''' 
        simulate: function returning a sample of the process
        N: number of simulations
    '''
    return compute_statistics(compute_samples(simulate, N))


@contract(samples='array[KxN]', returns='array[K]')
def compute_statistics(samples):
    statistics = np.ndarray(samples.shape[0], fit_dtype) 
    for i in range(samples.shape[0]):
        statistics[i]['mean'] = np.mean(samples[i, :])
        l, u = np.percentile(samples[i, :], [5, 95])
        statistics[i]['upper'] = u
        statistics[i]['lower'] = l
    return statistics 


@contract(statistics='array[K]', N='N,int,>0', returns='array[K]')
def estimate_order_by_resimulating(statistics, N):
    ''' 
        statistics: confidence bounds
        N: number of simulations
    '''
    samples = compute_samples(lambda: simulate_distribution(statistics), N) 
    order = compute_order(samples)
    return compute_statistics(order) 
 
 
@contract(samples='array[KxN]', returns='array[KxN]')
def compute_order(samples):
    order = np.zeros(samples.shape)
    for t in range(samples.shape[1]):
        order[:, t] = scale_score(samples[:, t])
    return order
    
def compute_order_samples(simulate, N):
    samples = compute_samples(simulate, N)
    return compute_order(samples)

    
def simulate_distribution(stats):
    return np.random.uniform(stats['lower'], stats['upper'])

def main():
    
    np.seterr(all='warn')
    
    K = 50
    ks = np.linspace(0, K - 1, K)
    f_mean = lambda k: np.exp(-k * 0.2)
    noise_eff = 0.05
    
    true_stats = np.ndarray(K, fit_dtype)
    true_stats['mean'] = f_mean(ks) 
    true_stats['lower'] = true_stats['mean'] - noise_eff
    true_stats['upper'] = true_stats['mean'] + noise_eff 
    
    simulate = lambda: simulate_distribution(true_stats)
    
    # two realizations
    X1 = simulate()
    X1_order = scale_score(X1)
    X2 = simulate()
    X2_order = scale_score(X2)
    
    # Now estimate upper and lower bounds by simulations
    observed_stats = estimate_bounds_by_simulations(simulate, N=100)
    order_est = estimate_order_by_resimulating(observed_stats, N=1000)


    print('Simulating distribution...')
    orders = compute_order_samples(simulate, N=10000)
    print('..done')

    r = Report('orderdemo')
    f = r.figure('figures', cols=3)
    
    z = 0.6
    figparams = dict(figsize=(4 * z, 3 * z), mime=MIME_PDF)
    
    from matplotlib import rc
    rc('font', **{'family':'serif',
                  'serif':['Times', 'Times New Roman', 'Palatino'],
                   'size': 7.0})
    rc('text', usetex=True)

    with f.plot('true', caption='True distribution', **figparams) as pl:
        plot_rate_bars(pl, ks, true_stats, 'b', label='$p(X^k)$')
        #pl.plot(ks, true_stats['mean'], 'b.')
        pl.xlabel('$k$')
        pl.ylabel('$X^k$')
        pl.legend()
        #pl.title('Distribution of the random variables $X^k$')

    with f.plot('meanorder', caption='True distribution', **figparams) as pl:
        pl.plot(ks, scale_score(true_stats['mean']), 'r.',
                label='$\\mathsf{order}(\\mathsf{mean}(X^k))$')
        pl.xlabel('$k$')
        pl.ylabel('$\\mathsf{order}(\\mathsf{mean}(X^k))$')
        pl.legend()
        #pl.title('Order of the means of $X^k$')

    with f.plot('realizations', caption='Realizations', **figparams) as pl:
        pl.plot(X1, 'bx', label='$x_1$')
        pl.plot(X2, 'g.', label='$x_2$')
        pl.xlabel('$k$')
        pl.ylabel('$x_i$')
        pl.legend()
        #pl.title('Two realizations of the process')

    with f.plot('orders', caption='orders', **figparams) as pl:
        pl.plot(X1_order, 'rx', label='$\\mathsf{order}(x_1)$')
        pl.plot(X2_order, 'm.', label='$\\mathsf{order}(x_2)$')
        pl.xlabel('$k$')
        pl.ylabel('$\\mathsf{order}(x_i)$')
        pl.legend()
        #pl.title('Computed order from realizations of the process')

    with f.plot('estorder', caption='Estimated order', **figparams) as pl:
        plot_rate_bars(pl, ks, order_est, 'r', label='$p(\\mathsf{order}(X^k))$')
        #pl.plot(ks, order_est['mean'], 'r.')
        pl.xlabel('$k$')
        pl.ylabel('$\\mathsf{order}(X)$')
        pl.legend()
        #pl.title('Estimated confidence bounds order from resimulating')

    with f.plot('observed', caption='Observed statistics', **figparams) as pl:
        plot_rate_bars(pl, ks, observed_stats, 'b')
        pl.xlabel('$k$')
        pl.ylabel('$X^k$')
        
    def plot_histogram(k, pylab, color, label):
        dist = orders[k, :]
        values, _ = np.histogram(dist, bins=range(K + 1), normed=True)
        left = ks 
        pylab.bar(left, values, width=1, color=color, label=label)
        
    with f.plot('ordersex', caption='Some examples', **figparams) as pl:
        plot_histogram(10, pl, 'r', '$\\mathsf{order}(X^{10})$')
        plot_histogram(15, pl, 'g', '$\\mathsf{order}(X^{15})$')
        plot_histogram(40, pl, 'b', '$\\mathsf{order}(X^{40})$')
        pl.xlabel('$\\mathsf{order}$')
        pl.ylabel('probability')
        pl.legend(loc='upper left')
        
    rd = 'order_estimation_test2' 
    filename = os.path.join(rd, 'index.html')
    print('Writing to %r.' % filename)
    r.to_html(filename, resources_dir=rd)
    
    
if __name__ == '__main__':
    main()

