############################################################
# Module  : Graph Class
# Date    : April 3rd, 2017
# Author  : Xiao Ling, merle
############################################################

from scripts.graph import *
from app.config import *

'''

	Graph class and associated functions. 


	Class parameters:

	* graph_path :: String, path to multi-directed graph to be loaded

	* edge_wt_dir :: String, path to directory with graph edge so it can be represented
	                 as a directed-graph

	                 Optional. If no path, load as uniform graph

	* ppr_dir    :: String, path to precomputed ppr. Optional. if it does not exist
	                then compute using internal nx.DiGraph api             		 

	Class methods:

	- edge :: String -> String -> [(String, String, String)] 
	         given vertices s and t, output all edges in s,t as list of : (s, t, adverb)

	- wtedge :: String -> String -> Float
	        given vertices s and t, output weight of edge s -> t
	        if no edge exist, output 0


	- mgraph :: [(String, String, String)]
	        output entire raw multi directed graph in list of tuples of form: (s,t,adverb)
	        where (s,t,adverb) signals:

			s + adverb = t

	- ppr :: String -> Float -> Dict String Float. 
	        compute the personalized page rank of vertex s at reset constant alpha

	- ppr_vec :: String -> Dict String Float
			compute personalized page rank of t from s for every t

	- Ex :: String -> Float
			E[X_st] = \sum_{r \in neigh(s)} X_sr

	- train_data :: { 'graph' :: [(String,String,String)], 'base' :: String, 'compare' :: String, 'superla' :: String}
	          output partial graph with base, comparative, superlative vertices and their edges

'''
class Graph:

	def __init__(self
		         , name       = None
		         , asset_dirs = None):

		print('\n>> constructing graph ' + name + ' ...')

		splits = name.split('|')

		'''
			get type of graph and how the edge weight is constructed
			default ppr alpha = 0.85, otherwise get specified ppr
		'''
		if len(splits) == 2:
			graph_name = splits[0]
			edge_type  = splits[1]
			alpha      = '0.8'
			print ('\n>> did not specify alpha. Default to ' + alpha)

		elif len(splits) == 3:
			graph_name = splits[0]
			edge_type  = splits[1]
			alpha      = splits[2]

		else:
			raise NameError("Error: expected name of form graph|weight|float")

		'''
			get all paths
		'''
		graph_path       = get_path(graph_name)
		degree_path_name = edge_type + '-' + graph_name
		degree_path      = asset_dirs[degree_path_name]
		ppr_path         = asset_dirs[degree_path_name + '-' + alpha]
		train_dir        = get_path('bcs')

		if os.path.exists(graph_path):

			G,W,E,V = load_as_digraph(graph_path, degree_path)

			self.graph    = G
			self.weights  = W
			self.edges    = E
			self.vertices = V
			self.labels   = set(join(join([[z for z,_ in x.iteritems()] for _,x in e.iteritems() ] for _,e in E.iteritems())))
			self.alpha    = alpha
			self.PATH     = { 'train': train_dir, 'ppr' : ppr_path }

		else:
			raise NameError('Error: ' + graph_path + ' does not exist')

	############################################################
	'''
		graph topology
	'''

	def out_neigh(self,src):
		E = self.edges
		if src in E:
			return E[src]
		else:
			return dict()

	'''
		@Use: given target `tgt`, get all parents of tgt and
			  the edge from parent to target
	'''
	def in_neigh(self,tgt):

		E = self.edges
		if tgt in E:
			return { _s :_d[tgt] for _s,_d in E.iteritems() if tgt in _d } 
		else:
			return dict()

	'''
		@Use: output in and out neighbors
	'''
	def neigh(self,src):
		in_vs  = self.in_neigh(src)
		out_vs = self.out_neigh(src)

		return { k:v for k,v in list(in_vs.iteritems()) + list(out_vs.iteritems()) }


	############################################################
	'''
		edge and ppr meaures
	'''

	'''
		@use: given vertices s and t
		 	  output raw edges between them, and weight of edge
	'''
	def edge(self,src,tgt):

		E = self.edges
		W = self.weights

		if src in E:
			if tgt in E[src]: 
				if tgt in W[src]:
					return E[src][tgt], W[src][tgt]
				else:
					return E[src][tgt], 0.0
			else:
				return dict(), 0.0
		else:
			raise NameError('Error: ' + s + ' no in graph')

	def ppr(self,src = '', tgt = '', alpha = None):

		if not alpha:

			return self.ppr(src, tgt, alpha = self.alpha)

		else:

			if float(alpha) == float(self.alpha):

				ppr_dir = self.PATH['ppr']
				name    = src + '-' + str(alpha) + '.pkl'
				path    = os.path.join(ppr_dir,name)

				if os.path.exists(path):
					pi = pickle.load(open(path,'rb'))
					if tgt in pi:
						return pi[tgt]
					else:
						return 0.0
				else:
					pi = self.compute_ppr(src = src, alpha = float(alpha))
					if tgt in pi:
						return pi[tgt]
					else:
						return 0.0

			else:
				pi = self.compute_ppr(src = src, alpha = float(alpha))
				if tgt in pi:
					return pi[tgt]
				else:
					return 0.0


	def compute_ppr(self, src = '', alpha = 0.85):

		G = self.graph

		personal      = {w : 0 for w in self.vertices}
		personal[src] = 1.0
		ppr           = nx.pagerank(G
			                       , personalization = personal
			                       , alpha = float(alpha))
		return ppr  

	
	def compute_page_rank(self):
		G = self.graph
		rank = nx.pagerank(G)
		return rank

	
	def train_data(self):

		train_dir = self.PATH['train']
		
		train_X = train_vertices(train_dir)

		return train_X


	############################################################
	'''
		logistic regression features
	'''

	'''
		represent vertex `src` as coin
	'''
	def coin(self,src):
		return edge_binomial(src,self)


############################################################
'''
	measures that succeeded in edge_measure.py 
	is migrated here

	@Use: compute beronoulli variable probability
	@Input: - src   :: String
			- graph :: Graph
'''
def edge_binomial(src, graph):

	parents = graph.in_neigh (src)
	childs  = graph.out_neigh(src)

	probs      = { 'H': 0, 'T': 0, '|H|': 0, '|T|': 0 } 
	eps        = 1e-5
	in_degree  = sum(join([n for _,n in edge.iteritems()] for _,edge in parents.iteritems()))
	out_degree = sum(join([n for _,n in edge.iteritems()] for _,edge in childs.iteritems() ))

	head = in_degree  + eps
	tail = out_degree + eps
	tot  = float(head + tail)

	probs['H']   = head / tot
	probs['T']   = tail / tot
	probs['|H|'] = head
	probs['|T|'] = tail

	return probs



