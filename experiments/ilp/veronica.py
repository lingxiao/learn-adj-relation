############################################################
# Module  : ILP 
# Date    : April 12th
# Author  : Xiao Ling, merle
############################################################

import os
import shutil

from scripts import *
from utils   import *
from app     import *

from experiments.ilp import *

# from pulp    import *

from collections import Counter

############################################################
'''
	open gold
'''
exp_root = get_path('ilp')
ccb      = read_gold(get_path('ccb'))
moh      = read_gold(get_path('bansal'))
probs    = '/Users/lingxiao/Documents/research/code/data-learn-adj-relation/deploy/probs/probs-ngram-ppdb.txt'


