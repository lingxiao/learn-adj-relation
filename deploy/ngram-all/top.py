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
dirs       = working_dirs('ngram-all',['scripts','shells'])

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
def split_into_pairs(size, output_dir):

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
	pwords   = to_unique_pairs(words)
	splits   = list(chunks(pwords,size))

	'''
		prepend debug pair file
	'''
	splits = [[('good','great'),('great','excellent'),('good','bad')]]  \
 	       + splits

	cnt = 0

	print('\n>> splitting words pairs into ' + str(len(splits)) + ' chunks')
	
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
def to_unique_pairs(words):
	tup   = lambda xs : (xs[0], xs[1])
	pairs = set(tup(sorted([u,v])) for u in words for v in words if u != v)
	return list(pairs)
				
############################################################
'''
	@Use: rewrite main-#.py file
'''
def run_auto_main(tot, work_dir, script_dir):

	print('\n>> running run_auto_main for total: ' + str(tot) + ' for job ' + current_job)
	print('\n>> removing existing scripts...')

	shutil.rmtree(script_dir)
	os.mkdir(script_dir)

	cnt = 0

	for k in xrange(tot-1):
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

	for k in xrange(tot-1):
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
current_job = 'all-pairs'

num_jobs    = len([p for p in os.listdir(word_dirs[current_job]) if '.txt' in p])

run_auto_main( num_jobs
	 		 , work_dir
	 		 , script_dir)

run_auto_sh  ( num_jobs
	         , work_dir
	         , shell_dir )




