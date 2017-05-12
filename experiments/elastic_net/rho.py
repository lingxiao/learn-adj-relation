############################################################
# Module  : feature representation rho based on edges
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import math
import numpy as np
from scripts import *
from scripts.graph import *

############################################################
'''
	@Use: given set of pairs and feature representation function
		  rho of each word, and a function that combines
		  the pair of words, output the X matrix
	@Input:  - xs  :: [(String,String)]	  
			 - rho :: String -> numpy.array
			 - op  :: numpy.array -> numpy.array -> numpy.array

	@Output: - X :: numpy.array 
				dim : n x m   where n is the number of examples
							  and m is number of features
'''
def to_X(xs, rho, op, normalize = False):
	X = np.array([ op(rho(s),rho(t)) for s,t in xs ])
	if normalize:
		return norm_by_mu_sigma(X)
	else:
		return X

def to_x(rho,op):
	def fn(s,t):
		return op(rho(s),rho(t)).reshape(1,-1)
	return fn


'''
	@Use: normalize x-vec by :   ___x_ - _E[x]___
	                                 var(x)
	      where x-vec is a column vector in X
	      and x is an element in this column vector                      
'''
def norm_by_mu_sigma(X):
	n,p  = X.shape
	mus  = np.array([ np.mean(X[:,k]) for k in xrange(p) ])
	sigs = np.array([ max(np.var (X[:,k]), 1e-6) for k in xrange(p) ])

	Mu    = np.matlib.repmat(mus, n,1)
	Sigma = np.matlib.repmat(sigs,n,1)
	Z     = (X - Mu)/Sigma

	return Z

############################################################
'''
	combine two rhos
'''
def vec_subtract(rho1, rho2):
	return rho1 - rho2

def vec_concat(rho1, rho2):
	return np.concatenate((rho1,rho2), axis = 0)

def vec_add(rho1, rho2):
	return rho1 + rho2

def vec_dot(phi1,phi2):
	v = np.dot(phi1,phi2)
	w = np.append(v,1.0)
	return w

def rho_divide(rho1, rho2):
	rho = [ v for v in rho1/rho2 ]
	out = []

	for v in rho:
		if math.isnan(v) or math.isinf(v):
			out.append(0.0)
		else:
			out.append(v)

	return np.array(out)

############################################################
'''
	@Use: given graph `G` and word `s`, and feature dict,
		  compute BTL-like score

	@Note: this only works with w2idx:
			 [ <ppdb weaker than>, <ngram weaker than> ]
'''
def rho_BTL(G, w2idx):

	def fn(s):

		vec_in, vec_out = get_edges(G, w2idx, s)

		ngram_idx = w2idx['<ngram weaker than>']['idx']
		ppdb_idx  = w2idx['<ppdb weaker than>'] ['idx']

		win_ngram  = vec_in [ngram_idx]
		lose_ngram = vec_out[ngram_idx]

		win_ppdb   = vec_in [ppdb_idx]
		lose_ppdb  = vec_out[ppdb_idx]

		tot_ppdb   = max(1e-5, win_ppdb  + lose_ppdb)
		tot_ngram  = max(1e-5, win_ngram + lose_ngram)

		btl_ngram = win_ngram / tot_ngram
		btl_ppdb  = win_ppdb  / tot_ppdb

		v = [0.0,0.0]
		v[ngram_idx] = btl_ngram
		v[ppdb_idx ] = btl_ppdb

		return np.array(v)

	return fn

'''
	@Use: given graph `G` and word `s`, and feature dict,
		  add in and out degree
'''
def rho_add_in_out(G, w2idx):

	def fn(s):

		vec_in, vec_out = get_edges(G, w2idx, s)
		v = np.array(vec_in )
		w = np.array(vec_out)
		return v + w

	return fn

def rho_subtract_in_out(G, w2idx):

	def fn(s):

		vec_in, vec_out = get_edges(G,w2idx,s)
		v = np.array(vec_in )
		w = np.array(vec_out)

		return v - w

	return fn	

def rho_concat_in_out(G, w2idx):

	def fn(s):

		vec_in, vec_out = get_edges(G,w2idx,s)
		v = np.array(vec_in )
		w = np.array(vec_out)

		return np.concatenate((v,w), axis = 0)

	return fn	

'''
	constuct in-neighbor adverb representation
'''
def rho_in(G, w2idx):

	def fn(s):

		vec_in, _ = get_edges(G,w2idx,s)

		return np.array(vec_in)

	return fn

'''
	constuct out-neighbor adverb representation
'''
def rho_out(G, w2idx):

	def fn(s):

		_, vec_out = get_edges(G,w2idx,s)

		return np.array(vec_out)

	return fn


'''	
	simple in degree out degree 
'''
def rho_head_tail(G, w2idx):

	def fn(s):

		v_in, v_out = get_edges(G, w2idx, s)

		head = sum(v_in )
		tail = sum(v_out)
		tot  = max(1e-5, head + tail)

		return np.array([head/tot, tail/tot])

	return fn

'''
	@Use: get in and out edge of s
'''
def get_edges(G, w2idx, s):

	'''
		in and out neighbor adverbs
	'''
	neigh_in  = [ d for _,d in G.in_neigh(s).iteritems()  ]
	neigh_out = [ d for _,d in G.out_neigh(s).iteritems() ]

	dict_out = { v : 0.0 for v in w2idx }
	dict_in  = { v : 0.0 for v in w2idx }

	for adv_i in neigh_in:
		for adv,n in adv_i.iteritems():
			if adv in dict_in:
				dict_in[adv] += n

	for adv_o in neigh_out:
		for adv,n in adv_o.iteritems():
			if adv in dict_out:
				dict_out[adv] += n

	'''
		construct vector so that idices are consistent
	'''
	vec_in  = [0]*len(dict_in )
	vec_out = [0]*len(dict_out)

	for v,n in dict_in.iteritems():
		stat = w2idx[v]
		vec_in[ stat['idx'] ] = n

	for v,n in dict_out.iteritems():
		stat = w2idx[v]
		vec_out[ stat['idx'] ] = n

	return vec_in, vec_out


