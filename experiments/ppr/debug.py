############################################################
# Module  : debug ppr
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
	paths and directories

	precomputed assets needed to make graph
'''
keys        = [e + '-' + t for e in edge for t in topo]
degree_dirs = data_dirs( 'out-degree' , keys )
ppr_dirs    = data_dirs( 'ppr' , [s + '-' + str(_a) for s in keys for _a in alphas ])

asset_dirs  = { k : v for k,v in list(degree_dirs.iteritems())
                               + list(ppr_dirs.iteritems()) }
############################################################
'''
	debug this word
'''
src,tgt = 'good','great'

try:
	G_uni
	G_edge
	G_BTL
except:	
	print('\n>> constructing two graphs')
	G_uni  = Graph('ppdb-ngram|uniform|0.8', asset_dirs)
	G_edge = Graph('ppdb-ngram|edge-wt|0.8', asset_dirs)
	G_BTL = Graph('ppdb-ngram|BTL|'        , asset_dirs)
else:
	print('\n>> constructed two graphs')

try:
	E,V,El
except:	
	'''
		raw graph
	'''
	E,V  = load_as_dict(get_path('ppdb-ngram'))
	El,_ = load_as_list(get_path('ppdb-ngram-txt'))

'''
	assert G_uni.wt_edge(s,t) is correct
'''	
out_vertex_s = E[src] 	
out_vertex_t = E[tgt]

out_neigh_sl = [(a,b,c) for a,b,c in El if a == src]
out_neigh_tl = [(a,b,c) for a,b,c in El if a == tgt]

out_vertex_sl = set((a,b) for a,b,_ in out_neigh_sl)
out_vertex_tl = set((a,b) for a,b,_ in out_neigh_tl)

'''
	assert G_uni.wt_edge(s,t) !=  G_edge.wt_edge(s,t) 
'''	
G_uni.ppr(src,tgt) != G_edge.ppr(src,tgt)

print('\n>> sanity check on small example passed')

############################################################
'''
	run edge on all base comaprative superlative parirs
'''
print('\n\t>> load base-comparative-superlative')
bcs = join(_xs for _, _xs in train_vertices(get_path('bcs')).iteritems())
bcs = [[[w] for w in _ws] for _ws in bcs ]
ccb = read_gold(get_path('ccb'))

print('\n>> running ppr on base-comparative-superlative pairs')

if False:
	print('\n>> running ppr on base-comparative-superlative pairs')

	ranked_bcs = dict()
	rank_by    = rank_each(G_edge)
	bcs_pair   = [_xs for _xs in bcs if len(_xs) == 2]
	num        = 0

	for gold in bcs:
		algo = rank_by(gold)
		pair = pairwise_accuracy(gold, algo)
		ktau = tau(gold,algo)

		ranked_bcs[num] = {  'gold' : gold
			                , 'algo': algo
			                , 'pair': pair
			                , 'tau' : ktau
				            ,'|tau|': abs(ktau)}

		num += 1


	avg_pair = sum(d['pair']     for _,d in ranked_bcs.iteritems())/len(ranked_bcs)
	avg_tau  = sum(d['tau']      for _,d in ranked_bcs.iteritems())/len(ranked_bcs)
	abs_tau  = sum(d['|tau|']    for _,d in ranked_bcs.iteritems())/len(ranked_bcs)

	print('\n>> pairwise: ' + str(avg_pair))		
	print('\n>> tau: '      + str(avg_tau) )		
	print('\n>> |tau|: '    + str(abs_tau) )		

############################################################
'''
	debug this one in particular
'''
# gold  = [['clear'], ['accurate'], ['precise'], ['exact']]
gold = [[w] for w in ['large','larger', 'largest']]

algo_argmax = argmax_order(G_edge)(gold)
algo_ilp    = ilp_order   (G_edge)(gold)


############################################################
'''
	one more thing to try:
		try shifting it by the mean
'''



























