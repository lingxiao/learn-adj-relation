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


############################################################

one_gram_path = get_path('1-gram')
out_path      = get_path('word-count')

words = { w : 0.0 for w in G_ppng.vertices }

with open(one_gram_path, 'rb') as h:
	for line in h:
		xsn = line.split('\t')
		if len(xsn) == 2:
			word,n = xsn
			n = int(n.replace('\n',''))
			if word in words:
				print('\n\t>> found word ' + word)
				words[word] += n
				
words = { w : max(n,1.0) for w,n in words.iteritems() }

print( '\n\t>> saving to ' + out_path )
with open(out_path,'wb') as h:
	pickle.dump(words,h)





