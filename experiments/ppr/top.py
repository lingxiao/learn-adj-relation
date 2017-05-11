############################################################
# Module  : Run this script to generate all test and shell 
# 			files
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import shutil
import pickle
import operator
import itertools
from pulp import *
from collections import Counter

from app     import *
from utils   import *
from scripts import *
from scripts.graph import *
from experiments import *

############################################################
'''
	@Use: given particular graph and gold, output 
		  total order using pairwise order
'''
def argmax_order(graph):

	def fn(gold):

		words  = join(gold)
		Omega  = list(itertools.permutations(words))

		dist = { _om : None for _om in Omega }

		for omega in dist:
			dist[omega] = prob_walk(omega, graph)

		argmax = max(dist.iteritems(), key=operator.itemgetter(1))[0]

		return [[w] for w in argmax]

	return fn

'''
	@Use: given a graph and gold set, output 
	      total ordering by maximizing pairwise preference
	      s.t. transitivity is maintained
'''
def ilp_order(graph):

	def fn(gold):
		words   = join(gold)
		pairs   = [ (s,t) for s in words for t in words if s != t ]
		triples = [ (s,t,r) for s in words for t in words for r in words
			      if s != t and t != r and s != r ]

		'''
			Lp problem
		'''		
		lpProb =  LpProblem ('='.join(words), LpMaximize)

		'''
			make variable and coefficents
		'''	
		coefs     = dict()
		variables = dict()

		for s,t in pairs:

			top = graph.ppr(t,s)
			bot = graph.ppr(s,t)

			'''
				if pi_t[s] = 0, then s << t (or they're not related)
				if pi_s[t] = 0, then s >> t (or they're not related)
			'''
			if not top: top = 1e-3
			if not bot: bot = 1e-3

			coefs[s + '>' + t] = top / bot
			variables[s + '=' + t] = LpVariable('b_' + s + '=' + t, 0,1, LpInteger)

		'''
			objective function
		'''
		objective = []

		for s,t in pairs:
			k_st = s + '>' + t
			k_ts = t + '>' + s
			objective.append(coefs[k_st] *  variables[s + '=' + t])
			objective.append(coefs[k_ts] * (1 - variables[s + '=' + t]))

		lpProb += lpSum(objective)  

		# constraints
		for s,t,r in triples:
			lpProb += (1 - variables[s + '=' + t]) \
			       +  (1 - variables[t + '=' + r]) \
			       >= (1 - variables[s + '=' + r])


		'''
			solve and extract ranking
		'''
		lpProb.solve()

		raw = [v.name.split('=') for v in lpProb.variables() \
		      if v.varValue == 1.0]
		raw = [(u.replace('b_',''),v) for [u,v] in raw]
		raw = [(u.replace('_','-'), v.replace('_','-')) for u,v in raw]

		# construct graph :: dictionary for topological sort
		order = dict()        

		for s,w in raw:
			if s in order:
			  order[s] += [w]
			else:
			  order[s] = [w]

		# complete the sink in the dictonary
		for w in words:
			if w not in order: order[w] = []

		algo = [[w] for w in toposort(order)]

		return algo

	return fn

############################################################
'''
	ranking subroutines
'''

'''
	@Use: given an event of form: w = (s1,...,s_n)
		  determine the likelihood of this event
		  by:
		  	Pr[w] = Pr[s1]Pr[s1 -> s2]Pr[s2 -> s3] .. Pr[s_{n-1} -> s_n]
		  where Pr[s1] = 1 by definition
		  and Pr[s1 -> s2] is the probability that a personalized random
		  walk starting at s1 termintates at s2
	@Input:  - omega :: [String]
			 - G     :: Graph where we use:
			 			G.ppr :: String -> String -> Dict (String,String) Float
			 				mapping (s1,s2) to Pr[s1 -> s2]
'''
def prob_walk(omega, G):

	trans_probs = []

	for idx, src in enumerate(omega):
		if idx < len(omega) - 1:
			tgt = omega[idx + 1]
			trans_probs.append(G.ppr(src = src, tgt = tgt))
		else:
			trans_probs.append(1.0)

	return reduce(lambda x, y: (x if x else 1) * (y if y else 1), trans_probs)

'''
  @Use: given milp object, output ranking
        as list of lists

  prob_to_algo_rank :: MILP -> [[String]] -> [[String]]
'''  
def prob_to_algo_rank(prob,words):

  raw = [v.name.split('=') for v in prob.variables() \
        if v.varValue == 1.0]
  raw = [(u.replace('s_',''),v) for [u,v] in raw]
  raw = [(u.replace('_','-'), v.replace('_','-')) for u,v in raw]

  # construct graph :: dictionary for topological sort
  order = dict()        

  for s,w in raw:
    if s in order:
      order[s] += [w]
    else:
      order[s] = [w]

  # complete the sink in the dictonary
  for w in words:
    if w not in order: order[w] = []

  return [[w] for w in toposort(order)]

############################################################
'''
	different graph parameters
'''
edge        = [ 'uniform', 'edge-wt', 'BTL' ]
topo        = [ 'ppdb-ngram', 'ppdb-ngram-bool' ]
alphas      = [ 0.9,0.8,0.1 ]
graph_names = [t + '|' + e + '|' + str(a) for t in topo for e in edge for a in alphas]              

'''	
	make results directory
'''
result_root = os.path.join(get_path('ppr'), 'results')
result_dir  = locate_dirs( result_root, graph_names, rewrite = False )

