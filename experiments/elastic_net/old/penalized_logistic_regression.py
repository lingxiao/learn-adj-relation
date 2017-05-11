############################################################
# Module  : l1 and l2 penalized logistic regression
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
test_X , test_y  = test_pairs (ccb)
test_no_tie_X, test_no_tie_y  = train_pairs (ccb)

############################################################
'''
	Feature Parameters and representations

	a vector where adverbs appearing more than adv_thresh
	are kept
'''
adv_thresh = 200

'''
	data set used
'''
GRAPH = {'ppdb'       : G_ppdb
		 ,'ngram'     : G_ngram
		 ,'ppdb-ngram': G_ppng
		 }

'''
	feature representation
'''
graph    = 'ngram'
adv_path = os.path.join(work_dir['assets'], 'adverb>' + str(adv_thresh) + '.pkl')

print( '\n>> constructing rho using ' + graph )

# rho = rho_adv_concat_in_out( GRAPH[graph], adv_path )
# rho = rho_adv_subtract_in_out( GRAPH[graph], adv_path )
# rho = rho_head_tail( GRAPH[graph], adv_path )

rho = rho_adv_out( GRAPH[graph], adv_path )

op  = rho_subtract

############################################################
'''
	Elastic Net
'''
alpha = 0.8

def exec_train():

	'''
		Train 
	'''
	X    = to_X(train_X, rho, op)
	y    = np.array(train_y)

	model  = ElasticNet( alpha = alpha, l1_ratio = 0.8 )   
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


exec_train()



