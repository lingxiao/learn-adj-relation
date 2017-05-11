############################################################
# Module  : run test
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os
import struct
import pickle
import numpy as np
import networkx as nx
from numpy.linalg import inv

from app     import *
from utils   import *
from scripts import *
from scripts.graph import *
from experiments.pagerank import *


############################################################
'''
	@Use: given pre computed page rank vector
	      output Pr[s < t] 
'''
def Pr_s_le_t_pageRank(pr):

	eps = 1e-3

	def fn(s,t):
		prs = pr[s] if s in pr else 0.0
		prt = pr[t] if t in pr else 0.0

		if prs < prt: return 0.5 - eps
		else: return 0.5 + eps

	return fn

def decide_pageRank(pr):
	def fn(gold):
		return argmax_Omega(join(gold), Pr_s_le_t_pageRank(pr))
	return fn	

'''
	@Use: given graph and alpha
		  compute Pr[s < t] under personalized page rank
'''
def Pr_s_le_t_ppr(G,alpha):

	eps = 1e-3

	def fn(s,t):
		pi_s_t = G.ppr(src = s, tgt = t, alpha = alpha)
		pi_t_s = G.ppr(src = t, tgt = s,alpha = alpha)

		if pi_s_t > pi_t_s:
			return 0.5 + eps
		else:
			return 0.5 - eps

	return fn

def decide_ppr(G,alpha):

	def fn(gold):
		return argmax_Omega(join(gold), Pr_s_le_t_ppr(G,alpha))

	return fn	


'''
	@Use: absolute baseline coin toss for each decision
'''
def decide_uniform(G):

	def uniform_s_le_t(s,t):
		return 0.5

	def fn(gold):
		return argmax_Omega(join(gold), uniform_s_le_t)
	return fn


