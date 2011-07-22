""" Statistics of permanence """

import logging

logging.basicConfig();
logger = logging.getLogger("density")
logger.setLevel(logging.DEBUG)


from .da_cells import *
from .xy_cells import *
