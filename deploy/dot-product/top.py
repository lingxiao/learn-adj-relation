############################################################
# Module  : get google ngram lines that contain words in graph
#           split edges and make dot-#.py
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

dirs = working_dirs('dot-product',['scripts','shells'])

word_dirs = working_dirs( 'words'
	                    , [p + '-' + s for p in ['train', 'valid', 'all'] \
	                                   for s in ['pairs', 'words'] ])

work_dir   = dirs['work']
script_dir = dirs['scripts']
shell_dir  = dirs['shells']

############################################################
'''
	@Use: rewrite dot-#.py file
'''
def run_auto_main(tot, work_dir, script_dir, current_job):

	print('\n>> running run_auto_main for total: ' + str(tot) + ' for job ' + current_job)
	print('\n>> removing existing scripts...')

	shutil.rmtree(script_dir)
	os.mkdir(script_dir)

	cnt = 0

	for k in xrange(tot-1):
		src_path = os.path.join(work_dir, 'dot-0.py')
		tgt_path = os.path.join(script_dir, 'dot-' + str(cnt) + '.py')
		src_strs = ['batch = 0', 'current_job    = None']
		tgt_strs = ['batch = ' + str(cnt), "current_job    = '" + current_job + "'"]
		auto_gen(src_path, tgt_path, src_strs, tgt_strs)
		cnt += 1

'''
	@Use: rewrite dot-#.sh file
'''
def run_auto_sh(tot, work_dir, shell_dir):

	print('\n>> running run_auto_sh for total: ' + str(tot))
	print('\n>> removing existing scripts...')

	shutil.rmtree(shell_dir)
	os.mkdir(shell_dir)

	cnt = 0

	for k in xrange(tot-1):
		src_path = os.path.join(work_dir,'dot-0.sh')
		tgt_path = os.path.join(shell_dir,'dot-' + str(cnt) + '.sh')
		src_strs = ['dot-0']
		tgt_strs = ['dot-' + str(cnt)]

		auto_gen(src_path, tgt_path, src_strs, tgt_strs)

		cnt +=1

############################################################
'''
	run all
'''
current_job = 'all-pairs'

num_jobs    = len([p for p in os.listdir(word_dirs[current_job]) if '.txt' in p])

run_auto_main( num_jobs
	         , dirs['work']
	         , dirs['scripts']
	         , current_job
	         )

run_auto_sh  ( num_jobs
	         , dirs['work']
	         , dirs['shells']
	         )





