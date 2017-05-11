############################################################
# Module  : run test
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os
import struct
import pickle
import numpy as np
import networkx as nx
from numpy.linalg import inv

from app     import *
from utils   import *
from scripts import *
from scripts.graph import *
from experiments.pagerank import *


############################################################

def exec_uniform(graph, test_paths):

	_,_, ccb = no_data_pairs(test_paths['ccb'])
	_,_, moh = no_data_pairs(test_paths['moh'])
	_,_, bcs = no_data_pairs(test_paths['bcs'])


	print('\n\t>> ranking ccb with ppdb-ngram graph ppr ...')
	rank_all_gold( ccb
		         , decide_uniform(graph)
		         , os.path.join(work_dir['results'], 'uniform-ccb.txt')
		         , refresh = False)

	print('\n\t>> ranking moh with ppdb-ngram graph ppr ...')
	rank_all_gold( moh
		         , decide_uniform(graph)
		         , os.path.join(work_dir['results'], 'uniform-moh.txt')
		         , refresh = False)

	print('\n\t>> ranking bcs with ppdb-ngram graph ppr ...')
	rank_all_gold( bcs
		         , decide_uniform(graph)
		         , os.path.join(work_dir['results'], 'uniform-bcs.txt')
		         , refresh = False)


############################################################
'''
	run
'''
if True:
	graph = Graph('ppdb-ngram|uniform|0.8', asset_dirs)
	exec_uniform(graph, both_gr)



