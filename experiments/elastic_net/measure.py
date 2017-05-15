############################################################
# Module  : inference with elastic baseline
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os
import math
import numpy as np
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
	@Use: use model to predict 
'''	
def Pr_s_le_t_model(model,phi):

	eps = 1e-3

	def fn(s,t):
		yhat = model.predict(phi(s,t))
		if yhat > 0.5 : p = 0.5 + eps
		else: p = 0.5 - eps

		return p

	return fn

'''
	@Use: baseline Pr[ s < t ] using just pointwise esitmation
'''
def Pr_s_le_t(G):

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
	@Use: combine measures
'''
def Pr_s_le_t_combo(G, model, phi):

	real  = Pr_s_le_t(G)
	model = Pr_s_le_t_model(model,phi)

	def fn(s,t):
		prob = real(s,t)
		if prob == 0.5:
			return model(s,t)
		else:
			return prob

	return fn

############################################################
'''
	Decision Functions

	@Use: pick out algo from gold
'''
def decide_fn_model(model, phi):
	def fn(gold):
		return argmax_Omega(join(gold), Pr_s_le_t_model(model,phi))
	return fn

def decide_fn_both(G,model,phi):
	def fn(gold):
		return argmax_Omega(join(gold), Pr_s_le_t_combo(G,model,phi))
	return fn







