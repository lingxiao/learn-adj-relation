############################################################
# Module  : compute edge weight where 
# 
#           			   | s -> t | 
# w(s -> t) =          -------------------
#                      	 sum_x  | s -> x|
# 
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import shutil
from utils   import *
from scripts import *
from app     import *
from deploy import *

############################################################
'''
	paths
'''
work_dirs = working_dirs('out-degree',['scripts','shells'])

asset_dirs = working_dirs( 'words'
	                    , [p + '-' + s for p in ['train', 'valid', 'all'] \
	                      for s in ['pairs', 'words'] ])


work_dir   = work_dirs['work']
script_dir = work_dirs['scripts']
shell_dir  = work_dirs['shells']

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

	for k in xrange(tot):
		src_path = os.path.join(work_dir, 'out-degree-0.py')
		tgt_path = os.path.join(script_dir, 'out-degree-' + str(cnt) + '.py')
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
		src_path = os.path.join(work_dir,'out-degree-0.sh')
		tgt_path = os.path.join(shell_dir,'out-degree-' + str(cnt) + '.sh')
		src_strs = ['out-degree-0']
		tgt_strs = ['out-degree-' + str(cnt)]

		auto_gen(src_path, tgt_path, src_strs, tgt_strs)

		cnt +=1


############################################################
'''
	run all
'''
current_job = 'all-words'

num_jobs    = len([p for p in os.listdir(asset_dirs[current_job]) if '.txt' in p])

run_auto_main( num_jobs
	 		 , work_dir
	 		 , script_dir)

run_auto_sh  ( num_jobs
	         , work_dir
	         , shell_dir )




