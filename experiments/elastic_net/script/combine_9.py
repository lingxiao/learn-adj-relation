############################################################
# Module  : combine models run on anne's data set
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

data_set  = 'ppdb-ngram-1'
num_neigh = 10

fix, nu = 'HT' , nu_coin( GRAPH[data_set], num_neigh )
OP , op = '-'  , vec_subtract
phi     = to_x(nu,op)

SAVE    = False

words  = join(join(anne_cluster['anne-25']))
bwords = [w for w in join(join(anne_cluster['anne-125'])) if w not in G_ppng.vertices]

############################################################
'''
	run on all data set
'''
results_dir = os.path.join(work_dir['results'], 'combined/' + winner)

if not os.path.exists(results_dir):
	os.mkdir(results_dir)
	
if False:
	exec_rank( data_set
		     , anne_cluster
		     , decide_fn_both(G_ppng, model, phi)
		     , results_dir
		     , save = SAVE
		     ) 

