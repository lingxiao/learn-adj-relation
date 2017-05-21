############################################################
# Module  : combine models using ilp argmax
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os
import math
import numpy as np
import networkx as nx
from sklearn.metrics import r2_score
from sklearn.linear_model import ElasticNet
import pickle

from pulp import *
from collections import deque


from app     import *
from utils   import *
from scripts import *
from scripts.graph import *
from experiments.argmax import *
from experiments.rank_all import *
from experiments.elastic_net import *


############################################################
'''
	model and feature space representation
'''
winner = 'logistic-regression|ppdb-ngram-1|[nu^HT(s)-nu^HT(t)]|num_neigh=10|penalty=l1|C=0.4'
path   = os.path.join(work_dir['results'],winner + '/model')
	
print('\n\t>> loading model from ' + winner)
with open(path,'rb') as h:
	model = pickle.load(h)

data_set   = 'ppdb-ngram-1'
num_neigh  = 10

fix, nu = 'HT' , nu_coin( GRAPH[data_set], num_neigh )
OP , op = '-'  , vec_subtract
phi     = to_x(nu,op)

SAVE = False

############################################################
'''
	run on all data set
'''
results_dir = os.path.join( work_dir['results']
	                      , 'combined-ilp/' 
	                      + winner           
	                      + '|infer_set=' + data_set      
	                      + '|50-50-prior')


if not os.path.exists(results_dir):
	os.mkdir(results_dir)

readme = 'model:\t' + winner              + '\n' \
	   + 'inference data set:\t' + data_set + '\n' \
	   + 'inference tosses:\t50-50-prior'   + '\n' \
	   + 'argmax function:\tilp'

with open( os.path.join(results_dir,'readme.txt'), 'wb' ) as h:
	h.write(readme)

if False:
	exec_rank( data_set
		     , test
		     , decide_fn_both_binomial_ilp(G_ppng, model, phi)
		     , results_dir
		     , save = SAVE
		     ) 

####################################################

gold = [['many'],['more']]
# gold = [[w] for w in ['cool', 'cooler']]

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
obj   = []
links = all_links(words)

# for s,t in links:
for s,t in pairs:
	obj.append(probs[(s,t)] *  variables[s + '<' + t])
	# obj.append(probs[(t,s)] * (1 - variables[t + '<' + s]))

lpProb += lpSum(obj)  

# constraints
for s,t,r in triples:
	lpProb += (1 - variables[s + '<' + t]) \
	       +  (1 - variables[t + '<' + r]) \
	       >= (1 - variables[s + '<' + r])

lpProb.solve()

solution = [ v.name.split('_')[1].split('<') \
             for v in lpProb.variables() \
             if v.varValue == 1.0 ]

# unsorted = dict()






