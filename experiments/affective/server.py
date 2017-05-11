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


