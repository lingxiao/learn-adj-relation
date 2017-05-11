############################################################
# Module  : A series of measures on the graph for experiments
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import re
import networkx as nx

from utils   import *
from scripts import *
from app.config import PATH

############################################################
'''
	paths
'''
_root       = os.path.join(PATH['directories']['deploy'], 'ngram-train')
_word_pair_dir = os.path.join(_root, 'pairs')
_output_dir = os.path.join(_root, 'outputs')
_script_dir = os.path.join(_root ,'scripts')

'''
	@Use: collect ngram counts
'''
batch = 28

word_pair_path  = os.path.join(_word_pair_dir  , 'batch-' + str(batch) + '.txt')
pattern_path    = PATH['assets']['patterns']
ngram_dir       = PATH['ngrams']['full']
out_dir         = _output_dir
log_dir         = PATH['directories']['log']


collect_ngram_patterns( word_pair_path
	                  , pattern_path
	                  , ngram_dir
	                  , out_dir
	                  , log_dir
	                  , debug = False)

