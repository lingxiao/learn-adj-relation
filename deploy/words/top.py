############################################################
# Module  : making train, validation, and all data
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os

import shutil
from scripts import *
from utils   import *
from app     import *

############################################################
'''
	paths
'''	

dirs = working_dirs('words',[p + '-' + s    \
	    for p in ['train', 'valid', 'all']  \
	    for s in ['pairs', 'words'] ])

############################################################

'''
	@Use: split training edges into chunks 
'''
def train_pairs(size, output_dir, refresh = False):
	'''
		open graph
	'''
	print ('\n>> running split pairs for training words')

	gr_path = get_path('graph')
	G       = Graph(gr_path)
	train   = G.train()

	words = train['base'] + train['compare'] + train['superla']

	print('\n>> found ' + str(len(words)) + ' training words')

	return split_and_save(words, size, output_dir, refresh)

'''
	@Use: split edges into chunks to compute
	      weight on remote 
'''
def all_pairs(size, output_dir, refresh = False):

	print ('\n>> running split pairs for all words')

	gr_path    = get_path('graph')
	ccb        = read_gold(get_path('ccb'))
	bansal     = read_gold(get_path('bansal'))
	'''
		get all words
	'''
	bansal_words = join(join(ws) for _,ws in bansal.iteritems())
	ccb_words    = join(join(ws) for _,ws in bansal.iteritems())

	_, words = load_as_list(gr_path)

	'''
		construct word pairs
	'''
	words    = words + bansal_words + ccb_words

	return split_and_save(words, size, output_dir, refresh)

'''
	@use: split into pairs for test words only
			- mohit words
			- ccb words
'''
def test_pairs(size, output_dir, refresh = False):

	print ('\n>> running split pairs for validation words')

	ccb     = read_gold(get_path('ccb'))
	bansal  = read_gold(get_path('bansal'))
	'''
		get all words
	'''
	bansal_words = join(join(ws) for _,ws in bansal.iteritems())
	ccb_words    = join(join(ws) for _,ws in bansal.iteritems())

	'''
		construct word pairs
	'''
	words = bansal_words + ccb_words

	return split_and_save(words, size, output_dir, refresh)

'''
	@Use: split vertices into chunks to compute
	      weight on remote 
'''
def all_words(size, output_dir, refresh = False):

	print ('\n>> running split words for all words')

	if refresh:
		print('\n\t>> adding onto existing batch')
	else:
		print('\n\t>> deleting existing batch')
		shutil.rmtree(output_dir)
		os.mkdir(output_dir)


	ccb        = read_gold(get_path('ccb'))
	bansal     = read_gold(get_path('bansal'))
	_, words   = load_as_list(get_path('graph'))

	'''
		get all words
	'''
	bansal_words = join(join(ws) for _,ws in bansal.iteritems())
	ccb_words    = join(join(ws) for _,ws in bansal.iteritems())
	words        = words + bansal_words + ccb_words

	'''
		split
	'''
	splits = list(chunks(words,size))

	'''
		prepend debug pairs file to make batch-0.txt
	'''
	splits = [['good', 'great', 'excellent']] + splits

	print('\n\t>> splitting words into ' + str(len(splits)) + ' chunks of ' + str(len(splits[1])) + ' pairs each')

	cnt = 0
	
	for ws in splits:

		path = os.path.join(output_dir, 'batch-' + str(cnt) + '.txt')

		with open(path,'wb') as h:
			for s in ws:
				h.write(s + '\n')
		cnt += 1

	return cnt


'''
	@Use: given words and chunk size, 
		  split and save to output directory
'''
def split_and_save(words, size, output_dir, refresh = False):

	print('\n>> splitting words and saving ...')

	if refresh:
		print('\n\t>> adding onto existing batch')
	else:
		print('\n\t>> deleting existing batch')
		shutil.rmtree(output_dir)
		os.mkdir(output_dir)

	pwords   = unique_pairs_with_self_pair(words)
	splits   = list(chunks(pwords,size))

	'''
		prepend debug pairs file to make batch-0.txt
	'''
	splits = [[ ('good','great')
	           ,('great','excellent')
	           ,('good','bad')
	           ,('bad' ,'worse')
	           ,('bad' ,'terrible')
	           ,('tasty','yummy')]]  \
 	       + splits

	cnt = 0

	print('\n\t>> splitting words pairs into ' + str(len(splits)) + ' chunks of ' + str(len(splits[1])) + ' pairs each')
	
	for ws in splits:

		path = os.path.join(output_dir, 'batch-' + str(cnt) + '.txt')

		with open(path,'wb') as h:
			for s,t in ws:
				h.write(s + ', ' + t + '\n')

		cnt += 1

	return cnt


'''
	construct unique pairs of words 
'''
def unique_pairs_with_self_pair(words):
	tup   = lambda xs : (xs[0], xs[1])
	pairs = set(tup(sorted([u,v])) for u in words for v in words)
	return list(pairs)

'''
	filter out the words that we know have no data
'''


############################################################
'''
	run
'''
train_pairs(1000  , dirs['train-pairs'])
test_pairs (1000  , dirs['valid-pairs'])
all_pairs  (100000, dirs['all-pairs'])
all_words  (500, dirs['all-words'])






