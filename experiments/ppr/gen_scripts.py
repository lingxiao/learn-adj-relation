############################################################
# Module  : Run this script to generate all test and shell 
# 			files
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import shutil
import pickle
import operator
import itertools
from collections import Counter

from app     import *
from utils   import *
from scripts import *
from scripts.graph import *
from experiments import *

from experiments.ppr.top import graph_names, edge, topo, alphas, result_dir


############################################################
'''
	make deploy scripts

	@Use: rewrite main-#.py file
'''
def run_auto_main(tot, root):

	print('\n>> run_auto_main: removing existing scripts...')

	script_dir = os.path.join(root, 'scripts')

	if os.path.exists(script_dir):
		shutil.rmtree(script_dir)
	os.mkdir(script_dir)

	cnt = 0

	for k in xrange(tot):
		src_path = os.path.join(root, 'exec-ppr-0.py')
		tgt_path = os.path.join(script_dir, 'exec-ppr-' + str(cnt) + '.py')
		src_strs = ['batch = 0']
		tgt_strs = ['batch = ' + str(cnt)]
		auto_gen(src_path, tgt_path, src_strs, tgt_strs)
		cnt += 1

'''
	@Use: rewrite main-#.sh file
'''
def run_auto_sh(tot, root):

	print('\n>> run_auto_sh: removing existing shell scripts...')

	shell_dir = os.path.join(root, 'shells')

	if os.path.exists(shell_dir):
		shutil.rmtree(shell_dir)
	os.mkdir(shell_dir)

	cnt = 0

	for k in xrange(tot):
		src_path = os.path.join(root,'exec-ppr-0.sh')
		tgt_path = os.path.join(shell_dir,'exec-ppr-' + str(cnt) + '.sh')
		src_strs = ['exec-ppr-0']
		tgt_strs = ['exec-ppr-' + str(cnt)]

		auto_gen(src_path, tgt_path, src_strs, tgt_strs)

		cnt +=1

############################################################
'''
	generate all scripts and make all paths and directories
'''
num_jobs = len(graph_names)

run_auto_main( num_jobs
	 		 , get_path('ppr')
	 		 )

run_auto_sh  ( num_jobs
	         , get_path('ppr')
	         )

