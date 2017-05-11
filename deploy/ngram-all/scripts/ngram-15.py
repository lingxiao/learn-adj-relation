############################################################
# Module  : A series of measures on the graph for experiments
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
from utils   import *
from scripts import *
from app     import *

############################################################
'''
	paths
'''
word_dirs = working_dirs( 'words'
	                    , [p + '-' + s for p in ['train', 'valid', 'all'] \
	                                   for s in ['pairs', 'words'] ])

out_dirs   = data_dirs( 'ngram-all'
	                  , ['outputs'
	                  , 'no-data'])

pair_dir   = word_dirs['all-pairs']

log_dir    = word_dirs['log']

'''
	@Use: collect ngram counts
'''
batch = 15

pair_path    = os.path.join( pair_dir
	 					   , 'batch-' + str(batch) + '.txt')

no_data_path = os.path.join( out_dirs['no-data']
	                       , 'batch-' + str(batch) + '-no-data.txt')

pattern_path = get_path('patterns')

ngram_dir    = get_path('ngram-grep')


'''
	run function
'''
collect_ngram_patterns( pair_path
	                  , pattern_path
	                  , no_data_path
	                  , ngram_dir
	                  , out_dirs['outputs']
	                  , word_dirs['log']
	                  , refresh = True
	                  , debug   = False)

