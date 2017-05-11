############################################################
# Module  : get google ngram lines that contain words in graph
#           split edges and make main-#.py
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import shutil
import pickle
from scripts import *
from utils   import *
from app     import *


############################################################
'''
	paths
'''

raw_dir     = get_path('2-gram-raw')
graph_path  = get_path('ppdb')
out_path    = get_path('bigram-freq')

def to_bigram(edge):
	s,_,v = edge
	adv = v[1:-1]
	bigm = adv + ' ' + s
	return bigm

############################################################
'''
	run routine
'''
print('\n>> ping out_path to make sure it exists')
with open(out_path,'wb') as h:
	pickle.dump(dict(),h)
 
print('\n>> get ppdb G = (E,V)')
E,V = load_as_list(graph_path)

print('\n>> constructing bigrams and ensure all bigrams appear at least once')				
bigrams = { to_bigram(e) : 1 for e in E }

print('\n>> counting bi-grams')
for ngm,n in with_zip_ngram(raw_dir, debug=False):
	if ngm in bigrams: 
		bigrams[ngm] += n

print('\n>> saving at path: ' + out_path)
with open(out_path,'wb') as h:
	pickle.dump(bigrams, h)

