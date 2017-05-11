############################################################
# Module  : convert graphs from raw list form to pickle file
# Date    : April 3rd, 2017
# Author  : Xiao Ling, merle
############################################################

import os
import shutil
import json
import pickle
import networkx as nx
from networkx.readwrite import json_graph
from collections import Counter

from utils   import *
from scripts import *
from app import *

############################################################
'''
	@Use: given path to graph, open and 
		  save as pickle file of form:
		  Edge ::
		  	word_s:
		  		word_s_1: 
		  			adv_1: count
		  			adv_2  count
		  			...
		  		word_s_2
		  		...
		  	so that we have, ie for edge set `E`
				E['good']['great']['<very'>] = 100
	@Input: - in_path  :: String
			- out_path :: String
'''
def to_dict(in_path, out_dir):

	print('\n\t>> reading raw graph from ' + in_path)

	print('\n\t>> removing existing files if any')
	if os.path.exists(out_dir):
		shutil.rmtree(out_dir)
		os.mkdir(out_dir)
	else:
		os.mkdir(out_dir)

	E,V = load_as_list(in_path)

	all_edges = {s : dict() for s in V}

	print('\n\t>> constructing graph ...')

	for src,neigh in all_edges.iteritems():
		neighbor = [(t,r) for s,t,r in E if s == src]
		neigh    = { t : dict() for t,_ in neighbor}
		for tgt in neigh:
			src_tgt_edges = [r for t,r in neighbor if t == tgt]
			src_tgt_edges = [[k,]*v for k,v in Counter(src_tgt_edges).iteritems()]
			for advs in src_tgt_edges:
				neigh[tgt][advs[0]] = len(advs)
		all_edges[src] = neigh


	print('\n\t>> sharding files')
	
	all_edges = [(k,v) for k,v in all_edges.iteritems()]
	shard_sz  = int(float(len(all_edges))/5)

	cnt = 1

	for chunk_edge in chunks(all_edges,shard_sz):

		d = {'edge': dict(chunk_edge), 'vertex': V}

		out_path = os.path.join(out_dir, 'shard-' + str(cnt) + '.pkl')

		print('\n\t>> saving shard to to ' + out_path)

		with open(out_path,'wb') as h:
			pickle.dump(d, h)

		cnt +=1 

############################################################
'''
	paths and run
'''
ppdb_txt            = get_path('ppdb-txt'           ) 
ngram_txt           = get_path('ngram-txt'          ) 
ngram_bool_txt      = get_path('ngram-bool-txt'     ) 
ppdb_ngram_txt      = get_path('ppdb-ngram-txt'     ) 
ppdb_ngram_bool_txt = get_path('ppdb-ngram-bool-txt') 

ppdb            = get_path('ppdb'           ) 
ngram           = get_path('ngram'          ) 
ngram_bool      = get_path('ngram-bool'     ) 
ppdb_ngram      = get_path('ppdb-ngram'     ) 
ppdb_ngram_bool = get_path('ppdb-ngram-bool') 


if True:

	print('\n>> converting ppdb graph')
	to_dict(ppdb_txt, ppdb)

	print('\n>> converting ngram graph')
	to_dict(ngram_txt, ngram)

	print('\n>> converting ngram-bool graph')
	to_dict(ngram_bool_txt, ngram_bool)

	print('\n>> converting ppdb-ngram graph')
	to_dict(ppdb_ngram_txt, ppdb_ngram)

	print('\n>> converting ppdb-ngram-bool graph')
	to_dict(ppdb_ngram_bool_txt, ppdb_ngram_bool)


