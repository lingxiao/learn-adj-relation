############################################################
# Module  : A series of measures on the graph for experiments
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import json
import pickle
import networkx as nx
from collections import Counter

from utils   import *
from scripts import *
from scripts.graph import *


############################################################
'''	DEPRICATED

	@Use  : open graph and compute the weight of 
	        edges between vertices, so that between
	        each vertex there is at most one directed
	        edge. the weight of the edge between s and t
	        is computed by function weighted_edge

	@Given: path to graph                :: String
			path to edges to be computed :: String
	        path to output directory     :: String

	@Note:  if one of the edges has zero weight while
	        other doese not, then smooth by 1e-5

	@output: None

'''
def weight_by_direct(gr_path, edge_path, out_path):

	print('\n>> computing edge weight by bradley terry')
	print('\n>> edge path: ' + edge_path)
	
	G, words = load_as_list(gr_path)

	with open(edge_path, 'rb') as h:

		edges = [xs.split(', ') for xs in h.read().split('\n') \
		        if len(xs.split(', ')) == 2]

	f = open(out_path, 'wb')

	for s,t in edges:

		eps = 1e-5	

		s_t = len([(x,y) for x,y,_ in G if x == s and y == t])
		t_s = len([(x,y) for x,y,_ in G if x == t and y == s])

		if s_t or t_s:

			'''
				smooth weights so we don't have 
				edges with 0 weight
			'''
			if s_t == 0: 
				s_t += eps
				t_s -= eps

			if t_s == 0:
				s_t -= eps
				t_s += eps

			tot = float(s_t + t_s)
			st  = s_t/tot
			ts  = t_s/tot

			st = s + '->' + t
			ts = t + '->' + s
			f.write(st + ': ' + str(s_t/tot) + '\n')
			f.write(ts + ': ' + str(t_s/tot) + '\n')

	f.close()


'''DEPRICATED
	@Use  : Given raw ppdb graph as list of edges of form:
				(source, target, <edge>)
			and vertices, output edges weighted by counting the 
	        number of vertices going between the vertices

	                   number_of_vertex(s -> t) 
	         ---------------------------------------------------
	         	sum_{x \in neighbor(s)} number_of_vertex(s -> x)

	@NOTE: alpha smoothing parameter ensure that: |neigh(x)| >= alpha

	@Given: path to graph                :: String
			path to edges to be computed :: String
	        path to output directory     :: String

	@output: None
'''
def weight_by_neigh(gr_path, edge_path, out_path):

	print('\n>> computing edge weight by neigh(s)')
	print('\n>> edge path: ' + edge_path)

	E, _ = load_as_list(gr_path)

	eps = 1e-5

	with open(edge_path, 'rb') as h:
		edges = [xs.split(', ') for xs in h.read().split('\n') \
		        if len(xs.split(', ')) == 2]

	f = open(out_path, 'wb')

	for s,t in edges:

		# weight(s -> t)
		neigh_s = [(x,y,z) for x,y,z in E if x == s]
		e_s_t   = [(x,y,z) for x,y,z in neigh_s if y == t]
		w_s_t   = len(e_s_t) / float(len(neigh_s) + 1e-5)

		# weight(t -> s)
		neigh_t = [(x,y,z) for x,y,z in E if x == t]
		e_t_s   = [(x,y,z) for x,y,z in neigh_t if y == s]
		w_t_s   = len(e_t_s) / float(len(neigh_t) + 1e-5)

		if w_s_t or w_t_s:

			'''
				smooth out the zero edge
			'''
			if w_s_t == 0:
				w_s_t += eps

			if w_t_s == 0:
				w_t_s += eps


			st = s + '->' + t
			ts = t + '->' + s
			f.write(st + ': ' + str(w_s_t) + '\n')
			f.write(ts + ': ' + str(w_t_s) + '\n')

	f.close()

'''	DEPRICATED
	@Use: compute for every word s in word_path:
			E[X_st] = \sum_{r \in neigh(s)} X_sr
		  and save output to out_path
'''
def edge_martin(gr_path, word_path, out_path):

	G = Graph(gr_path)

	words = [w for w in open(word_path,'rb').read().split('\n') if w]

	with open(out_path,'wb') as h:
		for word in words:
			h.write(word + ': ' + str(G.Ex(word)) + '\n')


'''@Depricated: using sparse representation instead
	@Use: edge multinomial
	@Input: - gr_path   :: String
			- word_path :: String
			- out_path  :: String
			- eps       :: Float
'''
def edge_multinomial(gr_path, word_path, out_path, eps = 0.0):

	if os.path.exists(out_path):
		os.remove(out_path)

	words = [w for w in open(word_path,'rb').read().split('\n') if w]
	E,V   = load_as_list(gr_path)

	'''
		construct sample space omega: {-K, ..., K} 
	'''
	max_K = [(s,t) for s,t,_ in E]
	max_K = [[k,]*v for k,v in Counter(max_K).items()]
	max_K = max(len(K) for K in max_K)

	neg_omega = sorted(-k for k in xrange(1,max_K + 1))
	omega     = neg_omega + range(0,max_K + 1)

	probs = { s : None for s in words }

	for word in probs:

		'''
			construct distributiion over {-K,...,K}
		'''
		dist = {o:eps for o in omega}

		in_neigh  = [(x,y) for x,y,z in E if y == word]
		out_neigh = [(x,y) for x,y,z in E if x == word]

		in_neigh  = [[k,]*v for k,v in Counter(in_neigh).items()]
		out_neigh = [[k,]*v for k,v in Counter(out_neigh).items()]

		n_in_neigh   = [len(n) for n in in_neigh]
		n_out_neigh  = [len(n) for n in out_neigh]

		for om in dist:
			if om < 0: 
				dist[om] = len([x for x in n_out_neigh if -x == om])
			else:
				dist[om] = len([x for x in n_in_neigh if x == om])

		probs[word] = dist

	'''
		save
	'''
	with open(out_path, 'wb') as h:
	    pickle.dump(probs, h, protocol=pickle.HIGHEST_PROTOCOL)
