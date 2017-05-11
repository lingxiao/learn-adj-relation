############################################################
# Module  : Load PPDB graph in variety of formats
# Date    : April 3rd, 2017
# Author  : Xiao Ling, merle
############################################################

import os
import json
import pickle
import networkx as nx
from networkx.readwrite import json_graph

from utils   import *
from scripts import *

############################################################
'''
	@Use: Given path to multi directed graph, and path to 
	      weighted vertex output weighted directed graph 
	      and all words in graph

	@Input: `gr_path`    :: String
	        `edge_weight_dir` :: String

	@output: networkx.classes.digraph.Digragh, words
'''
def load_as_digraph(graph_path, edge_wt_dir):

	print('\n>> loading raw direct graph')
	E,V =  load_as_dict(graph_path)

	print('\n>> creating direct graph and adding all vertices')
	G   = nx.DiGraph()
	[G.add_node(s) for s in V]

	if not edge_wt_dir:

	 	print('\n>> WARNING: cannot find directory for weight of edges, loading graph with uniform edges')
		u_edges = join([(src,tgt) for tgt,_ in d.iteritems()] for src,d in E.iteritems())
		[G.add_edge(s,t) for s,t in u_edges]

	else:

		print('\n>> adding all edges')
		wt_paths  = [os.path.join(edge_wt_dir,p) for p in \
		             os.listdir(edge_wt_dir) if '.pkl' in p]

		'''
			weight dict
		'''
		W = { s : dict() for s in V }

		for path in wt_paths:
			src = path.split('/')[-1]
			src = src.replace('.pkl', '')

			with open(path,'rb') as h:
				neigh = pickle.load(h)
				for tgt,p in neigh.iteritems():
					G.add_edge(src,tgt, weight = p)
					W[src][tgt] = p


	return G, W, E, V


############################################################
'''
	@Use: given path to graph, open edge as form:
		  	word_s:
		  		word_s_1: 
		  			adv_1: count
		  			adv_2  count
		  			...
		  		word_s_2
		  		...
		  	so that we have, ie for edge set `E`
				E['good']['great']['<very'>] = 100
	@Input: path  :: String
	@output: (edges,vertices) :: Dict String (Dict String (Dict String Int))
	                           , [String]
'''
def load_as_dict(path):

	if os.path.isdir(path):

		paths = [os.path.join(path,p) for p in os.listdir(path)]

		E = []
		V = None

		for path in paths:

			es,vs = load_as_dict(path)
			E += [(k,v) for k,v in es.iteritems()]
			V  = vs

		all_E = {k : v for k,v in E}

		return all_E, V

	elif os.path.isfile(path):

		_,ext = path.split('.')

		if ext == 'pkl':
			with open(path,'rb') as h:
				G = pickle.load(h)

				return G['edge'], G['vertex']

		else:
			raise NameError("expected pkl file")

	else:
		raise NameError("expected pkl file or directory of pkl file")

'''@Depricated
	@Use: given path to json file, load graph as
			(adj1, adj2, <adv>)
		  where `<adv> adj1` paraphrases `adj2`
		  and list of vertices

		If path invalid, return empty lists
'''
# load_as_list :: FilePath -> [(String,String, String)], [String]
def load_as_list(path):

	'''
		if directory, then open each graph shard and concat
		see scripts/make_ngram_ppdb.py for details 
	'''
	if os.path.isdir(path):
		paths = [os.path.join(path,p) for p in os.listdir(path)]

		E, V = [], []

		for path in paths:

			es,vs = load_as_list(path)
			E += es
			V += vs

		return E, list(set(V))

	if os.path.isfile(path):
		_,ext = path.split('.')

		if ext == 'txt':
			return load_txt_as_list(path)
		elif ext == 'json':
			return load_json_as_list(path)
		else:
			raise NameError('ERROR: expected txt or json format')

	else:
		raise NameError('ERROR: Path is not a directory, .json or .txt file')



############################################################

def load_json_as_list(path):

	with open(path, 'r') as f:
		raw_graph  = json.load(f)

	vertices = raw_graph['nodes']
	words    = [v['id'] for v in raw_graph['nodes']]
	edges    = [to_edge(edge, vertices) for edge in raw_graph['links']]

	return edges, words

def load_txt_as_list(path):

	edges    = []
	vertices = []

	with open(path,'rb') as h:
		for line in h:
			line = line.replace('\n','')
			edge = line.split(', ')
			if len(edge) == 3:
				s,t,v = edge
				edges.append((s,t,v))
				vertices += [s,t]

	vertices = list(set(vertices))

	return edges,vertices

def to_edge(edge, vertices):
	u = vertices[edge['source']]['id']
	v = vertices[edge['target']]['id']
	e = '<' + edge['adverb'] + '>'
	return (u,v,e)

############################################################
'''
	load raw json file as multidigraph
'''

def load_as_multi_digraph(path):
    with open(path, 'r') as infile:
        networkx_graph = json_graph.node_link_graph(json.load(infile))
    return networkx_graph

def multi_digraph_to_json(networkx_graph):
    return json.dumps(json_graph.node_link_data(self.nx_graph))

