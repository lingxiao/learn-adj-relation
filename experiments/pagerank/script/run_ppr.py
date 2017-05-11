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

def exec_ppr(graph_name, graph, test_paths, alpha):

	_,_, ccb = no_data_pairs(test_paths['ccb'])
	_,_, moh = no_data_pairs(test_paths['moh'])
	_,_, bcs = no_data_pairs(test_paths['bcs'])

	prefix = 'ppr-' + str(alpha) + '-' + graph_name

	print('\n\t>> running ' + prefix)


	print('\n\t>> ranking ccb with ppdb-ngram graph ppr ...')
	rank_all_gold( ccb
		         , decide_ppr(graph, alpha)
		         , os.path.join(work_dir['results'], prefix + '-ccb.txt')
		         , refresh = False)

	print('\n\t>> ranking moh with ppdb-ngram graph ppr ...')
	rank_all_gold( moh
		         , decide_ppr(graph, alpha)
		         , os.path.join(work_dir['results'], prefix + '-moh.txt')
		         , refresh = False)

	print('\n\t>> ranking bcs with ppdb-ngram graph ppr ...')
	rank_all_gold( bcs
		         , decide_ppr(graph, alpha)
		         , os.path.join(work_dir['results'], prefix + '-bcs.txt')
		         , refresh = False)


	return ccb, moh, bcs

############################################################
'''
	run
'''
def exec_all(alpha):

	salpha = str(alpha)

	print('\n\t>>  running ppdb-ngram')	
	graph      = Graph('ppdb-ngram|uniform|' + salpha
					  , asset_dirs)
	graph_name = 'both-out-neigh'
	exec_ppr(graph_name, graph, both_gr, alpha)

	graph      = Graph('ppdb-ngram|edge-wt|' + salpha
					  , asset_dirs)
	graph_name = 'both-out-edge'
	exec_ppr(graph_name, graph, both_gr, alpha)

	print('\n\t>> running ppdb ')
	graph      = Graph('ppdb|uniform|' + salpha
					  , asset_dirs)
	graph_name = 'ppdb-out-neigh'
	exec_ppr(graph_name, graph, ppdb_gr, alpha)

	graph      = Graph('ppdb|edge-wt|' + salpha
					  , asset_dirs)
	graph_name = 'ppdb-out-edge'
	exec_ppr(graph_name, graph, ppdb_gr, alpha)

	print('\n\t>> running ngram ')
	graph      = Graph('ngram|uniform|' + salpha
					  , asset_dirs)
	graph_name = 'ngram-out-neigh'
	exec_ppr(graph_name, graph, ngram_gr, alpha)

	graph      = Graph('ngram|edge-wt|' + salpha
					  , asset_dirs)
	graph_name = 'ngram-out-edge'
	exec_ppr(graph_name, graph, ngram_gr, alpha)


exec_all(0.2)
# exec_all(0.8)
# exec_all(0.9)
# exec_all(0.5)


