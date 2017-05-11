############################################################
# Module  : A series of measures on the graph for experiments
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import pickle
from collections import Counter
from utils   import *
from scripts import *
from app     import *

############################################################
'''
	paths
'''

batch = 8

'''
	grab all batch of words
'''
word_dirs = working_dirs( 'words'
	                    , [p + '-' + s for p in ['train', 'valid', 'all'] \
	                                   for s in ['pairs', 'words'] ])

'''
	construct all output directory in learn-adj-relation-data
'''
out_dirs   = data_dirs( 'expected-value' , [p + '-' + q + r    \
	                                        for p in ['coin','die']  \
	                                        for q in [ 'ngram'
	                                                 , 'ngram-bool'
	                                                 , 'ppdb'
	                                                 , 'ppdb-ngram'
	                                                 , 'ppdb-ngram-bool']
	                                        for r in ['-smooth', '']])


log_dir     = word_dirs['log']
word_path   = os.path.join( word_dirs['all-words'], 'batch-' + str(batch) + '.txt')

'''
	get all graph paths
'''

gr_ppdb       = get_path('ppdb'            )

gr_ngram      = get_path('ngram'           )
gr_ngram_bool = get_path('ngram-bool'      )

gr_ppdb_ngram      = get_path('ppdb-ngram'      )
gr_ppdb_ngram_bool = get_path('ppdb-ngram-bool' )

############################################################
'''
	@Use: compute expected value for coin and die
'''
def exec_EV(gr_path, word_path, coin, die, eps):

	print ('\n>> running edge_binomial with smoothing constant ' + str(eps))

	edge_binomial( gr_path
		         , word_path
		         , os.path.join(out_dirs[coin], 'batch-' + str(batch) + '.pkl')
		         , eps = eps)

	print ('\n>> running edge_multinomial smoothing constant ' + str(eps))
	edge_multinomial( gr_path
		            , word_path
		            , os.path.join(out_dirs[die], 'batch-' + str(batch) + '.pkl')
		            , eps = eps)

############################################################
'''
	run
'''
eps = 1e-5
suffix = '-smooth'

def exec_all_EV(eps, suffix):

	exec_EV(gr_ppdb      , word_path, 'coin-ppdb'  + suffix     , 'die-ppdb' + suffix      , eps)

	exec_EV(gr_ngram     , word_path, 'coin-ngram' + suffix     , 'die-ngram' + suffix     , eps)
	exec_EV(gr_ngram_bool, word_path, 'coin-ngram-bool' + suffix, 'die-ngram-bool' + suffix, eps)

	exec_EV(gr_ppdb_ngram     , word_path, 'coin-ppdb-ngram' + suffix, 'die-ppdb-ngram' + suffix , eps)
	exec_EV(gr_ppdb_ngram_bool, word_path, 'coin-ppdb-ngram-bool' + suffix, 'die-ppdb-ngram-bool' + suffix , eps)

exec_all_EV(1e-5, '-smooth')
exec_all_EV(0.0 , ''       )


