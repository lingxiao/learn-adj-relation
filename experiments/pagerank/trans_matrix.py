############################################################
# Module  : construct adjacency and degree matrix
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os
import struct
import pickle
import numpy as np
import networkx as nx
from numpy.linalg import inv

from app     import *
from utils   import *
from scripts import *
from scripts.graph import *
from experiments.pagerank import *

############################################################
'''
	make encode vector decode vector function

	@Use: given graph, and idx2w dict, 
		  construct adjacency matrix		  
		  and degree matrix
'''
def adjacency_degree_martrix(graph, idx2w, debug = False):

	A = []
	D = []

	if debug:
		print('\n\t>> in debug mode, considering 10 words only')
		idx2w = {i:w for i,w in list(idx2w.iteritems())[0:5]}

	for s,src in idx2w.iteritems():
		v    = adjacency_vector(src,graph, idx2w)
		w    = [0.0]*len(idx2w)
		w[s] = sum(v)
		v    = [float(n!=0) for n in v]

		A.append(v)
		D.append(w)

	return np.matrix(A), np.matrix(D)

'''
	@Use: given graph, word src, and idx2w dict, construct adjacency vector
		  for word s	
'''
def adjacency_vector(src, graph, idx2w):

	A_s = [0.0]*len(idx2w)

	for t,tgt in idx2w.iteritems():
		edges, _ = graph.edge(src,tgt)
		if edges:
			A_s[t] = 1.0
		else:
			A_s[t] = 0.0

	return A_s

'''
	@Use: Given matrix of form [[Float]], save to outpath
'''
def save_matrix(matrix, outpath):

	with open(outpath,'wb') as h:
		for vec in matrix:
			w = ','.join(str(n) for n in vec)
			h.write(w + '\n')

'''
	@Use: given matrix A and D, add self loop
'''
def add_self_loop(A,D):

	print('\n\t>> adding self loops ...')

	A_loop = [list(v.flat) for v in A]
	D_loop = [list(w.flat) for w in D]

	for s in range(len(A)):
		A_loop[s][s] = 1.0
		D_loop[s][s] = max(D_loop[s][s],1.0)

	A = np.matrix(A_loop)	
	D = np.matrix(D_loop)	

	return A,D


############################################################
'''
	run
'''
graph     = G_ppng
idx2w     = { i:w for i,w in enumerate(graph.vertices) }
prefix    = 'both'


def run_adjacency_degree_matrix(graph, idx2w, prefix):

	A_outpath = os.path.join(work_dir['matlab'], prefix + '-A.txt')
	D_outpath = os.path.join(work_dir['matlab'], prefix + '-D.txt')

	A,D = adjacency_degree_martrix(graph, idx2w)

	save_matrix(A, A_outpath)
	save_matrix(D, D_outpath)

	return A,D


# run_adjacency_degree_matrix(G_ppng, idx2w, 'both')

# toy example
if False:
	A = np.matrix([[1,1,0,0]
			      ,[0,1,1,0]
			      ,[0,1,1,1]
			      ,[1,0,0,1]])

	D = np.matrix([[2,0,0,0]
				  ,[0,2,0,0]
				  ,[0,0,3,0]
				  ,[0,0,0,2]])

	W = inv(D)*A


A,D = adjacency_degree_martrix(graph, idx2w, debug = False)
A,D = add_self_loop(A,D)
W   = inv(D) * A




# out_path = os.path.join(work_dir['matlab'], 'out.dat')

# data = [1,2,3,4,5,6,7,8,9]

# with open(out_path, 'wb') as data_file:
#     data_file.write(struct.pack('i'*len(data), *data))






















