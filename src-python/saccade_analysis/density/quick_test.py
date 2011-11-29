from . import np, Report

def noise(sigma):
    return np.random.randn() * sigma

def threshold(s, T):
    if s >= T:
        return +1
    elif s <= -T:
        return -1
    else:
        return 0
    
def model(z, sigma1, T1, sigma2, T2):
    ''' Returns -1,0,1 '''
    s1 = z + noise(sigma1)
    gen1 = threshold(s1, T1)
    gen2 = threshold(noise(sigma2), T=T2)
    gen = gen1 + gen2    
    return int(np.sign(gen))
    
    

def plot_stats(f, name, sigma1, T1, sigma2, T2, zmax=2, K=200):
    zs = np.linspace(-zmax, +zmax, 100)
    fL = np.zeros(zs.shape)
    fR = np.zeros(zs.shape)
    no = np.zeros(zs.shape)
#    choices = {1:fL, -1:fR, 0:no}
    for i, z in enumerate(zs):
        s = np.zeros(K)
        for k in range(K): #@UnusedVariable
            s[k] = model(z, sigma1, T1, sigma2, T2)
        
        for what, who in {1:fL, -1:fR, 0:no}.items():
            who[i] = np.sum(s == what)


#    M = np.max((np.max(fL), np.max(fR), np.max(no)))
    
    with f.plot(name) as pylab:
        pylab.plot(zs, (fR + fL) / K, 'k--')            
        pylab.plot(zs, fL / K, 'r')
        pylab.plot(zs, fR / K, 'b')
        pylab.axis((-zmax, zmax, -0.1, 1.1))
    
    f.last().add_to(f)
    
    with f.plot(name + 'm') as pylab:            
        pylab.plot(fL / K, fR / K, 'k.') 
        pylab.axis((-0.1, 1.1, -0.1, 1.1))
    
    f.last().add_to(f)
    
def main():
    r = Report()
    f = r.figure(cols=4)
    
    plot_stats(f, 'modelA', sigma1=0, T1=1, sigma2=0, T2=1)
    plot_stats(f, 'modelB', sigma1=0.2, T1=1, sigma2=0, T2=1)
    plot_stats(f, '2modelB', sigma1=0.5, T1=1, sigma2=0, T2=1)
    plot_stats(f, '2modelC', sigma1=0.5, T1=1, sigma2=1, T2=1)
    plot_stats(f, '2modelC2', sigma1=0.5, T1=1, sigma2=1, T2=1)
    plot_stats(f, '2modelD', sigma1=0.5, T1=100, sigma2=1, T2=1)
   
    sigmas = np.linspace(0, 3, 10)
    f = r.figure('sigma', cols=4)
    for i, sigma in enumerate(sigmas): #@UnusedVariable
        plot_stats(f, 'model%.1f' % sigma, sigma1=sigma, T1=1, sigma2=0, T2=1)
        
    r.to_html('quick_test.html')
    
    
if __name__ == '__main__':
    main()
