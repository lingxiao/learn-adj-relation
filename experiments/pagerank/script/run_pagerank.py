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

def exec_pageRank(graph_name, pr, test_paths):

	_,_, ccb = no_data_pairs(test_paths['ccb'])
	_,_, moh = no_data_pairs(test_paths['moh'])
	_,_, bcs = no_data_pairs(test_paths['bcs'])


	print('\n\t>> ranking ccb with ppdb-ngram graph pagerank ...')
	rank_all_gold( ccb
		         , decide_pageRank(pr)
		         , os.path.join(work_dir['results'], 'pagerank-' + graph_name + '-ccb.txt')
		         , refresh = False)

	print('\n\t>> ranking moh with ppdb-ngram graph pagerank ...')
	rank_all_gold( moh
		         , decide_pageRank(pr)
		         , os.path.join(work_dir['results'], 'pagerank-' + graph_name + '-moh.txt')
		         , refresh = False)

	print('\n\t>> ranking bcs with ppdb-ngram graph pagerank ...')
	rank_all_gold( bcs
		         , decide_pageRank(pr)
		         , os.path.join(work_dir['results'], 'pagerank-' + graph_name + '-bcs.txt')
		         , refresh = False)


############################################################
'''
	run
'''
def exec_all(alpha):

	print('\n\t>> running ppdb-ngram graph ...')
	graph      = Graph('ppdb-ngram|uniform|0.8', asset_dirs)
	pr         = nx.pagerank(graph.graph, alpha = alpha)
	graph_name = 'both-out-neigh'
	exec_pageRank(graph_name, pr, both_gr)

	graph      = Graph('ppdb-ngram|edge-wt|0.8', asset_dirs)
	pr         = nx.pagerank(graph.graph, alpha = alpha)
	graph_name = 'both-out-edge'
	exec_pageRank(graph_name, pr, both_gr)

	print('\n\t>> running ppdb graph ...')
	graph      = Graph('ppdb|uniform|0.8', asset_dirs)
	pr         = nx.pagerank(graph.graph, alpha = alpha)
	graph_name = 'ppdb-out-neigh'
	exec_pageRank(graph_name, pr, ppdb_gr)

	graph      = Graph('ppdb|edge-wt|0.8', asset_dirs)
	pr         = nx.pagerank(graph.graph, alpha = alpha)
	graph_name = 'ppdb-out-edge'
	exec_pageRank(graph_name, pr, ppdb_gr)


	print('\n\t>> running ngram graph ...')
	graph      = Graph('ngram|uniform|0.8', asset_dirs)
	pr         = nx.pagerank(graph.graph, alpha = alpha)
	graph_name = 'ngram-out-neigh'
	exec_pageRank(graph_name, pr, ngram_gr)

	graph      = Graph('ngram|edge-wt|0.8', asset_dirs)
	pr         = nx.pagerank(graph.graph, alpha = alpha)
	graph_name = 'ngram-out-edge'
	exec_pageRank(graph_name, pr, ngram_gr)


exec_all(0.9)



