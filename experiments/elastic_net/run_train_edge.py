############################################################
# Module  : run train elastic net regression using edge features
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
alpha      = 0.9
l1_ratio   = 0.9

num_adv    = 2
# data_set   = 'ppdb-ngram'
data_set   = 'ppdb-ngram-1'

w2idx_path = os.path.join( work_dir['assets']
	                     , 'w2idx-' + str(num_adv) + '.pkl')

with open(w2idx_path,'rb') as h:
	w2idx = pickle.load(h)

fix, rho = 'out' , rho_out( GRAPH[data_set], w2idx )
OP , op  = '-'   , vec_subtract
phi      = to_x(rho,op)
SAVE     = True

############################################################
'''
	train and validation data 
'''
if data_set in ['ppdb-ngram', 'ppdb-ngram-1']:
	test = both_gr
elif data_set in ['ppdb', 'ppdb-1'] :
	test = ppdb_gr
elif data_set == 'ngram':
	test = ngram_gr

G = G_ppng_1
s = 'good'
top_n = 10

n_in, n_out = get_neighbor(G, 10, 'great')

###########################################################
'''
	Train 
'''
dir_name = data_set   + '|'                 \
         + '[phi^'+ fix + '(s)' + OP + 'phi^' + fix + '(t)]|'  \
         + 'num_adv=' + str(num_adv) + '|'  \
         + 'alpha='   + str(alpha)   + '|'  \
         + 'l1='      + str(l1_ratio)   

if False:
	print('\n\t>> Training ' + dir_name)
	exec_train( dir_name = dir_name

		      , alpha    = alpha
		      , l1_ratio = l1_ratio

		      , rho      = rho
		      , op       = op
		      , w2idx    = w2idx

		      , train    = no_data_pairs (test['bcs'])
		      , valid    = no_data_pairs (test['ccb'])
		      , test     = no_data_pairs (test['moh'])

		      , out_root = work_dir['results']
		      , save     = SAVE

		      )








