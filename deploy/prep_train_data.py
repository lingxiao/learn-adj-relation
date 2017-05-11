############################################################
# Module  : construct all pairs and triples
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import shutil
from utils   import *
from scripts import *
from app     import *
import itertools

############################################################
'''
	paths and directories
'''
out_dir  = data_dirs('training', [])
out_dir  = out_dir['data']


def construct_pairs(out_dir):

	writer = Writer(get_path('log'),1)

	bc_path  = os.path.join(out_dir, 'base-comparative.txt')
	cs_path  = os.path.join(out_dir, 'comparative-superlative.txt')
	bs_path  = os.path.join(out_dir, 'base-superlative.txt')

	writer.tell('removing existing files if any')
	for p in [bc_path, cs_path, bs_path]:
		if os.path.exists(p):
			os.remove(p)


	edges,vertices = load_as_list(get_path('graph'))

	writer.tell('constructing base comparative pairs')
	base_compare_pairs = set( (s,t) for s in vertices for t in vertices \
	                          if base_compare(s,t) )

	writer.tell('saving base comparative pairs')
	with open(bc_path, 'a') as h:
		for s,t in base_compare_pairs:
			h.write(s + ' ' + t + '\n')



	writer.tell('constructing base superlative pairs')
	base_superla_pairs = set( (s,t) for s in vertices for t in vertices \
		                     if base_superla(s,t) )


	writer.tell('saving base superlative pairs')
	with open(bs_path, 'a') as h:
		for s,t in base_superla_pairs:
			h.write(s + ' ' + t + '\n')


	writer.tell('constructing compare superlative pairs')
	compare_superla_pairs = set( (s,t) for s in vertices for t in vertices \
		                       if compare_superla(s,t) )

	writer.tell('saving compare superlative pairs')
	with open(cs_path, 'a') as h:
		for s,t in compare_superla_pairs:
			h.write(s + ' ' + t + '\n')


	return base_compare_pairs, base_superla_pairs, compare_superla_pairs


base_compare_pairs, base_superla_pairs, compare_superla_pairs = construct_pairs(out_dir)

triples = { c : {'base': b, 'super': []} for b,c in base_compare_pairs }


for c,s in compare_superla_pairs:
	if c in triples:
		triples[c]['super'].append(s)

all_triples = []

for c,d in triples.iteritems():
	trips = [(d['base'],c,s) for s in d['super']]
	all_triples += trips

trip_path = os.path.join(out_dir, 'base-compare-super.txt')

with open(trip_path, 'wb') as h:
	for s,t,r in all_triples:
		h.write(s + ' ' + t + ' ' + r + '\n')






