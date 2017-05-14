############################################################
# Module  : Serves raw data
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os
import pickle
import numpy as np
from random import shuffle

from app     import *
from utils   import *
from scripts import *

############################################################
'''
	labels
'''
LABEL = { '<': 1.0
        , '>': 0.0
        , '=': -1.0
        }

############################################################
'''
	@Use: read data from pairs with no data
		  for file format, see:
		  	experiments/baseline/construct_pairs.py
'''
def no_data_pairs(in_path):

	with open(in_path,'rb') as h:
		no_data = pickle.load(h)

	out = []

	for _,ds in no_data.iteritems():
		for s,t in ds:
			out.append((s,t, LABEL['<']))
			out.append((t,s, LABEL['>']))

	for _ in range(10):
		shuffle(out)

	xs = [(s,t) for s,t,_ in out]
	ys = [y for _,_,y in out]

	return xs, ys, to_gold(out)


def to_gold(xys):

	gold = []

	for s,t,y in xys:
		if y:
			gold.append([[s],[t]])
		else:
			gold.append([[t],[s]])
	return gold

############################################################
'''
	construct training pairs

'''
def train_pairs(gold_set):

	pairs_le_than = []

	for gold in gold_set:
		pairs_le_than += to_pairs(gold)

	pairs_ge_than = [(t,s,LABEL['>']) for s,t,_ in pairs_le_than]

	pairs = pairs_ge_than + pairs_le_than

	for _ in xrange(10):
		shuffle(pairs)

	xs = [(s,t) for s,t,_ in pairs]
	ys = [y for _,_,y in pairs]

	return xs, ys

'''
	@Use: given test set of form: [test1, test2, ...]
		  where test_i = [[w1],[w2],[w3,w4],...]
		  so that w < w2 < (w3 = w4) < ...
		  turn into a list of pairs so that the first
		  word in the pair is weaker than second, ie:
		  [(w1,w2),(w1,w3),(w2,w3),(w2,w4),...]

	@Input : golds :: [[String]]	

	@output: pairs :: [(String,String)]
'''
def to_pairs(golds):
	return go(golds,[])

def go(golds, pairs):
	if golds == []:
		return pairs
	else:
		head = golds[0]
		tail = golds[1:]

		pairs1 = join([(s,t,LABEL['<']) for s in head for t in elem] \
			     for elem in tail)

		return go(tail, pairs + pairs1)		

############################################################
'''
	construct test pairs

'''
def test_pairs(gold_set):

	pairs = []

	for gold in gold_set:
		pairs += to_pairs_with_ties(gold)

	for _ in xrange(10):
		shuffle(pairs)

	xs = [(s,t) for s,t,_ in pairs]
	ys = [y for _,_,y in pairs]

	return xs, ys

'''	
	@Use: given test set of form: [test1, test2, ...]
		  where test_i = [[w1],[w2],[w3,w4],...]
		  so that w < w2 < (w3 = w4) < ...
		  turn into a list of pairs so that the first
		  word in the pair is weaker than second, ie:
		  [(w1,w2, LABEL['<']),(w1,w3,LABEL['<']),...]
		  and ties are include as:
		  [(w2,we,tied),...]

	@Input : golds :: [[String]]	

	@output: pairs :: [(String,String,Float)]
'''
def to_pairs_with_ties(golds):
	return go_tie(golds,[])

def go_tie(golds, pairs):
	if golds == []:
		return pairs
	else:
		head = golds[0]
		tail = golds[1:]

		pairs1 = join([(h,t,LABEL['<']) for h in head for t in elem] \
			     for elem in tail)

		if len(head) > 1:
			ties = list(set( sort_tup((a,b)) for a in head \
			                                 for b in head \
			                                 if a != b ))
			ties = [(a,b,LABEL['=']) for a,b in ties]
		else:
			ties = []

		return go_tie(tail, pairs + ties + pairs1)		

# sort_tup :: (String,String) -> (String,String)
def sort_tup(t):
	x,y = t
	xs = [x,y]
	xs.sort()
	a,b = xs
	return (a,b)
