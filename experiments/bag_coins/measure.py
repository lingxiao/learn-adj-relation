############################################################
# Module  : estimate missing edge using bag of coins model

# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os
import pickle
import numpy as np
import networkx as nx

from app     import *
from utils   import *
from scripts import *
from scripts.graph import *
from experiments.argmax import *
from experiments.rank_all import *
from experiments.bag_coins import *


############################################################
'''
	Measures 
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


def Pr_s_le_t_coin(G):

	eps = 1e-3

	def fn(src,tgt):

		src_coins = neigh_coin(src,G)
		tgt_coins = neigh_coin(tgt,G)

		src_p  = np.mean(np.array(src_coins))
		tgt_p  = np.mean(np.array(tgt_coins))

		if src_p < tgt_p:
			return 0.5 + eps
		else:
			return 0.5 - eps

	return fn

'''
	@Use: combine measures
'''
def Pr_s_le_t_combo(G):

	real = Pr_s_le_t(G)
	coin = Pr_s_le_t_coin(G)

	def fn(s,t):
		prob = real(s,t)

		if prob == 0.5:
			return coin(s,t)
		else:
			return prob

	return fn

'''
	@Use: given vertex src and graph G
		  compute bag of coins for src
'''
def neigh_coin(src,G):

	neigh_s = [ v for v,_ in G.neigh(src).iteritems() ]

	coins = []

	for t in neigh_s:
		head,_ = G.edge(t,src)
		tail,_ = G.edge(src,t)

		n_head = float(sum(n for _,n in head.iteritems()))
		n_tail = sum(n for _,n in tail.iteritems())

		'''
			smooth adhoc
		'''
		n_head = n_head if n_head != 0 else n_tail/10.0
		n_tail = n_tail if n_tail != 0 else n_head/10.0

		coins.append(n_head/(n_head + n_tail))

	return coins

############################################################
'''
	Decision Functions

	@Use: pick out algo from gold
'''
def decide_fn_coin(G):
	def fn(gold):
		return argmax_Omega(join(gold), Pr_s_le_t_coin(G))
	return fn

def decide_fn_both(G):
	def fn(gold):
		return argmax_Omega(join(gold), Pr_s_le_t_combo(G))
	return fn


























