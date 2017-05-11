############################################################
# Module  : Running ILP for veronica
# Date    : April 12th
# Author  : Xiao Ling, merle
############################################################

import os
import shutil
import pickle

from scripts import *
from utils   import *
from app     import *

from experiments.ilp import *
# from clus_reader import ClusReader
from pulp    import *


############################################################
'''
	open gold
'''
probs    = os.path.join(get_path('data-root'), 'deploy/probs/probs-ngram-ppdb.txt')
test     = os.path.join(get_path('tests'),'tgts1000.adj-adj.adj-nounaff.k250.pkl')

name     = 'tgts1000.adj-adj.adj-nounaff.k250'
out_dir  = get_path('results')
out_path = os.path.join(out_dir, name + '.txt')

cr = ClusReader(test)

############################################################

test_1 = cr.clus2words(cr.soft_clustering(thr=0.002))

ranked = dict()
cnt    = 1

for _,gold in test_1.iteritems():
	gold = [[w] for w in gold]
	ranked[cnt] = ilp_each(probs,gold)
	cnt += 1

with open(out_path, 'wb') as h:
	h.write(name + '\n')
	h.write('='*50 + '\n')
	for _,d in ranked.iteritems():
		for [w] in d['algo']:
			h.write(w + ' <\n')
		h.write('\n')			
	h.write('=== DONE')		

