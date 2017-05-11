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
winner = 'ppdb-ngram-1|[phi^out(s)-phi^out(t)]|num_adv=2|alpha=0.9|l1=0.9'
path   = os.path.join(work_dir['results'],winner + '/model')

print('\n\t>> loading model from ' + winner)
with open(path,'rb') as h:
	model = pickle.load(h)

num_adv    = 2
data_set   = 'ppdb-ngram-1'

w2idx_path = os.path.join( work_dir['assets']
	                     , 'w2idx-' + str(num_adv) + '.pkl')

print('\n\t>> loading word to index')
with open(w2idx_path,'rb') as h:
	w2idx = pickle.load(h)

print('\n\t>> constructing feature functions')
fix, rho  = 'o'  , rho_out( GRAPH[data_set], w2idx )
OP , op   = '-'  , rho_subtract
phi       = to_x(rho,op)

SAVE = True

############################################################
'''
	run on all data set
'''
decide      = decide_fn_both(G_ppng, model, phi)
results_dir = os.path.join(work_dir['combined'], winner)

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


