############################################################
# Module  : run train elastic net regression using neighbor features
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
	Training config
'''
alpha      = 0.5
l1_ratio   = 0.1

num_adv    = 2
data_set   = 'ppdb-ngram-1'
num_neigh  = 15

w2idx    = {'neig-' + str(k) : {'idx': k} \
           for k in xrange(num_neigh)}

fix, nu  = 'io' , nu_in_out_concat( GRAPH[data_set], num_neigh )
OP , op  = '-'  , vec_subtract
phi      = to_x(nu,op)
SAVE     = False

############################################################
'''
	train and validation data 
'''
if data_set in ['ppdb-ngram', 'ppdb-ngram-1']:
	test = both_gr
elif data_set in ['ppdb', 'ppdb-1']:
	test = ppdb_gr
elif data_set == 'ngram':
	test = ngram_gr

###########################################################
'''
	Train 
'''
dir_name = data_set     + '|'                 \
         + '[nu^'+ fix  + '(s)' + OP + 'nu^' + fix + '(t)]|'  \
         + 'num_neigh=' + str(num_neigh) + '|'  \
         + 'alpha='     + str(alpha)   + '|'  \
         + 'l1='        + str(l1_ratio)   

if True:
	print('\n\t>> Training ' + dir_name)
	exec_train( dir_name = dir_name

		      , alpha    = alpha
		      , l1_ratio = l1_ratio

		      , rho      = nu
		      , op       = op
		      , w2idx    = w2idx

		      , train    = no_data_pairs (test['bcs'])
		      , valid    = no_data_pairs (test['ccb'])
		      , test     = no_data_pairs (test['moh'])

		      , out_root = work_dir['results']
		      , save     = SAVE

		      )








