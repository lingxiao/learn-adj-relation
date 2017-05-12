############################################################
# Module  : make test set where ties are broken out into own clusters
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os
import pickle
import numpy as np

from app     import *
from utils   import *
from scripts import *
from scripts.graph import *
from experiments.argmax import *
from experiments.rank_all import *
from experiments.elastic_net import *

############################################################
'''
	load test sets
'''
print('\n\t>> load base-comparative-superlative')
bcs = join(_xs for _, _xs in train_vertices(get_path('bcs')).iteritems())
bcs = [[[w] for w in _ws] for _ws in bcs]

print('\n\t>> load turk')
ccb = read_gold( get_path('ccb') )

print('\n\t>> load moh')
moh = read_gold( get_path('moh') )

############################################################
'''
	@Use: determine if clusters has ties
	      if so break into cluster with no ties
'''
def remove_ties(clusters):

	def fn(cluster, out):

		if not cluster:
			return out

		else:
			head = cluster[0]
			tail = cluster[1:]

			if len(head) == 1:
				if not out: 
					return fn( tail, [head] )
				else: 
					out1 = [c + head for c in out]
					return fn( tail, out1 )

			else:
				if not out: 
					return fn (tail, [[h] for h in head] )
				else:
					out_    = out*len(head)
					rep_len = max(1, len(out_) - len(head))
					out1    = [x + [y] for x,y in zip(out_, head * rep_len)]
					return fn( tail, out1 )

	out = fn(clusters,[])
	ret = []

	for o in out:
		ret.append([[x] for x in o])

	return ret


def make_no_ties(gold_in, out_path):

	no_ties = []

	for cluster in gold_in:
		no_ties += remove_ties(cluster)

	gold = {k:w for k,w in enumerate(no_ties)}

	write_gold(out_path, gold)

	return gold


ccbn = make_no_ties( ccb
	               , os.path.join(get_path('data-root'), 'ccb-no-tie.txt')
	               )

mohn = make_no_ties( moh, os.path.join(get_path('data-root')
	               , 'moh-no-tie.txt')
				   )










