############################################################
# Module  : A series of measures on the graph for experiments
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import numpy as np

from utils   import *
from scripts import *
from app.config import *

############################################################
'''
	paths
'''
batch = 23

# dirs       = working_dirs('dot-product',['pairs', 'scripts','shells'])
out_dirs   = data_dirs('dot-product', ['outputs'])

word_dirs = working_dirs( 'words'
	                    , [p + '-' + s for p in ['train', 'valid', 'all'] \
	                                   for s in ['pairs', 'words'] ])

word_2_vec     = get_path('word2vec')
word_2_vec_sm  = get_path('word2vec-sm')


current_job    = 'all-pairs'

word_pair_path = os.path.join(word_dirs[current_job]  , 'batch-' + str(batch) + '.txt')
out_path       = os.path.join(out_dirs['outputs']     , current_job + '-' + str(batch) + '.txt')

print('\n>> running dot-' + str(batch) + '.py at ' + current_job)
dot(word_2_vec, word_pair_path, out_path, refresh = True)
