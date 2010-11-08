'''
Definition of variable of interests for plotting.

'''

class Variable():
    def __init__(self, id, letter, name, interesting, 
                 unit, density_max_y, density_bins, include, mod=False,
                 field=None):
        
        if field is None:
            field= id
        self.id = id
        self.name = name
        self.letter = letter
        self.interesting = interesting
        self.unit = unit
        self.density_max_y = density_max_y
        self.density_bins = density_bins
        self.include = include
        self.mod = mod
        self.field = field

variables = []

variables.append(Variable(
    id='amplitude',
    letter='A',
    interesting = [1, 200],
    name = 'Amplitude',
    unit = 'deg',
    density_max_y= 0.06,
    density_bins = 100,
    include = True
))


variables.append(Variable(
    id='duration',
    letter='D',
    interesting = [0.01, 0.9],
    name = 'Duration',
    unit = 's',
    density_max_y= 15,
    density_bins = 50,
    include = True
))
 

variables.append(Variable(
    id='top_velocity',
    letter='V',
    interesting = [10, 4000], # 2000 enough for tether
    name = 'Top angular velocity',
    unit = 'deg/s',
    density_max_y= 3 * 1e-3,
    density_bins = 100,
    include = True
))
  

variables.append(Variable(
    id='interval',
    field='time_passed',
    letter='I',
    interesting = [0.01, 8],
    name = 'Interval',
    unit = 's',
    density_max_y= 2,
    density_bins = 100,
    include = True
))


# 
#    nv=nv+1;
#    variables(nv).id = 'sign';
#    variables(nv).letter = 'S';
#    variables(nv).interesting = [-1.1 1.1];
#    variables(nv).name = 'Sign';
#    variables(nv).values = [saccades.sign];
#    variables(nv).unit = '';
#    variables(nv).density_max_y = 1.1;
#    variables(nv).density_bins = 100;
#    variables(nv).include_in_bigcorr = false;


variables.append(Variable(
    id='initial_orientation',
    field='orientation_start',
    letter='io',
    interesting = [0, 360],
    name = 'Initial orientation',
    unit = 'deg',
    density_max_y= None,
    density_bins = None,
    include = False,
    mod=True
)) 


variables.append(Variable(
    id='final_orientation',
    field='orientation_stop',
    letter='io',
    interesting = [0, 360],
    name = 'Final orientation',
    unit = 'deg',
    density_max_y= None,
    density_bins = None,
    include = False,
    mod=True
)) 
# 
#% 
#%     nv=nv+1;
#%     variables(nv).id = 'time_start';
#%     variables(nv).name = 'Time from log start';
#% %    variables(nv).interesting = [0 400];
#%     variables(nv).values = [saccades.time_start];
#%     variables(nv).unit = 's';
 