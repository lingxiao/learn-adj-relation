############################################################
# Module  : elastic net regression
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
	data server
'''

train_X, train_y = train_pairs(bcs)
test_X , test_y  = test_pairs (moh)
test_no_tie_X, test_no_tie_y  = train_pairs (moh)

############################################################
'''
	Feature Parameters and representations

	graph set used
'''
GRAPH = {
          'ppdb'       : G_ppdb
		 ,'ngram'      : G_ngram
		 ,'ppdb-ngram' : G_ppng
		 }

'''
	number of adverbs in feature representation
'''
num_adv = 200

'''
	feature representation
'''
graph    = 'ppdb'

w2idx_path = os.path.join( work_dir['assets']
	                     , 'w2idx-' + str(num_adv) + '.pkl')
idx2w_path = os.path.join( work_dir['assets']
	                     , 'idx2w-' + str(num_adv) + '.pkl')


print('\n\t>> [ using graph ' 
	 + graph 
	 + ' and ' 
	 + str(num_adv) 
	 + ' adverbs as rho(s) ]'
	 ) 

with open(w2idx_path,'rb') as h:
	w2idx = pickle.load(h)

with open(idx2w_path,'rb') as h:
	idx2w = pickle.load(h)

# rho = rho_adv_concat_in_out( GRAPH[graph], w2idx )
# rho = rho_adv_subtract_in_out( GRAPH[graph], w2idx )
# rho = rho_head_tail( GRAPH[graph], w2idx )
# rho = rho_adv_in( GRAPH[graph], w2idx )
rho = rho_adv_out( GRAPH[graph], w2idx )

op  = rho_subtract

stem        = 'baseline'
graph_names = ['ppdb','ngram','ppdb-ngram']
test_names  = ['ccb', 'moh','bcs']

names    = [ stem + '-' + g + '-' + t for g in graph_names for t in test_names]
in_paths = [ os.path.join(baseline_dir['no-data'],p + '-no-data.pkl') for p in names ]

in_path = in_paths[0]


############################################################
'''
	Elastic Net
'''
alpha    = 0.8
l1_ratio = 0.8

'''
	Train 
'''
if True:
	X    = to_X(train_X, rho, op)
	y    = np.array(train_y)

	print('\n\t>> training model ...')
	model  = ElasticNet( alpha = alpha, l1_ratio = l1_ratio)
	model  = model.fit(X, y)

	'''
		sanity check accuracies
	'''
	sanity = sanity_check(op,rho,model)

	print('\n>> training results')
	sanity( train_X, train_y )

	print('\n>> test results')
	sanity( test_X , test_y, log = False )

	print('\n>> test no tie results')
	sanity( test_no_tie_X, test_no_tie_y )

vector = model.coef_

print('\n\t>> decoding coefficients of model')
coefs = decode(vector,w2idx)

