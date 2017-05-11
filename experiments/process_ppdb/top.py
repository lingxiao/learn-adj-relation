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
from experiments.process_ppdb import *

############################################################
'''
	different graph parameters
'''
edge        = [ 'edge-wt' ]
topo        = [ 'ppdb-ngram', 'ppdb', 'ngram' ]
alphas      = [ 0.8 ]
graph_names = [t + '|' + e + '|' + str(a) for t in topo for e in edge for a in alphas]              

keys        = [e + '-' + t for e in edge for t in topo]
degree_dirs = data_dirs( 'out-degree' , keys )
ppr_dirs    = data_dirs( 'ppr' , [s + '-' + str(_a) for s in keys for _a in alphas ])

asset_dirs  = { k : v for k,v in list(degree_dirs.iteritems())
                               + list(ppr_dirs.iteritems())  }

work_dir = locate_dirs( get_path('elastic-net'), ['results'
	                                             ,'script'
	                                             ,'shells'
	                                             ,'assets'
	                                             ,'combined'])

baseline = locate_dirs( get_path('baseline'), ['no-data'] )

############################################################
'''
	graphs
'''
try:
	G_ppdb, G_ngram, G_ppng
except:	
	G_ppdb  = Graph( 'ppdb|edge-wt|0.8'       , asset_dirs )
	G_ngram = Graph( 'ngram|edge-wt|0.8'      , asset_dirs )
	G_ppng  = Graph( 'ppdb-ngram|edge-wt|0.8' , asset_dirs )

############################################################
'''
	@Use: get all edges
'''
def get_edges(G):

	all_edges = []

	for src,out in G.edges.iteritems():
		for tgt,adverbs in out.iteritems():
			for adverb,n in adverbs.iteritems():
				es = [(src,tgt,adverb)]*n
				all_edges += es

	return all_edges

'''
	@Use: convert to dictionary
'''
def to_edges(vertices,edges):

	print('\n\t>> making graph ...')
	graph = { v : None for v in vertices }	

	for src,_ in graph.iteritems():

		out = [(tgt,v) for x,tgt,v in edges if x == src]

		d = dict()

		for tgt,v in out:
			if tgt not in d: 
				d[tgt] = {v : 1}
			else:
				if v in d[tgt]:
					d[tgt][v] += 1
				else:
					d[tgt][v] = 1

		graph[src] = d 

	return graph

def make_graphs():

	print('\n\t>> remove loops from ngram')
	ngram_edges    = get_edges(G_ngram)
	ngram_no_loops = [(s,t,v) for s,t,v in ngram_edges if s != t]

	print('\n\t>> remove loops from ppdb')
	ppdb_edges     = get_edges(G_ppdb)
	ppdb_one_event = [(a,b,'<ppdb weaker than>') for a,b,c in ppdb_edges if s != t] 
	ppdb_vertex    = list(set(join([[s,t] for s,t,_ in ppdb_one_event])))
	ppdb_edge      = to_edges( ppdb_vertex, ppdb_one_event )

	print('\n\t>> collapse both graph down to one event')
	ngram_one_event = [(s,t,'<ngram weaker than>') for s,t,_ in ngram_no_loops]

	print('\n\t>> combine graph and sharding ...')
	both_one_event = ppdb_one_event + ngram_one_event
	both_vertex    = list(set(join([[s,t] for s,t,_ in both_one_event])))
	both_edge      = list(to_edges( both_vertex, both_one_event ).iteritems())
	chunk_size     = int(float(len(both_edge))/6)
	both_shards    = chunks( both_edge, chunk_size )

	print('\n\t>> saving ppdb graph')
	out_dir    = get_path('ppdb-one-event-no-loop')
	ppdb_graph = {'edge': ppdb_edge, 'vertex': ppdb_vertex}

	with open(os.path.join(out_dir, 'shard.pkl'),'wb') as h:
		pickle.dump(ppdb_graph, h)

	out_both = get_path('ppdb-one-event-ngram-no-loop')

	num = 1

	print('\n\t>> saving ppdb-ngram graph shards')

	for shard in both_shards:

		path = os.path.join(out_both, 'shard-' + str(num) + '.pkl')
		shard_graph = {'edge': shard, 'vertex': both_vertex}

		with open(path,'wb') as h:
			pickle.dump(shard_graph, h)

		num +=1 

make_graphs()

# print('\n\t>> remove loops from ppdb')
# ppdb_edges     = get_edges(G_ppdb)
# ppdb_no_loops  = [(a,b,c) for a,b,c in ppdb_edges if s != t] 
# ppdb_vertex    = list(set(join([[s,t] for s,t,_ in ppdb_one_event])))

# ppdb_one_event = [(s,t,'<ppdb weaker than>') for s,t,_ in ppdb_no_loops]
# ppdb_graph     = to_graph(ppdb_vertex, ppdb_one_event)


















