############################################################
# Module  : pick out pairs in baseline that had no information
#           construct new pairset 
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
from experiments.baseline import *


############################################################
'''
	@Use: given all paths to results
		  output subset of each result where there is no data

	@Input:  - in_path :: [String]
			 - out_dir :: String

	@Output: IO (Dict String [(String,String)])

		    output dictionary and write each dict to out_dir
'''

def make_all_no_data_pairs( in_paths, out_dir ):

	for in_path in in_paths:

		in_name   = in_path.split('/')[-1]
		in_name,_ = in_name.split('.')
		out_path_stem  = os.path.join(out_dir, in_name + '-no-data')

		print('\n\t>> find_no_data_pairs for ' + in_name)

		find_no_data_pairs( in_path, out_path_stem )

'''
	@Use: given in_path to results,
		  output subset of results where there is no data

	@Input:  - in_path  :: String
			 - out_path :: String

	@Output: IO (Dict String [(String,String)])

		    output dictionary and write it to out_path
'''
def find_no_data_pairs( in_path, out_path_stem ):

	with open(in_path,'rb') as h:
		test = pickle.load(h)

	no_data = dict()

	for n,cluster in test['ranking'].iteritems():

		pairs = to_le_than(cluster['gold'])
		no_data_pairs = []

		for s,t,p in cluster['raw']['link-probs']:
			if p == 0.5:
				if (s,t) in pairs:
					no_data_pairs.append((s,t))
				celse:
					no_data_pairs.append((t,s))

		if no_data_pairs:
			no_data[n] = no_data_pairs

	write_gold(out_path_stem + '.txt', no_data)

	with open(out_path_stem + '.pkl','wb') as h:
		pickle.dump(no_data, h)

	return no_data

############################################################
'''
	Utils

	@Use: given test set of form: [test1, test2, ...]
		  where test_i = [[w1],[w2],[w3,w4],...]
		  so that w < w2 < (w3 = w4) < ...
		  turn into a list of pairs so that the first
		  word in the pair is weaker than second, ie:
		  [(w1,w2),(w1,w3),(w2,w3),(w2,w4),...]

	@Input : golds :: [[String]]	

	@output: pairs :: [(String,String)]
'''
def to_le_than(golds):
	return go_le_than(golds,[])

def go_le_than(golds, pairs):
	if golds == []:
		return pairs
	else:
		head = golds[0]
		tail = golds[1:]

		pairs1 = join([(s,t) for s in head for t in elem] \
			     for elem in tail)

		return go_le_than(tail, pairs + pairs1)		


############################################################
'''
	construct all no-data pairs
'''
stem        = 'baseline'
graph_names = ['ppdb','ngram','ppdb-ngram']
test_names  = ['ccb', 'moh','bcs']

names = [ stem + '-' + g + '-' + t for g in graph_names for t in test_names]
paths = [ os.path.join(work_dir['results'],p + '.pkl') for p in names ]

make_all_no_data_pairs( paths, work_dir['no-data'] )



