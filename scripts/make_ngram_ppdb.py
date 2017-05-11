############################################################
# Module  : construct ppdb+ngram graph
# Date    : April 17th.
# Author  : Xiao Ling
############################################################

import os
import shutil
from app import *
from scripts import *
from utils   import *
import json

############################################################
'''
	@Use: given `in_dir` to open files of form "../s-t.txt"
	      construct edges between s and t and append-save
	      to out_path
'''
def add_ngram_edges(ngram_root               = ''
	              , ngram_out_path           = ''
				  , ngram_bool_out_path	     = ''               
	              , ngram_ppdb_out_path      = ''
	              , ngram_ppdb_bool_out_path = ''):

	'''
		load ppdb graph
	'''
	E,_ = load_as_list(get_path('ppdb-txt'))

	'''
		load all ngram patterns
	'''
	paths = [os.path.join(ngram_root, p) for p in os.listdir(ngram_root) \
		     if '.txt'in p]
	
	if True:		

		out_paths = [ngram_out_path,ngram_bool_out_path,ngram_ppdb_out_path,ngram_ppdb_bool_out_path]     

		print('\n>> removing existing graphs if it exists ...')
		for path in out_paths:
			if os.path.exists(path):
				os.remove(path)

	print('\n>> constructing ngram graph')		
	if True:
		print('\n\t>> adding ' + str(len(paths)) + ' ngram edges')
		[add_ngram_edge(p, ngram_out_path) for p in paths]


	print('\n>> constructing ngram boolean graph')		
	if True:
		print('\n\t>> adding ' + str(len(paths)) + ' boolean ngram edges')
		[add_ngram_boolean_edge(p, ngram_bool_out_path) for p in paths]


	print('\n>> constructing ngram-ppdb graph')		
	if True:
		
		print('\n\t>> adding ppdb edges ...')
		with open(ngram_ppdb_out_path,'a') as h:
			for line in E:
				xs = ', '.join(line)
				h.write(xs + '\n')

		print('\n\t>> adding ' + str(len(paths)) + ' ngram edges')
		[add_ngram_edge(p, ngram_ppdb_out_path) for p in paths]


	print('\n>> constructing ngram-ppdb boolean graph')

	if True:
		print('\n\t>> adding ppdb edges ...')
		with open(ngram_ppdb_bool_out_path,'a') as h:
			for line in E:
				xs = ', '.join(line)
				h.write(xs + '\n')

		print('\n\t>> adding ' + str(len(paths)) + ' boolean ngram edges')
		[add_ngram_boolean_edge(p, ngram_ppdb_bool_out_path) for p in paths]



############################################################

'''
	@Use: given `in_path` to open files of form "../s-t.txt"
	      construct edges between s and t and append-save
	      to out_path
'''
def add_ngram_edge(in_path,out_path):

	s,t = in_path.split('/')[-1].split('-')
	t   = t.replace('.txt','')

	datas = open(in_path,'rb').read().split('\n')

	s_ge_t = []
	s_le_t = []

	for idx,line in enumerate(datas):
		if s + ' < ' + t in line:
			s_ge_t = datas[0:idx]
			s_le_t = datas[idx:]

	s_ge_t = [x for x in s_ge_t if s + ' > ' + t not in x and x]
	s_le_t = [x for x in s_le_t if s + ' < ' + t not in x and 'END' not in x]

	s_ge_t = [split(x) for x in s_ge_t]
	s_le_t = [split(x) for x in s_le_t]

	s_ge_t_edge = [(t,s,'<is weaker than>')]*sum(n for _,n in s_ge_t)
	s_le_t_edge = [(s,t,'<is weaker than>')]*sum(n for _,n in s_le_t)


	with open(out_path,'a') as h:
		for line in s_ge_t_edge:
			xs = ', '.join(line)
			h.write(xs + '\n')
		for line in s_le_t_edge:
			xs = ', '.join(line)
			h.write(xs + '\n')


'''
	@Use: given `in_path` to open files of form "../s-t.txt"
	      construct edges between s and t and append-save
	      to out_path
'''
def add_ngram_boolean_edge(in_path,out_path):

	'''
		get words
	'''
	s,t = in_path.split('/')[-1].split('-')
	t   = t.replace('.txt','')


	'''
		reopen compile patterns to match against ngram edges
	'''
	patterns     = read_pattern(get_path('patterns'))
	patts        = compile_patterns(s,t,patterns)
	all_patterns = patts[s+'>'+t] + patts[s+'<'+t]

	datas = open(in_path,'rb').read().split('\n')

	s_ge_t = []
	s_le_t = []

	for idx,line in enumerate(datas):
		if s + ' < ' + t in line:
			s_ge_t = datas[0:idx]
			s_le_t = datas[idx:]

	s_ge_t = [x for x in s_ge_t if s + ' > ' + t not in x and x]
	s_le_t = [x for x in s_le_t if s + ' < ' + t not in x and 'END' not in x]

	s_ge_t = [split(x) for x in s_ge_t]
	s_le_t = [split(x) for x in s_le_t]

	# s_ge_t_boolean_edge = [(t,s,'<is weaker than>') for _ in s_ge_t]
	# s_le_t_boolean_edge = [(s,t,'<is weaker than>') for _ in s_le_t]

	s_ge_t_bool = [(t,s,'<'+p+'>') for p in to_boolean_edge(all_patterns, s_ge_t)]
	s_le_t_bool = [(s,t,'<'+p+'>') for p in to_boolean_edge(all_patterns, s_le_t)]

	with open(out_path,'a') as h:
		for line in s_ge_t_bool:
			xs = ', '.join(line)
			h.write(xs + '\n')
		for line in s_le_t_bool:
			xs = ', '.join(line)
			h.write(xs + '\n')

'''
	@Use: given list of ngram patterns with associated words
		  output the patterns that it matches
'''
def to_boolean_edge(patterns, edges):

	all_matched = []

	for gram,_ in edges:
		matched_patterns = [p for p,r in patterns if r.match(gram)]
		all_matched += matched_patterns

	return set(all_matched)


def split(xs):
	x,n = xs.split('\t')
	return (x,int(n))

############################################################

'''
	@Use: shard graph so it can be easily commited
'''
def shard_graph(out_path, out_dir, remove_big):

	print('\n>> shard graph so it can be git commited')

	if os.path.exists(out_dir):
		shutil.rmtree(out_dir)
		os.makedirs(out_dir)
	else:
		os.makedirs(out_dir)

	print('\n>> open graph and shard')

	E = []

	with open(out_path,'rb') as h:
		for line in h:
			E.append(line)

	Es = chunks(E, len(E)/4)			

	cnt = 1

	for edges in Es:
		path = os.path.join(out_dir, 'shard-' + str(cnt) + '.txt')
		print('\n>> saving shard '+ str(cnt))

		with open(path, 'wb') as h:
			for e in edges:
				h.write(e)

		cnt +=1 

	if remove_big:		
		print('\n>> removing original file ...')
		os.remove(out_path)

############################################################
'''
	run function to construct graph
'''
ngram_root = os.path.join(get_path('deploy-data'), 'ngram-all/outputs')

ngram_path           = os.path.join(get_path('data-root')  , 'inputs/raw-graph/ngram.txt')
ngram_bool_path      = os.path.join(get_path('data-root')  , 'inputs/raw-graph/ngram-bool.txt')
ngram_ppdb_path      = os.path.join(get_path('data-root')  , 'inputs/raw-graph/ppdb-ngram.txt')
ngram_ppdb_bool_path = os.path.join(get_path('data-root')  , 'inputs/raw-graph/ppdb-ngram-bool.txt')

ngram_dir            = get_path('ngram-txt')
ngram_bool_dir       = get_path('ngram-bool-txt')
ngram_ppdb_dir       = get_path('ppdb-ngram-txt')
ngram_ppdb_bool_dir  = get_path('ppdb-ngram-bool-txt')


print('\n>> construct ppdb-ngram graph')
add_ngram_edges(  ngram_root                = ngram_root
				, ngram_out_path            = ngram_path
				, ngram_bool_out_path	    = ngram_bool_path              
				, ngram_ppdb_out_path       = ngram_ppdb_path
				, ngram_ppdb_bool_out_path  = ngram_ppdb_bool_path )


print('\n>> Sharding ngram graph...')
shard_graph(ngram_path, ngram_dir, True)

print('\n>> Sharding ngram boolean graph...')
shard_graph(ngram_bool_path, ngram_bool_dir, True)

print('\n>> Sharding ngram boolean graph...')
shard_graph(ngram_ppdb_path, ngram_ppdb_dir, True)


print('\n>> Sharding ngram boolean graph...')
shard_graph(ngram_ppdb_bool_path, ngram_ppdb_bool_dir, True)



# print('\n>> assert can open as nx.graph')
# G = Graph(get_path('ppdb-ngram'))














