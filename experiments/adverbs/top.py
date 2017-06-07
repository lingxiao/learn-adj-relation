############################################################
# Module  : pointwise estimation baseline
# Date    : May 30th, 2017
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
from experiments.elastic_net import *


############################################################
'''
	current directory path
'''
adv_dir = locate_dirs( get_path('adverbs')
	                 , ['results', 'script', 'shells'])


############################################################
'''
	hypothesis one: there is a relationship between
	number of adjectives an adverb intensifies, 
	and its strength
'''

'''
	@Use: Given graph G and an adverb,
		  get all edges in G where adverb appears as 
		  list of triples of form:
		  	(s,t,adverb) 
		  where the interpretation is:

		  	adverb s = t
'''
def get_edges(G, adverb):

	adv_edges = []

	for s, edge in G.edges.iteritems():
		for t, es in edge.iteritems():
			if adverb in es:
				adv_edges.append((s,t,adverb))

	return adv_edges
	

G        = G_ppng
gold_set = test['ccb'] + test['moh'] + test['bcs']

def Pr_v_strong_baseline(G, gold_set):

	def fn(adverb):

		edges = get_edges(G, adverb)
		gold  = join( to_le_than(g) for g in gold_set )

		s_le_t = [ (s,t,w) for s,t,w in edges if (s,t) in gold ]
		s_ge_t = [ (s,t,w) for s,t,w in edges if (t,s) in gold ]
		tot    = float(len(s_le_t) + len(s_ge_t))

		if s_ge_t and s_le_t: coin = len(s_le_t) / tot
		else: coin = 0.5

		return coin

	return fn

# Pr_v_strong = Pr_v_strong_baseline(G_ppng, gold_set)

# probs = [ (v, Pr_v_strong(v)) for v in G.labels ]
# probs = sorted(probs, key = lambda tup: tup[1] )
# probs.reverse()








############################################################
'''
	Utils

	@Use: given test set of form: [test1, test2, ...]
		  where test_i = [[w1],[w2],[w3,w4],...]
		  so that w < w2 < (w3 = w4) < ...
		  turn into a list of pairs so that the first
		  word in the pair is weaker than second, ie:
		  [(w1,w2),(w1,w3),(w2,w3),(w2,w4),...]

	@Input : golds :: [[String]]	

	@output: pairs :: [(String,String)]
'''
def to_le_than(golds):
	return go_le_than(golds,[])

def go_le_than(golds, pairs):
	if golds == []:
		return pairs
	else:
		head = golds[0]
		tail = golds[1:]

		pairs1 = join([(s,t) for s in head for t in elem] \
			     for elem in tail)

		return go_le_than(tail, pairs + pairs1)		













