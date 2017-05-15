############################################################
# Module  : Utility functions
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os
import math
import numpy as np

from app     import *
from utils   import *
from scripts import *
from experiments.rank_all import *

############################################################
'''
	@Use: given graph and graph_name, and test set
	      run on all tests
'''
def exec_rank(graph_name, tests, decision_fn, results_dir, save = False):

	for test_name, test in tests.iteritems():

		msg = 'ranking ' + test_name + ' with ' + graph_name 
		print('\n\t' + msg)

		out_path = os.path.join(results_dir, test_name + '.txt')

		rank_all_gold( test, decision_fn, out_path, refresh = False, save = save )


############################################################
'''
	@Use: compute average in and out degree of G
'''
def mu_sigma_edges(G):

	V = G.vertices

	edges_in  = []
	edges_out = []

	for s in V:

		v_edges_in  = join( [ n for _,n in d.iteritems() ] for _,d in G.in_neigh(s).iteritems() )
		v_edges_out = join( [ n for _,n in d.iteritems() ] for _,d in G.out_neigh(s).iteritems() )

		edges_in.append ( sum(v_edges_in  ))
		edges_out.append( sum(v_edges_out ))

	mu = np.mean(np.array( edges_in  ))

	sigma_in  = np.var(np.array( edges_in  ))
	sigma_out = np.var(np.array( edges_out ))

	return mu, sigma_in, sigma_out

############################################################
'''
	@Use: Given rho and op so that op(rho(s),rho(t)) for every pair
		  and elastic net model

		  output function that takes in X,y and print accruacy to console
'''
def sanity_check(op, rho, net):

	def fn(X, y, log = False):

		right = 0.0
		wrong = 0.0

		cutoff = 0.50

		for (s,t),y in zip( X , y ):

			rho_st = op(rho(s),rho(t)).reshape(1,-1)
			y_raw  = net.predict(rho_st)
			yhat   = 0 if y_raw < cutoff else 1 

			if yhat == y:
				right += 1
			else:
				wrong += 1

			if log:
				print("\n\t>> (" + s + ', ' + t + '), ' + str(y))
				print('\n\t\t>> yhat = ' + str(yhat))

		print('\n\t>> accuracy: ' + str(right/(right + wrong)))

	return fn

