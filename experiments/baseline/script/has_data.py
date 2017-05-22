############################################################
# Module  : pointwise estimation baseline for those with data
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
from experiments.elastic_net.server import no_data_pairs

############################################################
'''
	Load data
'''

root_dir = work_dir['has-data']
prefix   = 'baseline'
data_set = ['ngram','ppdb', 'ppdb-ngram']
gold_set = ['bcs', 'ccb', 'moh']
suffix   = 'has-data'

names    = [prefix + '-' + d + '-' + g + '-' + suffix \
           for d in data_set for g in gold_set]

paths    = [(p,os.path.join(root_dir, p + '.pkl')) for p in names]


ppdb_test = { name: no_data_pairs(path)[2] \
              for name,path in paths if 'ppdb' in path \
              and 'ppdb-ngram' not in path }


ngram_test = { name: no_data_pairs(path)[2] \
              for name,path in paths if 'ngram' in path \
              and 'ppdb-ngram' not in path }

ppng_test = { name: no_data_pairs(path)[2] \
              for name,path in paths if 'ppdb-ngram' in path }

debug = {name : no_data_pairs(path)[2][0:5] for name,path in paths \
        if 'ppdb' in path and 'ppdb-ngram' not in path }

############################################################
'''
	make directory and run baseline using ppdb-ngram graph
'''
out_dir = os.path.join(work_dir['results'], 'has-data')

if not os.path.exists(out_dir):
	os.mkdir(out_dir)

def run_has_data(test_set, data_name, out_root):

	if data_name in ['ppdb', 'debug']:
		G = G_ppdb
	elif data_name == 'ppdb-ngram':
		G = G_ppng
	elif data_name == 'ngram':
		G = G_ngram

	print('\n\t>> using dataset: ' + data_name)	

	for name, test in test_set.iteritems():
		print('\n\t>> ranking ' + name + ' with ' + data_name + ' graph ...')
		rank_all_gold( test
			         , decide_fn(G)
			         , os.path.join(out_root, name + '-' + data_name + '.txt')
			         , refresh = False
			         , save = True
			         )

if True:
	run_has_data(ppdb_test , 'ppdb'      , out_dir)
	run_has_data(ppng_test , 'ppdb-ngram', out_dir)
	run_has_data(ngram_test, 'ngram'     , out_dir)

