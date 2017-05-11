############################################################
# Module  : A series of measures on the graph for experiments
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import json
import pickle
import networkx as nx
from collections import Counter

from utils   import *
from scripts import *
from scripts.graph import *

############################################################

'''
	@Use  : compute page rank for all words in graph at 
	        specfied restart constant and save
	@Input: 
		- `gr_path` :: String   path to multi-digraph
		- `wt_path` :: String   path vertex weights
		- `out_dir`	:: String   path to output directory
		- `log_dir` :: String   path to log output
		- `alpha`   :: Float    random walk reset constant
		- `refresh` :: Bool     if true do no recompute ppr if file already exists
		- `debug`   :: Bool     if true only run for three words

	@output: None. Write results to disk

	@Rasies: NameError if output directory does not exists
'''
def personalized_page_rank( gr_path
	                      , wt_path
	                      , out_dir
	                      , log_dir
	                      , alpha
	                      , refresh = True
	                      , debug   = False):

	if not os.path.exists(out_dir):
		raise NameError('output directory does not exist at ' + out_dir)

	else:

		salpha   = str(alpha)
		srefresh = 'refresh' if refresh else 'restart'
		writer   = Writer(log_dir, 1, debug)

		'''
			Read ppdb graph
		'''
		G_ppdb, _, _, words  = load_as_digraph( gr_path, wt_path )

		if debug: ws   = words[0:3]
		else:     ws   = words

		writer.tell('running compute_ppr at constant ' 
			       + salpha 
			       + ' in ' 
			       + srefresh
			       + ' mode') 

		for w in ws:

			out_path = os.path.join(out_dir, w + '-' + salpha + '.pkl')

			if os.path.exists(out_path) and refresh:
				writer.tell('skipping exiting file: ' + out_path)
			else:

				personal    = {w : 0 for w in words}
				personal[w] = 1.0

				ppr = nx.pagerank(G_ppdb, personalization = personal, alpha = alpha)

				with open(out_path, 'wb') as h:
					pickle.dump(ppr, h)

		writer.tell('Done')

############################################################
'''
	@Use: given file of words `s`
		  compute the prob(s -> t) for every t in 
		  out-neighbor of s
'''
def out_degree_uniform(word_path, graph_path, out_dir):
	return go_out_degree(compute_degree_uniform
		                , word_path
		                , graph_path
		                , out_dir)


def out_degree_edge_wt(word_path, graph_path, out_dir):
	return go_out_degree(compute_degree_edge_wt
		                , word_path
		                , graph_path
		                , out_dir)



'''
	@Use: compute outdegree based on thoughts of:
	      https://cdn2.hubspot.net/hubfs/489432/docs/Iterative_Ranking_from_Pair-wise_Comparisons.pdf
'''
def out_degree_BTL(word_path, graph_path, out_dir):
	return go_out_degree( compute_out_degree_BTL
		                , word_path
		                , graph_path
		                , out_dir )


def go_out_degree(fn, word_path, graph_path, out_dir):

	E,_ = load_as_dict(graph_path)

	with open(word_path,'rb') as h:

		for word in h:

			word = word.replace('\n','')
			out_path = os.path.join(out_dir, word + '.pkl')

			if os.path.exists(out_path):
				os.remove(out_path)

			with open(out_path, 'wb') as f:
				if word in E:
					d = fn(word,E)
				else:
					d = dict()
				pickle.dump(d,f)


'''
	@Use: compute probability of transition
		  to neighbor by uniform probability

		  that is: Pr(s -> t) = 1 / |neigh(s)|
'''
def compute_degree_uniform(src,E):
	out_neigh = E[src]
	neigh_sz  = float(len(out_neigh))
	return {tgt : 1/neigh_sz for tgt,_ in out_neigh.iteritems()}

'''
	@Use: compute probability of transition
		  to neighbor by number of edges

'''
def compute_degree_edge_wt(src,E):

	neigh_sz  = float(sum(join([n for _,n in d.iteritems()] \
		        for _,d in E[src].iteritems())))

	out = dict()

	for tgt, prob in E[src].iteritems():
		wt = sum(n for _,n in prob.iteritems())/neigh_sz
		out[tgt] = wt

	return out


'''
	@Use: compute outdegree based on thoughts of:
	      https://cdn2.hubspot.net/hubfs/489432/docs/Iterative_Ranking_from_Pair-wise_Comparisons.pdf

'''
def compute_out_degree_BTL(src,E):

	A_src  = dict()
	neigh  = E[src]

	for tgt, out_edges in neigh.iteritems():

		if src in E[tgt]:
			in_edges = E[tgt][src]
		else:
			in_edges = dict()

		num_win  = float(sum(n for _,n in in_edges.iteritems()))
		num_loss = float(sum(n for _,n in out_edges.iteritems()))

		A_src[tgt] = num_loss / (num_win + num_loss)

	if A_src:

		max_deg = max(w for _,w in A_src.iteritems())
		tot_deg = sum(w for _,w in A_src.iteritems())

		A_src = { tgt : v/tot_deg for tgt,v in A_src.iteritems() }

	return A_src


E,V = load_as_dict(get_path('ppdb'))

############################################################
'''
	page rank tutorials
'''
def page_rank_unit_test_1():
	'''
		construct graph where 1 is a sink
	'''
	G = nx.DiGraph()

	[G.add_node(k) for k in [1,2,3,4]]
	G.add_edge(2,1)
	G.add_edge(3,1)
	G.add_edge(4,1)

	# vary parameters
	ppr1     = nx.pagerank(G,personalization={1:1, 2:0, 3:0, 4:0})
	ppr1_5   = nx.pagerank(G,personalization={1:1, 2:0, 3:0, 4:0}, max_iter = 5)
	ppr1_100 = nx.pagerank(G,personalization={1:1, 2:0, 3:0, 4:0}, max_iter = 100)


	ppr2     = nx.pagerank(G,personalization={1:0, 2:1, 3:0, 4:0})
	ppr2_100 = nx.pagerank(G,personalization={1:0, 2:1, 3:0, 4:0}, max_iter = 100)
	ppr2_500 = nx.pagerank(G,personalization={1:0, 2:1, 3:0, 4:0}, max_iter = 500)

	ppr3 = nx.pagerank(G,personalization={1:0, 2:0, 3:1, 4:0})

	'''
		for ppr, the lower the alpha, the more likely that the random walk will 
		end up where I started given that v1 is a sink
	'''
	ppr3_a1 = nx.pagerank(G,personalization={1:0, 2:0, 3:1, 4:0}, alpha = 0.90, max_iter = 500)
	ppr3_a2 = nx.pagerank(G,personalization={1:0, 2:0, 3:1, 4:0}, alpha = 0.75)
	ppr3_a3 = nx.pagerank(G,personalization={1:0, 2:0, 3:1, 4:0}, alpha = 0.50)
	ppr3_a4 = nx.pagerank(G,personalization={1:0, 2:0, 3:1, 4:0}, alpha = 0.25)
	ppr3_a5 = nx.pagerank(G,personalization={1:0, 2:0, 3:1, 4:0}, alpha = 0.10)
	ppr3_a6 = nx.pagerank(G,personalization={1:0, 2:0, 3:1, 4:0}, alpha = 0.01)

def page_rank_unit_test_2():

	'''
		construct graph where 1 is a source
	'''
	G = nx.DiGraph()

	[G.add_node(k) for k in [1,2,3,4]]
	G.add_edge(1,2)
	G.add_edge(1,3)
	G.add_edge(1,4)

	# vary iterations
	ppr1     = nx.pagerank(G,personalization={1:1, 2:0, 3:0, 4:0})
	ppr1_100 = nx.pagerank(G,personalization={1:1, 2:0, 3:0, 4:0}, max_iter = 100)
	ppr1_500 = nx.pagerank(G,personalization={1:1, 2:0, 3:0, 4:0}, max_iter = 500)

	ppr2     = nx.pagerank(G,personalization={1:0, 2:1, 3:0, 4:0})
	ppr2_100 = nx.pagerank(G,personalization={1:0, 2:1, 3:0, 4:0}, max_iter = 100)
	ppr2_500 = nx.pagerank(G,personalization={1:0, 2:1, 3:0, 4:0}, max_iter = 500)

	ppr3 = nx.pagerank(G,personalization={1:0, 2:0, 3:1, 4:0})

	'''
		the lower the alpha, the more likely that random walk will end up where I started

		so 1 - alpha is the probability of restarting
	'''
	ppr3_a1 = nx.pagerank(G,personalization={1:0, 2:0, 3:1, 4:0}, alpha = 0.90, max_iter = 500)
	ppr3_a2 = nx.pagerank(G,personalization={1:0, 2:0, 3:1, 4:0}, alpha = 0.75)
	ppr3_a3 = nx.pagerank(G,personalization={1:0, 2:0, 3:1, 4:0}, alpha = 0.50)
	ppr3_a4 = nx.pagerank(G,personalization={1:0, 2:0, 3:1, 4:0}, alpha = 0.25)
	ppr3_a5 = nx.pagerank(G,personalization={1:0, 2:0, 3:1, 4:0}, alpha = 0.10)
	ppr3_a6 = nx.pagerank(G,personalization={1:0, 2:0, 3:1, 4:0}, alpha = 0.01)
