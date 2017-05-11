############################################################
# Module  : split edges and make ppr-#.py
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import json
import shutil
from utils   import *
from scripts import *
from app     import *

############################################################
'''
	paths
'''	
asset_dirs = working_dirs( 'words'
	                    , [p + '-' + s for p in ['train', 'valid', 'all'] \
	                      for s in ['pairs', 'words'] ])

work       = working_dirs('ppr',['scripts','shell'])

work_dir   = work['work']
script_dir = work['scripts']
shell_dir  = work['shell']


'''
	construct output directory
'''
alphas = [0.9,0.8,0.7,0.5,0.25,0.1,0.01]


############################################################
'''
	@Use: rewrite main-#.py file
'''
def run_auto_main(alphas, work_dir, script_dir):

	print('\n>> running run_auto_main for total: ' + str(len(alphas)))
	print('\n>> removing existing scripts...')

	shutil.rmtree(script_dir)
	os.mkdir(script_dir)

	for k in alphas:
		print('\n>> alpha: ' + str(k))
		src_path = os.path.join(work_dir, 'ppr-0.py')
		tgt_path = os.path.join(script_dir, 'ppr-' + str(k) + '.py')
		src_strs = ['alpha = 0']
		tgt_strs = ['alpha = ' + str(k)]
		auto_gen(src_path, tgt_path, src_strs, tgt_strs)


'''
	@Use: rewrite main-#.sh file
'''
def run_auto_sh(alphas, work_dir, shell_dir):

	print('\n>> running run_auto_sh for total: ' + str(len(alphas)))
	print('\n>> removing existing scripts...')

	shutil.rmtree(shell_dir)
	os.mkdir(shell_dir)

	for k in alphas:

		print('\n>> alpha: ' + str(k))

		src_path = os.path.join(work_dir,'ppr-0.sh')
		tgt_path = os.path.join(shell_dir,'ppr-' + str(k) + '.sh')
		src_strs = ['ppr-0']
		tgt_strs = ['ppr-' + str(k)]

		auto_gen(src_path, tgt_path, src_strs, tgt_strs)

'''
	@Use: assert all ppr probs for all words have been computed
		  ie.	assert_all_ppr(_output_dir, gr_path, 0.9)
'''
def assert_all_ppr(ppr_dir, gr_path, alpha):
	
	_, words = load_as_list(gr_path)

	bad = []

	for s in words:
		name = s + '-' + str(alpha) + '.pkl'
		path = os.path.join(ppr_dir,name)

		if not os.path.exists(path):
			bad.append(s)

	if bad:
		print('\n>> !!ERROR: missing ' + str(len(bad)) + ' words for ' + str(alpha))
	else:
		print('\n>> found ppr for all words at ' + str(alpha))

############################################################
'''
	run all
'''

run_auto_main( alphas
	 		 , work_dir
	 		 , script_dir)

run_auto_sh  ( alphas
	         , work_dir
	         , shell_dir )

# [assert_all_ppr(_output_dir, gr_path, a) for a in alphas]






