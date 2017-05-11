############################################################
# Module  : pointwise estimation baeline
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os
import pickle
import numpy as np

from app     import *
from utils   import *
from scripts import *
from scripts.graph import *
from experiments.argmax import *
from experiments.rank_all import *
from experiments.baseline import *

############################################################
'''
	run unform baseline 
'''
print('\n\t>> ranking ccb with ngram graph baseline ...')
rank_all_gold(ccb
	         , decide_fn_uniform()
	         , os.path.join(work_dir['results'], 'uniform-reverse-ccb.txt')
	         , refresh = False)

print('\n\t>> ranking moh with ngram graph baseline ...')
rank_all_gold(moh
	         , decide_fn_uniform()
	         , os.path.join(work_dir['results'], 'uniform-reverse-moh.txt')
	         , refresh = False)

print('\n\t>> ranking bcs with ngram graph baseline ...')
rank_all_gold(bcs
	         , decide_fn_uniform()
	         , os.path.join(work_dir['results'], 'uniform-reverse-bcs.txt')
	         , refresh = False)


