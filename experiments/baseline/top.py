############################################################
# Module  : pointwise estimation baseline assets
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

work_dir = locate_dirs( get_path('baseline')
	                  , [ 'results'
	                    , 'script'
	                    , 'shells'
	                    , 'no-data'
	                    ] 
	                 )

############################################################
'''
	Debug

	load test sets
'''
print('\n\t>> load base-comparative-superlative')
bcs = join(_xs for _, _xs in train_vertices(get_path('bcs')).iteritems())
bcs = [[[w] for w in _ws] for _ws in bcs]

print('\n\t>> load turk')
ccb = read_gold( get_path('ccb') )

print('\n\t>> load moh')
moh = read_gold( get_path('moh') )


'''
	create graph and paths
'''
try:
	G_ngram, G_ppdb, G_ppng
except:
	G_ngram = Graph('ngram|edge-wt|0.8'     , asset_dirs)
	G_ppdb  = Graph('ppdb|edge-wt|0.8'      , asset_dirs)
	G_ppng  = Graph('ppdb-ngram|edge-wt|0.8', asset_dirs)

