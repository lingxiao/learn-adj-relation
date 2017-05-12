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
	run baseline using ppdb-ngram graph
'''
print('\n\t>> ranking moh-no-ties with ppdb-ngram graph ...')
rank_all_gold( test['moh-no-tie']
	         , decide_fn(G_ppng)
	         , os.path.join(work_dir['results'], 'baseline-ppdb-ngram-moh-no-tie.txt')
	         , refresh = False
	         , save    = True )


print('\n\t>> ranking ccb-no-ties with ppdb-ngram graph ...')
rank_all_gold( test['ccb-no-tie']
	         , decide_fn(G_ppng)
	         , os.path.join(work_dir['results'], 'baseline-ppdb-ngram-ccb-no-tie.txt')
	         , refresh = False
	         , save    = True )

print('\n\t>> ranking ccb with ppdb-ngram graph baseline ...')
rank_all_gold( ccb
	         , decide_fn(G_ppng)
	         , os.path.join(work_dir['results'], 'baseline-ppdb-ngram-ccb.txt')
	         , refresh = False
	         , save    = True)

print('\n\t>> ranking moh with ppdb-ngram graph baseline ...')
rank_all_gold( moh
	         , decide_fn(G_ppng)
	         , os.path.join(work_dir['results'], 'baseline-ppdb-ngram-moh.txt')
	         , refresh = False
	         , save    = True)

print('\n\t>> ranking bcs with ppdb-ngram graph baseline ...')
rank_all_gold( bcs
	         , decide_fn(G_ppng)
	         , os.path.join(work_dir['results'], 'baseline-ppdb-ngram-bcs.txt')
	         , refresh = False
	         , save    = True)


