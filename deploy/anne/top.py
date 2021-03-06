############################################################
# Module  : get google anne lines that contain words in graph
#           split edges and make main-#.py
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import pickle
import shutil
from utils   import *
from scripts import *
from app     import *
from experiments import *

############################################################
'''
	paths
'''
dirs  = working_dirs('anne',['scripts','shells', 'results-ppdb-1', 'results-ppdb-ngram-1'])
anne  = get_path('anne')
files = [p for p in os.listdir(anne) if '.txt' in p]
			
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
		src_path = os.path.join(work_dir, 'anne-0.py')
		tgt_path = os.path.join(script_dir, 'anne-' + str(cnt) + '.py')
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

	cnt = 0

	for k in xrange(tot):
		src_path = os.path.join(work_dir,'anne-0.sh')
		tgt_path = os.path.join(shell_dir,'anne-' + str(cnt) + '.sh')
		src_strs = ['anne-0']
		tgt_strs = ['anne-' + str(cnt)]

		auto_gen(src_path, tgt_path, src_strs, tgt_strs)

		cnt +=1

############################################################
'''
	generate py and shell scripts
'''
if False:
	num_jobs = len(files)

	print('\n\t>> found ' + str(num_jobs) + ' jobs') 
	run_auto_main( num_jobs 
		 		 , dirs['root']
		 		 , dirs['scripts'])

	run_auto_sh  ( num_jobs 
		 		 , dirs['root']
		         , dirs['shells'])


############################################################
'''
	combine results into one file
'''
if True:
	data_sets   = ['ppdb-1', 'ppdb-ngram-1']

	for data_set in data_sets:
		print('\n\t>> saving results algo only for ' + data_set)
		results_dir = dirs['results-' + data_set ]
		results     = read_results(results_dir)	
		out_path    = os.path.join(dirs['root'], 'anne-all-' + data_set + '.txt')
		save_results(results, out_path, algo_only = True)





