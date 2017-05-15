############################################################
# Module  : execute test
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
from experiments.bag_coins import *

############################################################
'''
	@Use: given graph and graph_name, and test set
	      run on all tests
'''
def exec_coin(graph_name, tests, decision_fn, results_dir, save = False):

	for test_name, test in tests.iteritems():

		msg = 'ranking ' + test_name + ' with ' + graph_name 
		print('\n\t' + msg)

		out_path = os.path.join(results_dir, graph_name + '-' + test_name + '.txt')

		rank_all_gold( test, decision_fn, out_path, refresh = False, save = save )

