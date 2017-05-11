############################################################
# Module  : count number of words in ngrams for all words in ppdb
# Date    : April 17th.
# Author  : Xiao Ling
############################################################

import os
import shutil
import pickle
import json
import gzip

from app import *
from scripts import *
from utils   import *


############################################################
'''
	@Use: stream normalized 2grams directly from zipped file
'''
def with_2_gram(in_dir):

	print('\n>> unpack raw two grams ...')

	Tok = Tokenizer(casefold=True, elim_punct=True)

	paths = [os.path.join(in_dir,q) for q in os.listdir(in_dir) if 'gz' in q]

	print('\n>> unpacking ' + str(len(paths)) + ' 2gm docs')

	cnt = 0

	for in_path in paths:

		print('\n>> unpacking and normalizing 2gm-' + str(cnt))

		with gzip.open(in_path,'rb') as inh:
			for raw in inh:
				proc = norm(Tok,raw)
				if len(proc.split('\t')) == 2:
					gm, n = proc.split('\t')
					yield (gm, int(n))

		cnt += 1

'''
	@Use: unpack two gram from in_dir and write to out_dir
'''
def unpack_two_gram(in_dir, out_dir):

	print('\n>> unpack raw two grams ...')

	Tok = Tokenizer(casefold=True, elim_punct=True)

	paths = [os.path.join(in_dir,q) for q in os.listdir(in_dir) if 'gz' in q]

	print('\n>> found ' + str(len(paths)) + ' 2gm docs')

	cnt = 0

	for in_path in paths:

		print('\n>> unpacking and normalizing 2gm-' + str(cnt))

		out_path = os.path.join(out_dir, '2gm-' + str(cnt) + '.txt')

		with open(out_path,'wb') as outh:
			with gzip.open(in_path,'rb') as inh:
				for raw in inh:
					outh.write(norm(Tok,raw) + '\n')

		cnt += 1

def norm(Tok, rs):
    ts = rs.decode('utf-8')
    ts = Tok.tokenize(ts)
    ys = '\t'.join(ts)
    ys = ys.encode('utf-8')
    return ys.strip()

############################################################
'''
	run main
'''
raw_dir      = '/Users/lingxiao/Documents/research/code/learn-adj-relation-data/ngrams/raw'
two_gram_dir = get_path('2-gram')

# unpack_two_gram(raw_dir, two_gram_dir)
















