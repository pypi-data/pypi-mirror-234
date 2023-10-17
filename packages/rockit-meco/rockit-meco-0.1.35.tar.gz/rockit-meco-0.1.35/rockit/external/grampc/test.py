from pylab import *
import unittest

from rockit import Ocp, DirectMethod, MultipleShooting, FreeTime, Stage
import numpy as np
from casadi import kron, DM

from .method import GrampcMethod

from ...casadi_helpers import AutoBrancher

class GrampcTests(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
