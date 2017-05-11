############################################################
# Module  : compute results by expected value as a baseline
#           on ppdb data
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import shutil
import pickle
import operator
from collections import Counter

from app     import *
from utils   import *
from scripts import *
from scripts.graph import *
from experiments import *
from experiments.elementary.top import *

############################################################
'''
	paths and directories
'''
measure_names = [p + '-' + q + r  
	            for p in ['coin','die']  \
	            for q in [ 'ngram'
	                     , 'ngram-bool'
	                     , 'ppdb'
	                     , 'ppdb-ngram'
	                     , 'ppdb-ngram-bool']
	            for r in ['-smooth', '']]

ev_dirs   = data_dirs( 'expected-value' , measure_names )


'''
	make results directory if it does not exist
	remove existing results if it does
'''
result_root = os.path.join(get_path('elementary'), 'results')
result_dir = locate_dirs( result_root, measure_names, rewrite = False )

############################################################
'''
	training data
'''
print('\n\t>> load base-comparative-superlative')
bcs = join(_xs for _, _xs in train_vertices(get_path('bcs')).iteritems())
bcs = [[[w] for w in _ws] for _ws in bcs]

print('\n\t>> load turk')
ccb = read_gold(get_path('ccb'))

print('\n\t>> load moh')
moh = read_gold(get_path('moh'))

############################################################
'''
	load all measures
'''
print('\n\t>> loading all measures')

measure_probs = dict()

for name, path in ev_dirs.iteritems():
	measure_probs[name] = load_probs_table(path)

############################################################
'''
	@Use: run experiment on `test_set`
	      for all possible measures over all graphs
'''
def exec_each_experiment(test_set, test_name):

	for measure_name in measure_names:

		print('\n\t>> computing results for ' + measure_name)

		measure   = measure_probs[measure_name]
		out_stem  = os.path.join(result_dir[measure_name],test_name)

		stem = measure_name.split('-')[0]

		if stem == 'coin':
			prob_fn_1, out_suffix_1 = decide_coin    (measure), '-prob.txt'
			prob_fn_2, out_suffix_2 = decide_coin_bet(measure), '-bet.txt'

			decide(test_set, prob_fn_1, out_stem +  out_suffix_1)
			decide(test_set, prob_fn_2, out_stem +  out_suffix_2)

		elif stem == 'die':

			prob_fn_1, out_suffix_1 = decide_die    (measure), '-prob.txt'
			prob_fn_2, out_suffix_2 = decide_die_bet(measure), '-bet.txt'

			decide(test_set, prob_fn_1, out_stem +  out_suffix_1)
			decide(test_set, prob_fn_2, out_stem +  out_suffix_2)


for test_set, test_name in [(bcs,'bcs'), (ccb, 'ccb'),(moh, 'moh')]:
	exec_each_experiment(test_set, test_name)


