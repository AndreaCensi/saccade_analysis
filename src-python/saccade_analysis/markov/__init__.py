
from contracts import contract
import numpy as np



fit_dtype = [
     ('lower', float),
     ('upper', float),
     ('mean', float),
     ('confidence', float),
     ('skewed', float) # only used for binomial
]
 
 
from .binomial_dist_stats import *
from .first_order import *
from .poisson_fitting import *
from .binomial_fitting import *
