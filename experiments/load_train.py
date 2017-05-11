############################################################
# Module  : compute results by expected value
# 			as a baseline
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import app
from utils   import *
from scripts import *

############################################################
'''
	load all train, validation, and test data
'''
def load_train(G):

	V = G.vertices

	'''
		Do direct order by expected value for pairs
		problem: right now you don't have a 
		list of good base comparative and superlative pairs
	'''
	train_data = G.train_data()

	bcs = train_data['base-compare'] \
		+ train_data['compare-super'] \
		+ train_data['base-super']    \
		+ train_data['triples']

	bcs = [[[s] for s in data] for data in bcs]
	ccb = read_gold(app.get_path('ccb'))
	moh = read_gold(app.get_path('bansal'))

	moh_small = []

	'''
		construct subset of moh graph 
		where data exists
	'''	
	for gold in moh:
		ws = join(gold)
		if all( s in V for s in ws ):
			moh_small.append(gold)

	return {'bcs': bcs, 'ccb': ccb, 'moh': moh, 'moh-small': moh_small}



























