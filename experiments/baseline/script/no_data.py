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
from experiments.baseline.server import *

############################################################
'''
	get no data pairs
'''
ngram_gr = { 
      'ccb': os.path.join( work_dir['no-data']
      	                 , 'baseline-ngram-ccb-no-data.pkl'),

      'moh': os.path.join( work_dir['no-data']
      	                 , 'baseline-ngram-moh-no-data.pkl'),

      'bcs': os.path.join( work_dir['no-data']
      	                 , 'baseline-ngram-bcs-no-data.pkl')
	   }     

ppdb_gr = { 

      'ccb': os.path.join( work_dir['no-data']
      	                 , 'baseline-ppdb-ccb-no-data.pkl'),

      'moh': os.path.join( work_dir['no-data']
      	                 , 'baseline-ppdb-moh-no-data.pkl'),

      'bcs': os.path.join( work_dir['no-data']
      	                 , 'baseline-ppdb-bcs-no-data.pkl')
	   }     


both_gr = { 

      'ccb': os.path.join( work_dir['no-data']
      	                 , 'baseline-ppdb-ngram-ccb-no-data.pkl'),

      'moh': os.path.join( work_dir['no-data']
      	                 , 'baseline-ppdb-ngram-moh-no-data.pkl'),

      'bcs': os.path.join( work_dir['no-data']
      	                 , 'baseline-ppdb-ngram-bcs-no-data.pkl')
	   }     

############################################################
'''
	run test across all measures
'''
def from_label(pair_labels):

	pairs, labels = pair_labels

	test_format = []

	for (s,t),y in zip(pairs, labels):
		if y: test_format.append([[s],[t]])
		else: test_format.append([[t],[s]])

	return test_format


'''
	@Use: Given graph dictionary from above containing
		subset of pairs of words where no data exist
		in the namesake graph, a decision function that ranks
		gold set, and a prefix to delimit the decision function
		and data set, rank

	@Input: - test_set :: Dict String Path
			- graph  :: Graph
			- decide :: [[String]] -> Dict String _
			- prefix :: String
	@Output: IO ()
			 save to results directory			
'''
def rank_all(test_set, graph, decide, prefix):

	ccb   = from_label(no_data_pairs(test_set['ccb']))
	moh   = from_label(no_data_pairs(test_set['moh']))
	bcs   = from_label(no_data_pairs(test_set['bcs']))

	print('\n\t>> ranking ccb with ngram graph baseline ...')
	rank_all_gold( ccb
		         , decide(graph)
		         , os.path.join(work_dir['results'], prefix + '-ccb.txt')
		         , refresh = False)

	print('\n\t>> ranking moh with ngram graph baseline ...')
	rank_all_gold( moh
		         , decide(graph)
		         , os.path.join(work_dir['results'], prefix + '-moh.txt')
		         , refresh = False)

	print('\n\t>> ranking bcs with ngram graph baseline ...')
	rank_all_gold( bcs
		         , decide(graph)
		         , os.path.join(work_dir['results'], prefix + '-bcs.txt')
		         , refresh = False)

############################################################
'''
	run using all methods on graph on their respective test set
'''
def run_on_set(test_set, graph, suffix):

	rank_all( test_set
		    , graph
		    , decide_fn_uniform
		    , 'uniform-' + suffix
		    )	

	rank_all( test_set
		    , graph
		    , decide_fn
		    , 'baseline-' + suffix
		    )	

	rank_all( test_set
		    , graph
		    , decide_fn_shortest_path
		    , 'short-path-' + suffix
		    )

	rank_all( test_set
		    , graph
		    , decide_fn_neigh
		    , 'neigh-' + suffix
		    )


# run_on_set( ngram_gr, G_ngram , 'ngram')
# run_on_set( ppdb_gr, G_ppdb , 'ppdb')
# run_on_set( both_gr, G_ppng , 'ppdb-ngram')

# test_set = both_gr
# ccb   = from_label(no_data_pairs(test_set['ccb']))
# moh   = from_label(no_data_pairs(test_set['moh']))
# bcs   = from_label(no_data_pairs(test_set['bcs']))







