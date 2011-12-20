

class PlotParams:
    
    max_rate = 6.0

    COL_LEFT = 'r'
    COL_LEFT_RGB = [1, 0, 0]
    
    COL_RIGHT = 'b'
    COL_RIGHT_RGB = [0, 0, 1]
    
    COL_BOTH = 'k'
    #COL_BOTH_RGB = [0, 0, 0.2]
    
    TEXT_EVENT_GEN_RATES = 'Event rates $r_i^k$ (sac./s)'
    TEXT_OBSERVED_EVENT_RATES = 'Event rates $m_i^k$ (sac./s)'
    
    FEATURE_TEXT = 'Estimated feature $z^k$ (unitless)'
    
    LABEL_LEFT = 'left'
    LABEL_RIGHT = 'right'
    
    # figparams = dict(figsize=(2.5, 1.5))
    
    #figsize = (2.5, 1.7)
    figsize = (2.2, 1.7)
    
    figsize_kernel = (1.3, 1)
    figsize_order = (1, 1)
    
    speed_bounds = dict(min_value=0.2, max_value=0.33)
    cmap_speed = 'jet'
    cmap_total = 'jet'
    
    @staticmethod
    def init_matplotlib():
        from matplotlib import rc
        #    rc('font', **{'family':'serif',
        #                  'serif':['Times', 'Times New Roman', 'Palatino'],
        #                   'size': 8.0})
        rc('font', **{'family':'sans-serif',
                      'sans-serif':['Arial'],
                       'size': 8.0})
        #rc('text', usetex=True)    
        
    spines_outward = 10
    
