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
		G_ppdb, words  = load_as_digraph( gr_path, wt_path )

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
def out_degree(word_path, graph_path, out_dir):

	E,_ = load_as_list(graph_path)

	with open(word_path,'rb') as h:
		for word in h:
			word = word.replace('\n','')
			out_path = os.path.join(out_dir, word + '.pkl')
			with open(out_path, 'wb') as f:
				d = compute_out_degree(word,E)
				pickle.dump(d,f)

'''
	@Use: given word `src` and edges of graph, compute
	 	  probability of transitioing to each neighbor
	@Input: - src :: String
		    - E   :: [(String, String, String)]

'''
def compute_out_degree(src,E):

	out_neigh = [(s,t,r) for s,t,r in E if s == src]
	neigh_sz  = float(len(out_neigh))

	out = { t : 0.0 for t in set(t for _,t,_ in out_neigh) }

	for tgt in out:
		out[tgt] = len([t for s,t,r in out_neigh if t == tgt]) / neigh_sz

	return out

############################################################

'''
	@Use: compute beronoulli variable probability
	@Input: - gr_path   :: String
			- word_path :: String
			- out_path  :: String
			- eps       :: Float
'''
def edge_binomial(gr_path, word_path, out_path, eps = 0.0):

	if os.path.exists(out_path):
		os.remove(out_path)

	words = [w for w in open(word_path,'rb').read().split('\n') if w]
	E,V   = load_as_list(gr_path)

	probs = { s : {'H': 0, 'T': 0, '|H|': 0, '|T|': 0} \
	        for s in words}

	for s,table in probs.iteritems():
		in_neigh  = [(x,y,z) for x,y,z in E if y == s]
		out_neigh = [(x,y,z) for x,y,z in E if x == s]
		head      = float(len(in_neigh)  + eps)
		tail      = float(len(out_neigh) + eps)
		tot       = head + tail 

		if tot:

			table['H']   = head / tot
			table['T']   = tail / tot
			table['|H|'] = head
			table['|T|'] = tail

			'''
				store infromation about elementary events
			'''
			table['<META>'] = {'Omega': ['H','T'], 'smooth': eps}

	with open(out_path, 'wb') as h:
	    pickle.dump(probs, h, protocol=pickle.HIGHEST_PROTOCOL)


'''@Depricated: using sparse representation instead
	@Use: edge multinomial
	@Input: - gr_path   :: String
			- word_path :: String
			- out_path  :: String
			- eps       :: Float
'''
def edge_multinomial(gr_path, word_path, out_path, eps = 0.0):

	if os.path.exists(out_path):
		os.remove(out_path)

	words = [w for w in open(word_path,'rb').read().split('\n') if w]
	E,V   = load_as_list(gr_path)

	'''
		construct sample space omega: {-K, ..., K} 
	'''
	max_K = [(s,t) for s,t,_ in E]
	max_K = [[k,]*v for k,v in Counter(max_K).items()]
	max_K = max(len(K) for K in max_K)

	neg_omega = sorted(-k for k in xrange(1,max_K + 1))
	omega     = neg_omega + range(0,max_K + 1)

	probs = { s : None for s in words }

	for word in probs:

		'''
			construct distributiion over {-K,...,K}
			with sparse represenation
		'''
		# dist = {o:eps for o in omega}
		dist = dict()

		in_neigh  = [(x,y) for x,y,z in E if y == word]
		out_neigh = [(x,y) for x,y,z in E if x == word]

		in_neigh  = [[k,]*v for k,v in Counter(in_neigh).items()]
		out_neigh = [[k,]*v for k,v in Counter(out_neigh).items()]

		n_in_neigh   = [len(n) for n in in_neigh]
		n_out_neigh  = [len(n) for n in out_neigh]

		for om in omega:
			if om < 0: 
				d = len([x for x in n_out_neigh if -x == om])
				if d: dist[om] = d
			else:
				d = len([x for x in n_in_neigh if x == om])
				if d: dist[om] = d

		'''
			meta information about elementary events
		'''
		dist['<META>'] = {'lower': -max_K, 'upper': max_K, 'smooth': eps}

		probs[word] = dist

	'''
		save
	'''
	with open(out_path, 'wb') as h:
	    pickle.dump(probs, h, protocol=pickle.HIGHEST_PROTOCOL)


'''
	@Use: given eleemntary event space `omega` :: Dict String _
		  a sparse representation
		  output all elementary events and their probability
'''
def Omega(omega):

	meta = omega['<META>']

	if 'Omega' in meta:
		for o in meta['Omega']:
			if o in omega: 
				yield o,omega[o]
			else:
				yield o,eps

	elif 'lower' in meta and 'upper' in meta:
		l_om  = meta['lower']
		u_om  = meta['upper']
		eps   = meta['smooth']

		for o in xrange(l_om, u_om + 1):
			if o in omega: 
				yield o,omega[o]
			else: 
				yield o,eps
	else:
		raise NameError ("Error: Failed to find dense representation for Omega")

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
