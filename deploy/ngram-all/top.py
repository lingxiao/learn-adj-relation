############################################################
# Module  : get google ngram lines that contain words in graph
#           split edges and make main-#.py
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import shutil
from utils   import *
from scripts import *
from app     import *

############################################################
'''
	paths
'''
dirs = working_dirs('ngram-all',['scripts','shells','pairs'])

word_dirs = working_dirs( 'words'
	                    , [p + '-' + s for p in ['train', 'valid', 'all'] \
	                                   for s in ['pairs', 'words'] ])

work_dir   = dirs['work']
script_dir = dirs['scripts']
shell_dir  = dirs['shells']

############################################################
'''
	@Use: split edges into chunks to compute
	      weight on remote 
'''
def split_into_pairs(size, gr_path, output_dir, save = False):

	print('\n>> opening all test sets ...')
	ccb        = read_gold(get_path('ccb'))
	bansal     = read_gold(get_path('moh'))
	anne_sm    = read_gold(get_path('anne-25' ))
	anne_lg    = read_gold(get_path('anne-125'))
	bcs        = join(_xs for _, _xs in train_vertices(get_path('bcs')).iteritems())
	bcs        = [[[w] for w in _ws] for _ws in bcs]	


	'''
		get all words
	'''
	print('\n>> combining all test sets ...')
	test_words = join(join(ccb + bansal + anne_sm + anne_lg + bcs))
	new_words  = join(join(anne_sm + anne_lg))

	_, words   = load_as_dict(gr_path)

	'''
		construct word pairs
	'''
	words    = set(words + test_words)
	pwords   = to_unique_pairs(words)

	'''
		filter out pairs with new words only
	'''
	print('\n>> pruning whole graph for unique pairs ...')
	pwords = [ (s,t) for s,t in pwords if s in new_words or t in new_words ]
	print('\n>> found ' + str(len(pwords)) + ' new unique pairs')


	print('\n>> dividing pairs into ' + str( float(len(pwords)/size) ) + ' chunks ...')
	splits   = list(chunks(pwords,size))


	'''
		prepend debug pair file
	'''
	splits = [[('good','great'),('great','excellent'),('good','bad')]]  \
 	       + splits

	cnt = 0

	print('\n>> splitting words pairs into ' + str(len(splits)) + ' chunks')

	if save:
		
		for ws in splits:

			path = os.path.join(output_dir, 'batch-' + str(cnt) + '.txt')

			print('\n\t>> saving to ' + path)

			with open(path,'wb') as h:
				for s,t in ws:
					h.write(s + ', ' + t + '\n')

			cnt += 1

	return cnt

'''
	construct unique pairs of words 
'''
def to_unique_pairs(words):
	tup   = lambda xs : (xs[0], xs[1])
	pairs = set(tup(sorted([u,v])) for u in words for v in words if u != v)
	return list(pairs)
				
############################################################
'''
	@Use: rewrite main-#.py file
'''
def run_auto_main(tot, work_dir, script_dir):

	print('\n>> running run_auto_main for total: ' + str(tot) )
	print('\n>> removing existing scripts...')

	shutil.rmtree(script_dir)
	os.mkdir(script_dir)

	cnt = 0

	for k in xrange(tot):
		src_path = os.path.join(work_dir, 'ngram-0.py')
		tgt_path = os.path.join(script_dir, 'ngram-' + str(cnt) + '.py')
		src_strs = ['batch = 0']
		tgt_strs = ['batch = ' + str(cnt)]
		auto_gen(src_path, tgt_path, src_strs, tgt_strs)
		cnt += 1

'''
	@Use: rewrite main-#.sh file
'''
def run_auto_sh(tot, work_dir, shell_dir):

	print('\n>> running run_auto_sh for total: ' + str(tot))
	print('\n>> removing existing scripts...')

	shutil.rmtree(shell_dir)
	os.mkdir(shell_dir)

	'''
		if too many scripts, break into chunks
	'''
	# batches = chunks(xrange(tot),30)

	cnt = 0

	for k in xrange(tot):
		src_path = os.path.join(work_dir,'ngram-0.sh')
		tgt_path = os.path.join(shell_dir,'ngram-' + str(cnt) + '.sh')
		src_strs = ['ngram-0']
		tgt_strs = ['ngram-' + str(cnt)]

		auto_gen(src_path, tgt_path, src_strs, tgt_strs)

		cnt +=1

############################################################
'''
	run all
'''

# run this to make pairs
if True:
	num_jobs = split_into_pairs( 100000
		                       , get_path('ppdb')
		                       , word_dirs['all-pairs']
		                       , save = False)

	print('\n\t>> constructed ' + str(num_jobs) + ' jobs')

# run this after the pairs have been made
if False:
	num_jobs = len([p for p in os.listdir(word_dirs['all-pairs']) if '.txt' in p])

	print('\n\t>> found ' + str(num_jobs) + ' jobs') 
	run_auto_main( num_jobs 
		 		 , work_dir
		 		 , script_dir)

	run_auto_sh  ( num_jobs 
		         , work_dir
		         , shell_dir )




