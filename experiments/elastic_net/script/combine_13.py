############################################################
# Module  : combine models with beta prior measure
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os
import math
import numpy as np
import networkx as nx
from sklearn.metrics import r2_score
from sklearn.linear_model import ElasticNet
import scipy.stats
import pickle


from app     import *
from utils   import *
from scripts import *
from scripts.graph import *
from experiments.argmax import *
from experiments.rank_all import *
from experiments.elastic_net import *

from scipy.stats import binom, beta
from scipy.misc import comb

############################################################
'''
	model and feature space representation
'''
winner = 'logistic-regression-beta-binomial|ppdb-ngram-1|[nu^HT(s)`o`nu^HT(t)]|num_neigh=10|penalty=l1|C=0.1num_tosses=100'
path   = os.path.join(work_dir['results'],winner + '/model')
	
print('\n\t>> loading model from ' + winner)
with open(path,'rb') as h:
	model = pickle.load(h)

data_set   = 'ppdb-1'
num_neigh  = 10
num_tosses = 5

fix, nu = 'HT' , nu_coin( GRAPH[data_set], num_neigh )
OP , op = '`o`', vec_concat
phi     = to_x(nu,op)

SAVE = True

############################################################
'''
	run on all data set
'''
results_dir = os.path.join(work_dir['results'], 'combined/' + winner + '|infer_tosses=' + str(num_tosses))

if not os.path.exists(results_dir):
	os.mkdir(results_dir)
	
if True:
 	exec_rank( data_set
		     , test
		     , decide_fn_both_binomial(G_ppdb, model, phi, num_tosses)
		     , results_dir
		     , save = SAVE
		     ) 





