############################################################
# Module  : top level inference function
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os
import pickle
import numpy as np
from random import shuffle
from operator import itemgetter

from pulp import *
from collections import deque


from app     import *
from utils   import *
from scripts import *
from scripts.graph import *


'''
	Top level function to decide if s_1 < ... < s_n

	@Use: given words and pairwise judguments from logistic regression
		  output most likely permutation

	@Input: - gold   :: [[String]]
			- probs  :: Dict (String,String) _
				with key:
					(word1, word2)
				and value: a dictionary with key:
					- prob
					- yhat
	@Output: ranked :: [[String]] 
'''
def argmax_ILP(gold, Pr_s_le_t):

	raise NameError("Error in this formulation. Do not Use")

	algo, link_probs = ilp(gold, Pr_s_le_t)
	return algo, {'link-probs': link_probs}


############################################################

'''
	@Use: top level ilp function. Given gold cluster
	      and probabillity measure of pairs of words
	      output ranking and probability for every pair
'''
def ilp(gold, Prob):

	words   = join(gold)

	pairs   = [(s,t) for s in words for t in words if s!=t ]
	triples = [(u,v,w) for u in words for v in words for w in words
	                   if  u != v and v != w and u != w]

	probs   = to_prob(gold, Prob)

	'''
		construct solver
	'''
	lpProb =  LpProblem ('='.join(words), LpMaximize)

	'''
		variables where u-v imples u > v
	''' 
	variables = dict()

	for s,t in pairs:
		st = s +'<'+ t
		variables[st] = LpVariable('b_' + st, 0,1, LpInteger)


	'''
		objective function
	'''
	objective = []
	links     = all_links(words)

	for s,t in links:
		objective.append(probs[(s,t)] *  variables[s + '<' + t])
		objective.append(probs[(t,s)] * (1 - variables[t + '<' + s]))


	lpProb += lpSum(objective)  

	# constraints
	for s,t,r in triples:
		lpProb += (1 - variables[s + '<' + t]) \
		       +  (1 - variables[t + '<' + r]) \
		       >= (1 - variables[s + '<' + r])

	'''
		solve
	'''
	lpProb.solve()
	return read_solution(lpProb),probs

'''
	output ranking
'''
def read_solution(lpProb):

	solution = [ v.name.split('_')[1].split('<') \
	             for v in lpProb.variables() \
	             if v.varValue == 1.0 ]

	unsorted = dict()

	for s,t in solution:
		if s in unsorted: 
			unsorted[s].append(t)
		else:
			unsorted[s] = [t]


	algo = list(topological(unsorted))
	return [[w] for w in algo]


'''
	@Use: given gold set and prob measure
		  output prob s < t for every s,t
		  in ordered enumeration of s,t
'''
def to_prob(gold, Prob):
	words = join(gold)
	edges = [(s,t) for s in words for t in words if s != t]
	return { (s,t): Prob(s,t) for s,t in edges }


############################################################

'''
	@Use: given sample omega
		  construct all comparisons between
		  elements i and all i + k for k = 1 ... |omega|
''' 
def all_links(omega):

	def go(omega, pairs):
		if omega == []:
			return pairs
		else:
			head = omega[0]
			tail = omega[1:]

			pairs1 = [(head,t) for t in tail]

			return go(tail, pairs + pairs1)		

	if type(omega) == tuple:
		omega = [o for o in omega]

	return go(omega, [])


'''	
	@Use: topological sort
'''
def topological(graph):
	
	GRAY, BLACK = 0, 1

	order, enter, state = deque(), set(graph), {}

	def dfs(node):
	    state[node] = GRAY
	    for k in graph.get(node, ()):
	        sk = state.get(k, None)
	        if sk == GRAY: raise ValueError("cycle")
	        if sk == BLACK: continue
	        enter.discard(k)
	        dfs(k)
	    order.appendleft(node)
	    state[node] = BLACK

	while enter: dfs(enter.pop())
	return order














