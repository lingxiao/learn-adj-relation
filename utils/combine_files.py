############################################################
# Module  : combine all files in directory with extension
#          into one big file
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
from utils   import *
from scripts import *


'''
	@Use: combine all .txt files at src_dir into one big .txt
	     file to be saved at tgt_path
'''
def combine_txt(src_dir, tgt_path):

	paths = [os.path.join(src_dir, p) for p in os.path.listdir(src_dir) \
			 if ext in p]

	print('\n>> found ' + str(len(paths)) + ' files in ' + src_dir)		
	print('\n>> saving all files at ' + tgt_path)

	with open(tgt_path,'wb') as tgt:
		for p in paths:
			with open(p, 'rb') as src:
				for line in src:
					if line: 
						tgt.write(line + '\n')

	print('\n>> Done!')		
