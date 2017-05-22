############################################################
# Module  : pointwise estimation baeline
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
from experiments.baseline import *

############################################################
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
	@Use: neighborhood baseline Pr[ s < t ] using union of neighbors
'''
def Pr_s_le_t_union_neigh(G):

	def fn(s,t):

		s_in_neigh_no_t  = { k:v for k,v in G.in_neigh(s).iteritems()  if k != t }
		s_out_neigh_no_t = { k:v for k,v in G.out_neigh(s).iteritems() if k != t }

		t_in_neigh_no_s  = { k:v for k,v in G.in_neigh(t).iteritems()  if k != s }
		t_out_neigh_no_s = { k:v for k,v in G.out_neigh(t).iteritems() if k != s }

		tot = lambda d : sum(join([n for _,n in x.iteritems()] for _,x in d.iteritems()))

		s_le_z = max(tot(s_out_neigh_no_t), 1e-5)
		s_ge_z = max(tot(s_in_neigh_no_t ), 1e-5)
		t_le_z = max(tot(t_out_neigh_no_s), 1e-5)
		t_ge_z = max(tot(t_in_neigh_no_s ), 1e-5)
		total  = float(s_le_z + s_ge_z + t_le_z + t_ge_z)

		s_le_t = (s_le_z + t_ge_z)/total
		s_ge_t = (s_ge_z + t_le_z)/total

		return s_le_t

	return fn

'''
	@Use: neighborhood baseline Pr[ s < t ] using 
			Pr[s < _] * Pr[_  < t ]
'''
def Pr_s_le_t_mult_neigh(G):

	def fn(s,t):

		s_in_neigh_no_t  = { k:v for k,v in G.in_neigh(s).iteritems()  if k != t }
		s_out_neigh_no_t = { k:v for k,v in G.out_neigh(s).iteritems() if k != t }

		t_in_neigh_no_s  = { k:v for k,v in G.in_neigh(t).iteritems()  if k != s }
		t_out_neigh_no_s = { k:v for k,v in G.out_neigh(t).iteritems() if k != s }

		tot = lambda d : sum(join([n for _,n in x.iteritems()] for _,x in d.iteritems()))

		s_le_z = float(max(tot(s_out_neigh_no_t), 1e-5))
		s_ge_z = float(max(tot(s_in_neigh_no_t ), 1e-5))
		t_le_z = float(max(tot(t_out_neigh_no_s), 1e-5))
		t_ge_z = float(max(tot(t_in_neigh_no_s ), 1e-5))
		total  = float(s_le_z + s_ge_z + t_le_z + t_ge_z)

		# Pr[ s < ] and Pr[s >]
		s_le = s_le_z/(s_le_z + s_ge_z)
		s_ge = 1 - s_le

		t_le = t_le_z/(t_le_z + t_ge_z)
		t_ge = 1 - t_le

		s_le_t_raw = s_le * t_ge
		s_ge_t_raw = s_ge * t_le

		s_le_t = s_le_t_raw / (s_le_t_raw + s_ge_t_raw)
		s_ge_t = s_ge_t_raw / (s_le_t_raw + s_ge_t_raw)

		print(s_le_t, s_ge_t)

		return s_le_t

	return fn

'''
	@Use: given vertices s and t, compute 
				Pr[ s <_{P_s} t ]
'''
def Pr_s_le_t_shortest_path(G):

	def fn(s,t):

		p_s_le_t = short_s_le_t(G, s,t)
		q_s_le_t = 1 - short_s_le_t(G,t,s)

		pq = p_s_le_t * q_s_le_t

		return pq / (pq + (1-p_s_le_t)*(1-q_s_le_t))

	return fn

def short_s_le_t(G,s,t):

	try:
		path_s_t = nx.shortest_path(G.graph, source = s, target = t) 
	except:
		path_s_t = []

	# if path_s_t:
	if len(path_s_t) > 2:

		path_probs = path_prob_table(G,path_s_t)
		s_to_t     = enumerate_path(path_s_t)
		t_to_s     = reverse_path(s_to_t)

		s_le_t  = np.prod(np.array([ path_probs[(x,y)] for x,y in s_to_t ]))
		s_ge_t  = np.prod(np.array([ path_probs[(x,y)] for x,y in t_to_s ]))

		return s_le_t / (s_le_t + s_ge_t)
	else:
		return 0.5


'''
	@Use: given path, compute probability of 
		  every s,t along the path.
'''
def path_prob_table(G,path):

	path  = enumerate_path(path) 
	path  = path + reverse_path(path)

	probs = dict()

	for s,t in path:
		p_s_le_t = Pr_s_le_t(G)(s,t)
		probs[(s,t)] = p_s_le_t

	return probs

'''
	@Use: enumerate all pairs along path
'''
def enumerate_path(path):

	out = []

	for i,s in enumerate(path):
		if i == len(path) - 1:
			pass
		else:
			t = path[i+1]
			out+= [(s,t)]
	return out


def reverse_path(path):
	q = [(t,s) for s,t in path]
	q.reverse()
	return q

############################################################
'''
	Decision Functions

	@Use: pick out algo from gold
'''
def decide_fn(G):
	def fn(gold):
		return argmax_Omega(gold, Pr_s_le_t(G))
	return fn

def decide_fn_neigh(G):
	def fn(gold):
		return argmax_Omega(gold, Pr_s_le_t_union_neigh(G))
	return fn	

'''
	@Use: absolute baseline coin toss for each decision
'''
def decide_fn_uniform():

	def uniform_s_le_t(s,t):
		return 0.5

	def fn(gold):
		return argmax_Omega(gold, uniform_s_le_t)
	return fn

'''
	@Use: decide using shortest path heuristic
'''
def decide_fn_shortest_path(G):
	def fn(gold):
		return argmax_Omega(gold, Pr_s_le_t_shortest_path(G))
	return fn

