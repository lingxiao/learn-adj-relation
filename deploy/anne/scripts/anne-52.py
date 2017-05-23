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
winner = 'logistic-regression|ppdb-ngram-1|[nu^HT(s)-nu^HT(t)]|num_neigh=10|penalty=l1|C=0.4'
path   = os.path.join(work_dir['results'],winner + '/model')
	
print('\n\t>> loading model from ' + winner)
with open(path,'rb') as h:
	model = pickle.load(h)

data_set   = 'ppdb-ngram-1'
num_neigh  = 10

fix, nu = 'HT' , nu_coin( GRAPH[data_set], num_neigh )
OP , op = '-'  , vec_subtract
phi     = to_x(nu,op)

SAVE    = True

############################################################
'''
	load data and deploy root
'''
dirs  = working_dirs('anne',['scripts','shells', 'results-ppdb-1', 'results-ppdb-ngram-1'])
anne  = get_path('anne')
files = [ p for p in os.listdir(anne) if '.txt' in p ]
			
############################################################
'''
	open current batch
'''
batch = 52
path        = os.path.join(anne, 'cluster-' + str(batch) + '.txt')
golds       = read_gold(path)
results_dir = dirs['results-' + data_set]

readme = 'model:\t\t' + winner              + '\n' \
	   + 'inference data set:\t' + data_set + '\n' \
	   + 'inference tosses:\t1'             + '\n' \
	   + 'goldset:\t anne'

with open( os.path.join(results_dir,'readme.txt'), 'wb' ) as h:
	h.write(readme)

if True:
	out_path    = os.path.join(dirs['results-' + data_set], 'anne-' + str(batch) + '.txt')
	decision_fn = decide_fn_both_binomial(G_ppng, model, phi)
	rank_all_gold( golds, decision_fn, out_path, refresh = False, save = True )








