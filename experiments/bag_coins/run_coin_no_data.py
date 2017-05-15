############################################################
# Module  : estimate missing edge using bag of coins model
# 		    on no data set
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os
import pickle
import numpy as np
import networkx as nx

from app     import *
from utils   import *
from scripts import *
from scripts.graph import *
from experiments.argmax import *
from experiments.rank_all import *
from experiments.bag_coins import *

############################################################
'''
	run on all data set
'''
decide      = decide_fn_coin(G_ppng)
results_dir = os.path.join(work_dir['results'], 'coin-no-data')
SAVE        = True

if not os.path.exists(results_dir):
	os.mkdir(results_dir)

for no_data in ( ngram_gr, ppdb_gr, both_gr ):
	exec_coin('ppdb-ngram', no_data , decide_fn_coin(G_ppng ), results_dir, save = SAVE ) 
	exec_coin('ppdb'      , no_data , decide_fn_coin(G_ppdb ), results_dir, save = SAVE ) 
	exec_coin('ngram'     , no_data , decide_fn_coin(G_ngram), results_dir, save = SAVE )








