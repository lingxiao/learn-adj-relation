############################################################
# Module  : pointwise estimation baeline
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
from experiments.milp import *


'''
    @Use  : compile word pattern for every pattern
    @Input: s     :: String  word1
            t     :: String  word2
            patts :: Dict String [String]
                      with keys: strong-weak
                                 weak-strong
                      and values that is a list of patterns
    @Output a dictionary of regular expressions for 
            s t at each pattern
'''
def compile_patterns(s,t, patts):

    s_stronger_t = [(R,re.compile(parse_re(R,[s,t]))) for R in patts['strong-weak']] \
                 + [(R,re.compile(parse_re(R,[t,s]))) for R in patts['weak-strong']]

    s_weaker_t  = [(R,re.compile(parse_re(R,[s,t]))) for R in patts['weak-strong']]  \
                + [(R,re.compile(parse_re(R,[t,s]))) for R in patts['strong-weak']]

    return { s + '>' + t : s_stronger_t, s + '<' + t : s_weaker_t }

'''
	@Use: open all ngrams in ngram_dir and yield outputs
'''
def with_ngrams(ngram_path):

	parse  = lambda s : (s.split('\t')[0], s.split('\t')[1])

	# for path in out_paths:            
	with open(ngram_path,'rb') as h:
		for line in h:
			if line and '===' not in line:
				xsn = line.split('\t')
				if len(xsn) == 2:
					xs,n = line.split('\t')
					yield (xs, float(n))

############################################################
'''
	get paths
'''
all_ngram  = get_path('ngram-all')
dev_ngram  = get_path('ngram-dev')
milp_ngram = get_path('ngram-milp')
pattern_dir = get_path('patterns')

patterns = read_pattern(pattern_dir)

ngram_dir = dev_ngram
out_paths = [os.path.join(ngram_dir, p) for p in os.listdir(ngram_dir) \
            if '.txt' in p]

ngram_path = out_paths[0]

ngrams = []

# for xsn in with_ngrams(out_paths[0]):
	# ngrams.append(xsn)












