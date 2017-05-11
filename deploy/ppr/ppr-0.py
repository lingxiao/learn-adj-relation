############################################################
# Module  : compute ppr
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os

import shutil
import pickle
import operator
import json
import networkx as nx
from networkx.readwrite import json_graph

from app     import *
from utils   import *
from scripts import *
from scripts.graph import *
from experiments.elementary.top import *

############################################################
'''
	paths
'''
alphas = [0.9,0.8,0.7,0.5,0.25,0.1,0.01]

'''
	get all graph paths
'''
gr_ppdb            = get_path('ppdb'       )
gr_ngram           = get_path('ngram'      )
gr_ngram_bool      = get_path('ngram-bool' )
gr_ppdb_ngram      = get_path('ppdb-ngram'      )
gr_ppdb_ngram_bool = get_path('ppdb-ngram-bool' )


keys = [s + '-' + t \
	   for s in ['uniform', 'edge-wt', 'BTL' ]  \
	   for t in [ 'ngram'
                , 'ngram-bool'
                , 'ppdb'
                , 'ppdb-ngram'
                , 'ppdb-ngram-bool']]

out_root  = data_dirs( 'ppr' , [s + '-' + str(_a) for s in keys for _a in alphas ])
wt_root   = data_dirs( 'out-degree' , keys )

############################################################
'''
	experiment function
'''
def exec_ppr(gr_path, wt_root_key, a):

	out_root_key = wt_root_key + '-' + str(a)

	personalized_page_rank( gr_path
		                  , wt_root [wt_root_key]
		                  , out_root[out_root_key]
		                  , out_root['log']
		                  , a
		                  , refresh = True
		                  , debug   = False)

############################################################

alpha = 0

print('\n>> ppr over ppdb-ngram graph')
exec_ppr(gr_ppdb_ngram, 'BTL-ppdb-ngram', alpha)

print('\n>> ppr over ppdb-ngram-bool graph')
exec_ppr(gr_ppdb_ngram_bool, 'BTL-ppdb-ngram-bool', alpha)

print('\n>> ppr over ppdb graph')
exec_ppr(gr_ppdb, 'BTL-ppdb', alpha)

print('\n>> ppr over ngram graph')
exec_ppr(gr_ngram, 'BTL-ngram', alpha)

print('\n>> ppr over ngram-bool graph')
exec_ppr(gr_ngram_bool, 'BTL-ngram-bool', alpha)

if False:
	print('\n>> ppr over ppdb graph')
	exec_ppr(gr_ppdb, 'uniform-ppdb', alpha)
	exec_ppr(gr_ppdb, 'edge-wt-ppdb', alpha)

	print('\n>> ppr over ngram graph')
	exec_ppr(gr_ngram, 'uniform-ngram', alpha)
	exec_ppr(gr_ngram, 'edge-wt-ngram', alpha)

	print('\n>> ppr over ngram-bool graph')
	exec_ppr(gr_ngram_bool, 'uniform-ngram-bool', alpha)
	exec_ppr(gr_ngram_bool, 'edge-wt-ngram-bool', alpha)

	print('\n>> ppr over ppdb-ngram graph')
	exec_ppr(gr_ppdb_ngram, 'uniform-ppdb-ngram', alpha)
	exec_ppr(gr_ppdb_ngram, 'edge-wt-ppdb-ngram', alpha)

	print('\n>> ppr over ppdb-ngram-bool graph')
	exec_ppr(gr_ppdb_ngram_bool, 'uniform-ppdb-ngram-bool', alpha)
	exec_ppr(gr_ppdb_ngram_bool, 'edge-wt-ppdb-ngram-bool', alpha)













