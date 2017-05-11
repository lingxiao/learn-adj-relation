############################################################
# Module  : compute out degree from s for each t:
#           w(s -> t) =             | s -> t | 
#                       ---------------------------------
#                      	 sum_{x \in neigh{t}}  | s -> x|
# 
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import shutil
import pickle
from app     import *
from utils   import *
from scripts import *
from experiments import *

############################################################
'''
	paths
'''
word_dir = working_dirs( 'words'
	                    , [p + '-' + s for p in ['train', 'valid', 'all'] \
	                      for s in ['pairs', 'words'] ])

out_dirs   = data_dirs( 'out-degree' , [s + '-' + t for \
	 								    s in [ 'uniform'
	 								         , 'edge-wt'
	 								         , 'BTL'    ] \

	 								    for t in                   \

	 								    [ 'ngram'
	                                   , 'ngram-bool'
	                                   , 'ppdb'
	                                   , 'ppdb-ngram'
	                                   , 'ppdb-ngram-bool']])

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
	run all
'''
batch = 7

word_path   = os.path.join( word_dir['all-words'], 'batch-' + str(batch) + '.txt')

def exec_out_degree(out_degree, prefix):

	print('\n>> computing ' + prefix + ' out_degree for set of words from ')
	print('\n\t' + word_path)

	print('\n>> computing ' + prefix + ' out probs for each vertex in ppdb graph')
	out_degree(word_path
		      ,gr_ppdb
			  ,out_dirs[prefix + '-ppdb'])

	print('\n>> computing ' + prefix + ' out probs for each vertex in ngram graph')
	out_degree(word_path
			  ,gr_ngram
			  ,out_dirs[prefix + '-ngram'])

	print('\n>> computing ' + prefix + ' out probs for each vertex in ngram boolean graph')
	out_degree(word_path
			  ,gr_ngram_bool
			  ,out_dirs[prefix + '-ngram-bool'])

	print('\n>> computing ' + prefix + ' out probs for each vertex in ppdb-ngram graph')
	out_degree(word_path
			  ,gr_ppdb_ngram
			  ,out_dirs[prefix + '-ppdb-ngram'])

	print('\n>> computing ' + prefix + ' out probs for each vertex in ppdb-ngram boolean graph')
	out_degree(word_path
			  ,gr_ppdb_ngram_bool
			  ,out_dirs[prefix + '-ppdb-ngram-bool'])

# exec_out_degree(out_degree_uniform, 'uniform')
# exec_out_degree(out_degree_edge_wt, 'edge-wt')
exec_out_degree(out_degree_BTL    , 'BTL')

