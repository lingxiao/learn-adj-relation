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
	@Use: given a graph with multiple labels for adverbs
		  collpas to one label for adverbs
'''
def collapse_graph(graph):

	print('\n\t>> get ppdb-ngram edges')

	vertex = graph.vertices
	edges  = { v : dict() for v in vertex }

	print('\n\t>> converting edges ...')
	for src,out in graph.edges.iteritems():
		for tgt,es in out.iteritems():
			if src != tgt:
				es    = graph.edges[src][tgt]
				ngram  = [n for x,n in es.iteritems() if x == '<is weaker than>']
				adverb = [n for x,n in es.iteritems() if x != '<is weaker than>']
				out    = {'<ngram weaker than>': sum(ngram), '<ppdb weaker than>': sum(adverb)}
				
				edges[src][tgt] = out

	print('\n\t>> sharding edges ...')
	size   = int(float(len(edges))/6)
	shards = chunks(list(edges.iteritems()), size)

	print('\n\t>> saving ppdb-ngram graph shards')
	out_both = get_path('ppdb-one-event-ngram-no-loop')
	num = 1

	for shard in shards:
		path  = os.path.join(out_both, 'shard-' + str(num) + '.pkl')
		shard = { k:v for k,v in shard }
		shard_graph = {'edge': shard, 'vertex': vertex}

		with open(path,'wb') as h:
			pickle.dump(shard_graph, h)

		num +=1 

















