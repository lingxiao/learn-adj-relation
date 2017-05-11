############################################################
# Module  : Auto generate python file
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
from utils   import *
from scripts import *


'''
	@Use: given `src_path` to existing foo.py and nonexisting bar.py
		  open foo.py and swap out `src_str` string in foo.py
		  for `tgt_str` string in bar.py
		  write to `tgt_path`
	@Inputs: src_path :: String
			 tgt_path :: String
			 src_strs :: [String]	  
			 tgt_strs :: [String]
'''
def auto_gen(src_path, tgt_path, src_strs, tgt_strs):

	src = open(src_path,'rb').read().split('\n')

	tgt = src

	for src_str, tgt_str in zip(src_strs, tgt_strs):
		tgt = [swap(x, src_str, tgt_str) for x in tgt]

	with open(tgt_path,'wb') as h:
		h.write('\n'.join(tgt))

	return tgt


def swap(xs, src_str, tgt_str):
	if src_str in xs:
		return xs.replace(src_str, tgt_str)
	else:
		return xs

