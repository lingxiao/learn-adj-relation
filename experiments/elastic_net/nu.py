############################################################
# Module  : feature representation nu based on neighbors
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import math
import numpy as np
from scripts import *
from scripts.graph import *


############################################################
'''
	@Use: pick the top n most connected vertices in G
		  and compute their btl score
'''
def nu_coin(G, top_n):

	def fn(src):

		squash = lambda d : sum(n for _,n in d.iteritems())

		neigh = sorted( [(t,squash(d)) for t,d in G.neigh(src).iteritems()], key = lambda x : x[1] )
		neigh.reverse()
		neigh_sm = neigh[0:top_n]

		coins = []

		for tgt,_ in neigh_sm:

			head,_ = G.edge(tgt,src)
			tail,_ = G.edge(src,tgt)

			n_head = float(sum(n for _,n in head.iteritems()))
			n_tail = float(sum(n for _,n in tail.iteritems()))

			'''
				smooth adhoc
			'''
			n_head = n_head if n_head != 0 else n_tail/10.0
			n_tail = n_tail if n_tail != 0 else n_head/10.0

			coins.append(n_head/(n_head + n_tail))

		# return coins
		coins = np.array(coins + [0.0] * max(0,top_n - len(coins)))
		return coins

	return fn		

'''
	@Use: concat top n in and out neighbor
'''
def nu_in_out_concat(G,n):

	def fn(s):
		n_in, n_out = get_neighbor(G, n,s)
		return np.array(n_in + n_out)

	return fn

'''
	@Use: concat top n in and out neighbor
		  where out neighbor default to negative value
'''
def nu_in_neg_out_concat(G,num_neighbor):

	def fn(s):
		n_in, n_out = get_neighbor(G,num_neighbor,s)
		n_out = [-1*n for n in n_out]
		return np.array(n_in + n_out)

	return fn

def nu_in(G,n):

	def fn(s):
		n_in, _ = get_neighbor(G, n,s)
		return np.array(n_in)

	return fn

def nu_out(G,n):

	def fn(s):
		_, n_out = get_neighbor(G, n,s)
		return np.array(n_out)

	return fn

############################################################
'''
	@Use: get in and out neighbor of vertex s 
		  padded to given length
		  sorted from to pto bottom
'''
def get_neighbor(G, top_n, s):

	squash = lambda d : sum(n for _,n in d.iteritems())

	neigh_in_raw  = sorted( squash(d) for _,d in G.in_neigh(s).iteritems() )
	neigh_out_raw = sorted( squash(d) for _,d in G.out_neigh(s).iteritems())

	neigh_in_raw.reverse()
	neigh_out_raw.reverse()

	neigh_in  = neigh_in_raw [0:top_n] + [0.0]* max(0, top_n - len(neigh_in_raw))
	neigh_out = neigh_out_raw[0:top_n] + [0.0]* max(0, top_n - len(neigh_out_raw))

	return neigh_in, neigh_out










