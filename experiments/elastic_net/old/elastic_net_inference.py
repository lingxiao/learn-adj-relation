############################################################
# Module  : inference with elastic baseline
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os
import math
import numpy as np
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
	Load Elastic Net
'''
alpha    = 0.2
l1_ratio = 0.8

model_name = 'bcs-'        \
           + 'ppdb-ngram'  \
           + '-'           \
           + 'alpha='      \
           + str(alpha)    \
           + '-'           \
           + 'l1_ratio='   \
           + str(l1_ratio) \
		   + '.sav'

m_path = os.path.join( work_dir['models'], model_name )
model  = pickle.load (open(m_path, 'rb'))

graph  = GRAPH['ppdb-ngram']

'''	
	make representation function :: String -> String -> np.array
'''
s,t  = 'bad', 'horrific'
phi  = to_x(rho,op)
yhat = model.predict(phi(s,t))

############################################################
'''
	@Use: baseline Pr[ s < t ] using just pointwise esitmation
	      plus model when there's no data
'''
def Pr_s_le_t_coin(G):

	def fn(s,t):

		s_ge_t = 0.0
		s_le_t = 0.0

		if t in G.out_neigh(s):
			s_le_t += sum(n for _,n in G.out_neigh(s)[t].iteritems())
			
		if t in G.in_neigh(s):
			s_ge_t += sum(n for _,n in G.in_neigh(s)[t].iteritems())

		s_ge_t = max(1e-5,s_ge_t)	
		s_le_t = max(1e-5,s_le_t)	

		return s_le_t/(s_ge_t + s_le_t)

	return fn


'''
	@Use: shameless combine measures
'''
def Pr_s_le_t_coin_net(G):

	def fn(s,t):

		eps = 1e-3
		p = Pr_s_le_t_coin(G)(s,t)

		if p == 0.5:
			yhat = model.predict(phi(s,t))
			if yhat > 0.5: p = 0.5 + eps
			else: p = 0.5 - eps

		return p

	return fn

############################################################
'''
	Decision Functions

	@Use: pick out algo from gold
'''
def decide_fn_coin_net(G):
	def fn(gold):
		return argmax_Omega(join(gold), Pr_s_le_t_coin_net(G))
	return fn

'''
	@Use: pick out algo from gold using baseline alone
'''
def decide_fn_coin(G):
	def fn(gold):
		return argmax_Omega(join(gold), Pr_s_le_t_coin(G))
	return fn











