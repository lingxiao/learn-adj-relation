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
	different graph parameters
'''
edge        = [ 'edge-wt', 'uniform' ]
topo        = [ 'ppdb-ngram', 'ppdb-ngram-bool', 'ppdb', 'ngram' ]
alphas      = [ 0.9, 0.8, 0.1 ]
graph_names = [t + '|' + e + '|' + str(a) for t in topo for e in edge for a in alphas]              

keys        = [e + '-' + t for e in edge for t in topo]
degree_dirs = data_dirs( 'out-degree' , keys )
ppr_dirs    = data_dirs( 'ppr' , [s + '-' + str(_a) for s in keys for _a in alphas ])

asset_dirs  = { k : v for k,v in list(degree_dirs.iteritems())
                               + list(ppr_dirs.iteritems())  }

work_dir = locate_dirs( get_path('baseline'), ['results','scripts','shells'] )

############################################################
'''
	Debug

	load test sets
'''
print('\n\t>> load base-comparative-superlative')
bcs = join(_xs for _, _xs in train_vertices(get_path('bcs')).iteritems())
bcs = [[[w] for w in _ws] for _ws in bcs]

print('\n\t>> load turk')
ccb = read_gold(get_path('ccb'))

print('\n\t>> load moh')
moh = read_gold(get_path('moh'))

'''
	create graph and paths
'''
try:
	G_ngram, G_ppdb, G_ppng
except:
	G_ngram = Graph('ngram|edge-wt|0.8', asset_dirs)
	G_ppdb  = Graph('ppdb|edge-wt|0.8', asset_dirs)
	G_ppng  = Graph('ppdb-ngram|edge-wt|0.8', asset_dirs)


############################################################
'''
	debug functions
'''
def data_for_all_links(cluster):
	raw   = cluster['raw']['link-probs']
	prob  = [p for _,_,p in raw if p != 0.5]
	return len(prob) == len(raw)


def no_data(cluster):
	raw  = cluster['raw']['link-probs']
	prob = [p for _,_,p in raw if p == 0.5]
	return len(prob) == len(raw)


def neg_tau(cluster):
	return cluster['tau'] < 0

############################################################


p_neigh = os.path.join(work_dir['results'], 'prob-neigh-ppdb-graph-moh.pkl')
p       = os.path.join(work_dir['results'], 'ppdb-graph-moh.pkl')

with open(p,'rb') as h:
	test = pickle.load(h)

with open(p_neigh,'rb') as h:
	test_neigh = pickle.load(h)
'''
	see how neigh estimte did on clusters where 
	taus arenegative
'''	
negs = { n:c for n,c in test['ranking'].iteritems() if neg_tau(c) }
negs_neigh = { n:c for n,c in test_neigh['ranking'].iteritems() if neg_tau(c) }

intersect = { n:c for n,c in negs.iteritems() if n in negs_neigh }

# look for cluster that's negative in test but > 0 in test_neigh
good = [ n for n,c in negs.iteritems() if test_neigh['ranking'][n]['tau'] > 0 ]
good = { n:test_neigh['ranking'][n] for n in good }

bad  = [ n for n,c in negs_neigh.iteritems() if test['ranking'][n]['tau'] > 0 ]









