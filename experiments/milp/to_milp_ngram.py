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

    s_sw_t  = [(R,re.compile(parse_re(R,[s,t]))) for R in patts['strong-weak']] 
    t_sw_s  = [(R,re.compile(parse_re(R,[t,s]))) for R in patts['strong-weak']]

    s_ws_t  = [(R,re.compile(parse_re(R,[s,t]))) for R in patts['weak-strong']] 
    t_ws_s  = [(R,re.compile(parse_re(R,[t,s]))) for R in patts['weak-strong']]

    return { s + '<strong-weak>' + t : s_sw_t
           , t + '<weak-strong>' + s : t_ws_s

           , t + '<strong-weak>' + s : t_sw_s
           , s + '<weak-strong>' + t : s_ws_t
           }

'''	
	@Use: parse each file in inpath using patterns and save to output
'''
def parse_each(in_path, patterns):

	s,t      = (in_path.split('/')[-1]).split('-')
	t        = t.replace('.txt','')
	out_path = os.path.join(out_dir, s + '-' + t + '.txt')

	regex  = compile_patterns(s,t,patterns)

	ngrams = { s + '<strong-weak>' + t : [] 
	         , t + '<weak-strong>' + s : []

	         , t + '<strong-weak>' + s : []
	         , s + '<weak-strong>' + t : []
	         }

	print('\n\t>> parsing input ...' )        
	for xs,n in with_ngrams(in_path):
		for patt in ngrams: 
			matches = [ (xs,n) for m in [r.match(xs) for _,r in regex[patt]] if m]
			ngrams[patt] += matches

		
	print('\n\t>> saving output to ' + out_path)
	with open(out_path,'wb') as h:
		for key,ret in ngrams.iteritems():
			h.write('=== ' + key + '\n')
			for r,n in ret:
				h.write(r + '\t' + str(n) + '\n')
			h.write('\n')

############################################################
'''
	get paths
'''
all_ngram   = get_path('ngram-all' )
dev_ngram   = get_path('ngram-dev' )
milp_ngram  = get_path('ngram-milp')
pattern_dir = get_path('patterns'  )

patterns  = read_pattern(pattern_dir)
ngram_dir = dev_ngram
out_dir   = milp_ngram

'''
	@Use: parse each file and put in milp appropriate format
'''
out_paths = [os.path.join(ngram_dir, p) for p in os.listdir(ngram_dir) \
            if '.txt' in p]

for path in out_paths:
	parse_each(path, patterns)












