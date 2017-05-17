############################################################
# Module  : run train penalized logistic regression 
#           using neighbor features and binomial prior
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os
import math
import numpy as np
import networkx as nx
from sklearn.metrics import r2_score
from sklearn.linear_model import ElasticNet, LogisticRegression
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
model      = 'logistic-regression-beta-binomial'

# elastic net regularization
alpha      = 0.9
l1_ratio   = 0.1

# logistic regression regularization
penalty    = 'l1'
C          = 0.1
num_tosses = 100

# data set to train the model on
# and the size of feature represenation
data_set   = 'ppdb-ngram-1'
num_neigh  = 10

w2idx    = {'neig-' + str(k) : {'idx': k} \
           for k in xrange(num_neigh)}

# feature representation function
fix, nu  = 'HT' , nu_coin( GRAPH[data_set], num_neigh )
OP , op  = '`o`'  , vec_concat
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
if model == 'logistic-regression-beta-binomial':
	dir_name = model        + '|'                                 \
	         +  data_set    + '|'                                 \
	         + '[nu^'+ fix  + '(s)' + OP + 'nu^' + fix + '(t)]|'  \
	         + 'num_neigh=' + str(num_neigh) + '|'                \
	         + 'penalty='   + penalty        + '|'                \
	         + 'C='         + str(C)         + '|'                \
	         + 'num_tosses=' + str(num_tosses)
else:
	raise NameError('Expected elastic-net or logistic-regression')	         

if True:
	print('\n\t>> Training ' + dir_name)
	exec_train( dir_name = dir_name

			  , model    = model

		      , alpha    = alpha
		      , l1_ratio = l1_ratio

		      , penalty  = penalty
		      , C        = C
		      , num_tosses = num_tosses

		      , rho      = nu
		      , op       = op
		      , w2idx    = w2idx

		      , train    = no_data_pairs (test['bcs'])
		      , valid    = no_data_pairs (test['ccb'])
		      , test     = no_data_pairs (test['moh'])

		      , out_root = work_dir['results']
		      , save     = SAVE

		      )








