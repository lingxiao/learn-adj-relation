############################################################
# Module  : elastic net regression
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os
import math
import numpy as np
import pickle
from sklearn.linear_model import ElasticNet


from app     import *
from utils   import *
from scripts import *
from scripts.graph import *
from experiments.argmax import *
from experiments.rank_all import *
from experiments.elastic_net import *

############################################################
'''
	train and test data
'''

print('\n\t>> [ training data is base-comparative-superlative ]')
train_X, train_y = train_pairs(bcs)

'''
	test data set is the set of pairs where
	no data exists for baseline
'''
baseline_dir = locate_dirs( get_path('baseline'), ['no-data'] )
stem         = 'baseline'
graph_names  = ['ppdb','ngram','ppdb-ngram']
test_names   = ['ccb', 'moh','bcs']

names        = [ stem + '-' + g + '-' + t for g in graph_names for t in test_names]
in_paths     = [ os.path.join(baseline_dir['no-data'],p + '-no-data.pkl') for p in names ]

test_set = -2

print('\n\t>> [ Using test data pairs from ' + names[test_set] + ' ]')
test_X, test_y = no_data_pairs(in_paths[test_set])

############################################################
'''
	Elastic Net
'''
alpha    = 0.2
l1_ratio = 0.8

model_name = 'bcs-'   \
           + data_set   \
           + '-'      \
           + 'alpha='     \
           + str(alpha)   \
           + '-'           \
           + 'l1_ratio='   \
           + str(l1_ratio) \
		   + '.sav'

'''
	Train 
'''
def train_model():

	X    = to_X(train_X, rho, op)
	y    = np.array(train_y)

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

	print('\n\t>> decoding coefficients of model')
	coefs = decode(model.coef_,w2idx)

	print('\n\t>> saving coefficient to desktop')
	with open('/Users/lingxiao/Desktop/coef.txt','wb') as h:
		for v,n in coefs.iteritems():
			h.write(v + ': ' + str(n) + '\n')

	m_path = os.path.join( work_dir['models'], model_name )

	print('\n\t>> saving model ' + model_name)			
	pickle.dump(model, open(m_path, 'wb'))

	return model

net = train_model()	

'''	
	sanity check
'''
s,t = 'good', 'excellent'
phi = to_x(rho,op)
yhat = net.predict(phi(s,t))






























