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

no_data_pairs = []

tup = lambda t : (t[0],t[1])

for path in no_data_paths:
    pairs = [tup(x.split(', ')) for x in open(path,'rb').read().split('\n') if len(x.split(', ')) == 2]
    no_data_pairs += pairs

no_data_pairs = list(set(no_data_pairs))
out = '\n'.join( ', '.join([s,t]) for s,t in no_data_pairs )

for k in xrange(num_jobs + 1):
	out_path = os.path.join(no_data_dir, 'batch-' + str(k) + '-no-data.txt')
	with open(out_path,'wb') as h:
		h.write(out)







