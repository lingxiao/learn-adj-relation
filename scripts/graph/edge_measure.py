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
	@Use: compute beronoulli variable probability
	@Input: - gr_path   :: String
			- word_path :: String
			- out_path  :: String
			- eps       :: Float
			- debug     :: False
'''
def edge_binomial( gr_path
			     , word_path
				 , out_path
				 , eps = 0.0
				 , debug = False):
	
	print('\n\t>> runing edge_binomial over words from ' + word_path)

	if not debug and os.path.exists(out_path):
		print('\n\t>> removing existing probability table if any')
		os.remove(out_path)

	print('\n\t>> loading graph from ' + gr_path)
	words = [w for w in open(word_path,'rb').read().split('\n') if w]
	E,V   = load_as_dict(gr_path)

	probs = { s : {'H': 0, 'T': 0, '|H|': 0, '|T|': 0} \
	        for s in words}

	print('\n\t>> constructing probs table')

	for src,table in probs.iteritems():

		if src in E:

			parents  = [pa for pa in V if src in E[pa]]
			parents  = [E[par][src] for par in parents]

			in_edges  = sum(join([n for _,n in par.iteritems()] for par in parents))
			out_edges = sum(join([n for _,n in d.iteritems()] for _,d in E[src].iteritems()))

		else:
			in_edges  = 0
			out_edges = 0

		'''
			smooth with eps. Note eps may be 0
		'''
		head      = in_edges  + eps
		tail      = out_edges + eps
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

	if not debug:
		print('\n\t>> saving output to ' + out_path)
		with open(out_path, 'wb') as h:
		    pickle.dump(probs, h, protocol=pickle.HIGHEST_PROTOCOL)

	return probs


'''
	@Use: edge multinomial
	@Input: - gr_path   :: String
			- word_path :: String
			- out_path  :: String
			- eps       :: Float
'''

def edge_multinomial(gr_path, word_path, out_path, eps = 0.0, debug = False):

	if not debug and os.path.exists(out_path):
		print('\n\t>> removing probs table if it exists')
		os.remove(out_path)

	print('\n\t>> opening words from ' + word_path)
	words = [w for w in open(word_path,'rb').read().split('\n') if w]
	E,V   = load_as_dict(gr_path)

	'''
		construct sample space omega: {-K, ..., K} 
	'''
	connected = [_word for _word in V if E[_word]]

	max_K = max(max(sum(n for _,n in d.iteritems()) \
		   for _,d in E[_word].iteritems()) \
		   for _word in connected)

	print('\n\t>> constructing Omega ranging over {-' 
		 + str(max_K) + ',...,' + str(max_K) + '}')
	neg_omega = sorted(-k for k in xrange(1,max_K + 1))
	omega     = neg_omega + range(0,max_K + 1)

	probs = { s : None for s in words }

	print('\n\t>> constructing probability table')

	for src in probs:

		dist = dict()

		parents        = [E[pa][src] for pa in V if src in E[pa]]
		n_in_neighbor  = [sum(n for _,n in pa.iteritems()) for pa in parents]

		if src in E:
			n_out_neighbor = [sum(n for _,n in d.iteritems()) for _,d in E[src].iteritems()]
		else:
			n_out_neighbor = []

		for om in omega:
			if om < 0: 
				d = len([x for x in n_out_neighbor if -x == om])
				if d: dist[om] = d
			else:
				d = len([x for x in n_in_neighbor if x == om])
				if d: dist[om] = d

		'''
			meta information about elementary events
		'''
		dist['<META>'] = {'lower': -max_K, 'upper': max_K, 'smooth': eps}

		probs[src] = dist


	'''
		save
	'''
	if not debug:
		print('\n\t>> saving output to ' + out_path)
		with open(out_path, 'wb') as h:
			pickle.dump(probs, h, protocol=pickle.HIGHEST_PROTOCOL)

	return probs

'''
	@Use: given eleemntary event space `omega` :: Dict String _
		  a sparse representation
		  output all elementary events and their probability
'''
def with_Omega(omega):

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
	@Use: compute beronoulli variable probability
'''
def edge_binomial_from_list(gr_path, word_path, out_path,debug=True):

	if os.path.exists(out_path):
		os.remove(out_path)

	G     = Graph(gr_path)
	words = [w for w in open(word_path,'rb').read().split('\n') if w]
	E,V   = load_as_list(gr_path)

	probs = { s : {'H': 0, 'T': 0, '|H|': 0, '|T|': 0} \
	        for s in words}

	eps = 1e-10
 
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

	if not debug:
		with open(out_path, 'wb') as h:
		    pickle.dump(probs, h, protocol=pickle.HIGHEST_PROTOCOL)
	return probs	    

def edge_multinomial_from_list(gr_path, word_path, out_path, eps = 0.0, debug = False):

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
	if not debug:
		with open(out_path, 'wb') as h:
		    pickle.dump(probs, h, protocol=pickle.HIGHEST_PROTOCOL)

	return probs
