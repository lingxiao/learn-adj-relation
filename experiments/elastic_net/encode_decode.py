############################################################
# Module  : encode and decode adverb features
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os
import pickle
import numpy as np


from app     import *
from utils   import *
from scripts import *
from scripts.graph import *
from experiments.argmax import *
from experiments.rank_all import *
from experiments.elastic_net import *

############################################################
'''
	@Use: given ppdb-ngram graph, output word-to-index and index-to-word
		  encoding

		  each word-to-index is of form:
		  	<adverb>: idx, mu, sigma

		  each index-to-word is of form:
		  	idx: <adverb>, mu, sigma
'''
def encode(graph, top_n, out_dir):

	w2idx_path = os.path.join( out_dir
		                     , 'w2idx-' + str(top_n) + '.pkl')

	idx2w_path = os.path.join( out_dir
		                     , 'idx2w-' + str(top_n) + '.pkl')

	print('\n\t>> getting all adverbs and their frequencies')

	num_edges   = float(len(graph.vertices)**2)
	adverb_freq = { v : [] for v in graph.labels }

	for src, out in graph.edges.iteritems():
		for tgt, es in out.iteritems():
			for adv, n in es.iteritems():
				adverb_freq[adv].append(float(n))

	advs = sorted([ (v,sum(ns)) for v,ns in adverb_freq.iteritems() ]
		          , key = lambda x : x[1])

	advs.reverse()

	advs_small = advs[0:top_n]

	vocab = [ (v,n) for v,n in advs_small ]

	print('\n\t>> constructing word2index and index2word')

	idx2w = dict()
	w2idx = dict()

	for i,(adv,n) in enumerate(vocab):
		mu,sig, maxv, minv = stats(adverb_freq[adv], num_edges)

		idx2w[i]   = {'word'  : adv
		             , 'mu'   : mu
		             , 'sigma': sig
		             , 'count': n
		             , 'max'  : maxv
		             , 'min'  : minv}

		w2idx[adv] = {'idx'   : i
		             , 'mu'   : mu
		             , 'sigma': sig
		             , 'count': n
		             , 'max'  : maxv
		             , 'min'  : minv}

	print('\n\t>> saving ...')
	with open(w2idx_path,'wb') as h:
		pickle.dump(w2idx, h)

	with open(idx2w_path,'wb') as h:
		pickle.dump(idx2w, h)

	return w2idx, idx2w


'''
	@Use: given a vector and correpsonding w2idx, output 
		  word to value
'''
def decode(vector, w2idx):

	decoded = { w : None for w,_ in w2idx.iteritems() }

	for w in decoded:
		stat       = w2idx[w]
		decoded[w] = vector[stat['idx']]

	return decoded

############################################################

def all_edges(graph, debug = False):

	if debug:
		vertices = list(graph.vertices)[0:10]
	else:
		vertices = graph.vertices

	for s in vertices:
		for t in vertices:
			yield (s,t)


'''
	@Use: compute expected value and variance of every adverb
		over all possible edges
	 	reconstruct whole sample space with zeros
		and compute variance
'''
def stats(counts, num_edges):

	num_zeros = int(num_edges - len(counts))
	mean      = sum(counts)/num_edges
	
	variance = (sum( (n - mean)**2 for n in counts ) \
	         + num_zeros * (-mean ** 2)) \
		     / num_edges
	
	return mean, variance, max(counts), 0.0	    


