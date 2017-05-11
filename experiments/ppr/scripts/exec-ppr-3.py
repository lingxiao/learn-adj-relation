############################################################
# Module  : template script for deploying on remote
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import itertools
from pulp import *

from app     import *
from utils   import *
from scripts import *
from scripts.graph import *
from experiments import *
from experiments.ppr.top import *

############################################################
'''
	data to test on
'''
print('\n\t>> load base-comparative-superlative')
bcs = join(_xs for _, _xs in train_vertices(get_path('bcs')).iteritems())
bcs = [[[w] for w in _ws] for _ws in bcs]

print('\n\t>> load turk')
ccb = read_gold(get_path('ccb'))

print('\n\t>> load moh')
moh = read_gold(get_path('moh'))

############################################################
'''
	paths and directories

	precomputed assets needed to make graph
'''
keys        = [e + '-' + t for e in edge for t in topo]
degree_dirs = data_dirs( 'out-degree' , keys )
ppr_dirs    = data_dirs( 'ppr' , [s + '-' + str(_a) for s in keys for _a in alphas ])

asset_dirs  = { k : v for k,v in list(degree_dirs.iteritems())
                               + list(ppr_dirs.iteritems()) }
'''
	make results directory
'''
result_root = os.path.join(get_path('ppr'), 'results')
result_dir  = locate_dirs( result_root, graph_names, rewrite = False )


############################################################
'''
	run 
'''
batch = 3
graph_name = graph_names[batch]
out_dir    = result_dir[graph_name]

tests      = {'bcs': bcs, 'ccb': ccb, 'moh': moh}

print('\n\t>> making graph ' + graph_name)
G = Graph(graph_name, asset_dirs)

for test_name, test_set in tests.iteritems():

	print('\n\t>> rank with ilp inference on ' + test_name)
	rank_all_gold( test_set
		         , ilp_order(G)
		         , os.path.join(out_dir, test_name + '-ilp.txt')
		         , refresh = False )

	print('\n\t>> rank with argmax inference on ' + test_name )
	rank_all_gold( test_set
		         , argmax_order(G)
		         , os.path.join(out_dir, test_name + '-argmax.txt')
		         , refresh = False )

