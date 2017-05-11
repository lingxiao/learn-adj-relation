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


from app     import *
from utils   import *
from scripts import *
from scripts.graph import *


'''
	Top level function to decide if s_1 < ... < s_n

	@Use: given words and pairwise judguments from logistic regression
		  output most likely permutation

	@Input: - words  :: [String]
			- probs  :: Dict (String,String) _
				with key:
					(word1, word2)
				and value: a dictionary with key:
					- prob
					- yhat
	@Output: ranked :: [[String]] 
'''
def argmax_Omega(words, Pr_s_le_t):

	Omega      = Pi(words)
	probs      = [ (o, prob_om(o,Pr_s_le_t)) for o in Omega ]
	probs      = [ (o, p, raw) for o,(p,raw) in probs ]

	om_star, prob_star, link_probs = max(probs, key = itemgetter(1) )

	algo = [ [w] for w in om_star ]

	return algo, {'prob*': prob_star, 'link-probs': link_probs}

############################################################

'''
	@Use: given a tuple of n words (s_1,...,s_n)
		  interpreted as s_1 < ... < s_n
		  output probability of this sequence

 	@Input: - omega :: (String,..)
 			- Pr_s_le_t :: String -> String -> Float

 	@Output :: Pr[s_1 < ... < s_n] :: Float
'''
def prob_om(omega, Pr_s_le_t):

	links  = all_links(omega)
	probs  = [(s,t,Pr_s_le_t(s,t)) for s,t in links]
	probs_ = [ p for _,_,p in probs ]
	return np.prod(np.array(probs_)), probs


'''
	@Use: given list of words, output all permutations
		  reverse order so there's strong bias against
'''
def Pi(words):
	Om = list(itertools.permutations(words))
	Om.sort()
	Om.reverse()     # NOTE the set is reversed

	return Om


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















