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
from experiments.baseline.top import *

############################################################
'''
	run baseline using ppdb graph
'''
print('\n\t>> ranking ccb with ppdb graph baseline ...')
rank_all_gold( ccb
	         , decide_fn(G_ppdb)
	         , os.path.join(work_dir['results'], 'baseline-ppdb-ccb.txt')
	         , refresh = False)

print('\n\t>> ranking moh with ppdb graph baseline ...')
rank_all_gold( moh
	         , decide_fn(G_ppdb)
	         , os.path.join(work_dir['results'], 'baseline-ppdb-moh.txt')
	         , refresh = False)

print('\n\t>> ranking bcs with ppdb graph baseline ...')
rank_all_gold( bcs
	         , decide_fn(G_ppdb)
	         , os.path.join(work_dir['results'], 'baseline-ppdb-bcs.txt')
	         , refresh = False)


