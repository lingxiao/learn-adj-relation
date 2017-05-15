############################################################
# Module  : combine all no-data files into one big file
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

num_jobs      = 87
no_data_dir   = get_path('ngram-no-data')
no_data_paths = [os.path.join(no_data_dir, p) for p in os.listdir(no_data_dir)]


def run():

	no_data_pairs = ''
	
	for path in no_data_paths:
	    pairs = open(path,'rb').read()
	    no_data_pairs += pairs

	for k in xrange(num_jobs + 1):
		out_path = os.path.join(no_data_dir, 'batch-' + str(k) + '-no-data.txt')
		with open(out_path,'wb') as h:
			h.write(no_data_pairs)


run()			