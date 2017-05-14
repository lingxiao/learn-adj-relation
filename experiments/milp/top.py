############################################################
# Module  : pointwise estimation baeline
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os
import pickle
import numpy as np
import networkx as nx
from pulp    import *

from app     import *
from utils   import *
from scripts import *
from scripts.graph import *
from experiments.argmax import *
from experiments.rank_all import *
from experiments.milp import *

############################################################
'''
	path
'''
work_dir = locate_dirs( get_path('milp'), ['results'] )

'''
	load test sets
'''
try:
	bcs, ccb, moh, mohn, ccbn
except:

	print('\n\t>> load base-comparative-superlative')
	bcs = join(_xs for _, _xs in train_vertices(get_path('bcs')).iteritems())
	bcs = [[[w] for w in _ws] for _ws in bcs]

	print('\n\t>> load turk')
	ccb = read_gold( get_path('ccb') )

	print('\n\t>> load moh')
	moh = read_gold( get_path('moh') )

	print('\n\t>> load moh-no-tie')
	mohn = read_gold( get_path('moh-no-tie') )

	print('\n\t>> load turk-no-tie')
	ccbn = read_gold( get_path('ccb-no-tie') )

	test = {
		  'bcs' : bcs
		, 'ccb' : ccb
		, 'moh' : moh 
		, 'moh-no-tie': mohn
		, 'ccb-no-tie': ccbn
		}

############################################################
'''
	@Use: load ngram stat
'''
ngram_dir  = get_path('ngram-milp')
count_path = get_path('word-count')

with open(os.path.join(ngram_dir,'stat-strong-weak.pkl'),'rb') as h:
	stat = pickle.load(h)		

with open(count_path,'rb') as h:
	count = pickle.load(h)


decide = paper_milp(ngram_dir, stat, count)	
gold = [['sufficient'], ['wide'], ['full']]

words = join(gold)
pairs = [ (s,t) for s in words for t in words if s != t ]

scores = [ (s,t,paper_score(ngram_dir, stat, count)(s,t)) for s,t in pairs ]
no_data = all(v == 0 for _,_,v in scores)
















