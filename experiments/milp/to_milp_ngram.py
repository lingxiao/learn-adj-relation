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
def parse_each(in_path, out_dir, patterns):

	s,t      = (in_path.split('/')[-1]).split('-')
	t        = t.replace('.txt','')
	out_path = os.path.join(out_dir, s + '-' + t)

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

		
	print('\n\t>> saving output to ' + out_path + '.txt')
	with open(out_path + '.txt','wb') as h:
		for key,ret in ngrams.iteritems():
			h.write('=== ' + key + '\n')
			for r,n in ret:
				h.write(r + '\t' + str(n) + '\n')
			h.write('\n')

	print('\n\t>> saving output to ' + out_path + '.pkl')
	with open(out_path + '.pkl','wb') as h:
		pickle.dump(ngrams,h)

	ws = ngrams[t + '<weak-strong>' + s] \
	   + ngrams[s + '<weak-strong>' + t]

	sw = ngrams[t + '<strong-weak>' + s] \
	   + ngrams[s + '<strong-weak>' + t]

	ws = sum(n for _, n in ws)   
	sw = sum(n for _, n in sw)   

	return sw, ws

'''
	@Use: parse all files in ngram_dir and put in milp appropriate format
'''
def parse_all(ngram_dir, out_dir, pattern_dir):

	patterns  = read_pattern(pattern_dir)

	out_paths = [os.path.join(ngram_dir, p) for p in os.listdir(ngram_dir) \
	            if '.txt' in p]

	SW = 0
	WS = 0

	for path in out_paths:
		sw, ws = parse_each(path, milp_ngram, patterns)
		SW += sw
		WS += ws

	return SW, WS

############################################################
'''
	get paths and run
'''
all_ngram   = get_path('ngram-all' )
dev_ngram   = get_path('ngram-dev' )
milp_ngram  = get_path('ngram-milp')
pattern_dir = get_path('patterns'  )

print('\n\t>> parsing all ngrams ...')
sw, ws = parse_all(all_ngram, milp_ngram, pattern_dir)		

print('\n\t>> saving gross statistics')
stat = {'strong-weak' : sw, 'weak-strong': ws }

with open( os.path.join(milp_ngram,'stat-strong-weak.pkl'), 'wb') as h:
	pickle.dump(stat,h)








