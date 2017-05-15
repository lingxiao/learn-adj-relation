############################################################
# Module  : combine models
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os
import math
import numpy as np
import networkx as nx
from sklearn.metrics import r2_score
from sklearn.linear_model import ElasticNet
import pickle


from app     import *
from utils   import *
from scripts import *
from scripts.graph import *
from experiments.argmax import *
from experiments.rank_all import *
from experiments.elastic_net import *


############################################################
'''
	model and feature space representation
'''
winner = 'ppdb-ngram-1|[nu^io(s)-nu^io(t)]|num_neigh=50|alpha=0.5|l1=0.1'
path   = os.path.join(work_dir['results'],winner + '/model')
	
print('\n\t>> loading model from ' + winner)
with open(path,'rb') as h:
	model = pickle.load(h)

num_adv    = 2
data_set   = 'ppdb-ngram-1'
num_neigh  = 50

w2idx    = {'neig-' + str(k) : {'idx': k} \
           for k in xrange(num_neigh)}

fix, nu  = 'io' , nu_in_out_concat( GRAPH[data_set], num_neigh )
OP , op  = '-'  , vec_subtract
phi      = to_x(nu,op)

SAVE = True

############################################################
'''
	run on all data set
'''
decide      = decide_fn_both(G_ppng, model, phi)
results_dir = os.path.join(work_dir['results'], 'combined/' + winner)


print('\n\t>> ranking moh-ppdb with ppdb-ngram graph ...')
rank_all_gold( test['moh-ppdb']
	         , decide
	         , os.path.join(results_dir, 'moh-ppdb.txt')
	         , refresh = False
	         , save    = SAVE )

if False:

	print('\n\t>> ranking moh-no-ties with ppdb-ngram graph ...')
	rank_all_gold( test['moh-no-tie']
		         , decide
		         , os.path.join(results_dir, 'moh-no-tie.txt')
		         , refresh = False
		         , save    = SAVE )


	print('\n\t>> ranking ccb-no-ties with ppdb-ngram graph ...')
	rank_all_gold( test['ccb-no-tie']
		         , decide
		         , os.path.join(results_dir, 'ccb-no-tie.txt')
		         , refresh = False
		         , save    = SAVE )

	print('\n\t>> making directory ' + results_dir)
	if not os.path.exists(results_dir):
		os.mkdir(results_dir)

	print('\n\t>> ranking bcs with ppdb-ngram graph ...')
	rank_all_gold( test['bcs']
		         , decide
		         , os.path.join(results_dir, 'bcs.txt')
		         , refresh = False
		         , save    = SAVE )

	print('\n\t>> ranking ccb with ppdb-ngram graph ...')
	rank_all_gold( test['ccb']
		         , decide
		         , os.path.join(results_dir, 'ccb.txt')
		         , refresh = False
		         , save    = SAVE )

	print('\n\t>> ranking moh with ppdb-ngram graph ...')
	rank_all_gold( test['moh']
		         , decide
		         , os.path.join(results_dir, 'moh.txt')
		         , refresh = False
		         , save    = SAVE )












