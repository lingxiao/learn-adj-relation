############################################################
# Module  : train elastic net regression
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
	@Use: train validate and test model. save results if needed
'''

def exec_train( dir_name = None

	          , model    = ''
	          , alpha    = None
	          , l1_ratio = None

	          , penalty  = ''
	          , C        = None

	          , rho      = None
	          , op       = None
	          , w2idx    = None

	          , train    = None
	          , valid    = None
	          , test     = None

	          , out_root = None
	          , save     = False ):

	train_X, train_y, train_gold = train
	valid_X, valid_y, valid_gold = valid
	test_X , test_y , test_gold  = test
	
	X = to_X(train_X, rho, op, normalize = False)
	y = np.array(train_y)

	print('\n\t>> training model ' + model + ' ...')
	
	if model == 'elastic-net':

		print('\n\t >> running ' + model + ' with alpha = ' + str(alpha) + ' and l1-ratio = ' + str(l1_ratio))
		model = ElasticNet( alpha = alpha, l1_ratio = l1_ratio)
		model = model.fit(X, y)

	elif model == 'logistic-regression':

		print('\n\t >> running ' + model + ' with penalty ' + penalty + ' at C = ' + str(C))
		model = LogisticRegression(C = C, penalty = penalty)
		model = model.fit(X, y)

	results_dir = ''
	phi = to_x(rho, op)

	print('\n\t>> decoding coefficients of model')
	vector = model.coef_

	if len(vector) == len(w2idx):
		coefs  = decode(vector,w2idx)		
		print('\n\t>> coefficents: ')
		for w,v in coefs.iteritems():
			print('\n\t\t ' + w + ': ' + str(v))
	else:
		coefs = {k:c for k,c in enumerate(vector)}
		print('\n\t\t >> coefficents: ' + str(coefs))

	if save:

		results_dir = os.path.join(out_root, dir_name)

		print('\n\t>> saving results to ' + dir_name)
		if not os.path.exists(results_dir):
			os.mkdir(results_dir)		

		m_path = os.path.join( results_dir, 'model' )

		print('\n\t>> saving model ')
		pickle.dump(model, open(m_path, 'wb'))	

		print('\n\t>> saving coefficients ...')
		with open(os.path.join(results_dir, 'coef.txt'),'wb') as h:
			for v,n in coefs.iteritems():
				h.write(str(v) + ': ' + str(n) + '\n')		

	print('\n\t>> ranking bcs with ppdb-ngram graph ...')
	rank_all_gold( train_gold
		         , decide_fn_model(model, phi)
		         , os.path.join(results_dir, 'bcs.txt')
		         , refresh = False
		         , save    = save )

	print('\n\t>> ranking ccb with ppdb-ngram graph ...')
	rank_all_gold( valid_gold
		         , decide_fn_model(model, phi)
		         , os.path.join(results_dir, 'ccb.txt')
		         , refresh = False
		         , save    = save )

	print('\n\t>> ranking moh with ppdb-ngram graph ...')
	rank_all_gold( test_gold
		         , decide_fn_model(model, phi)
		         , os.path.join(results_dir, 'moh.txt')
		         , refresh = False
		         , save    = save )












