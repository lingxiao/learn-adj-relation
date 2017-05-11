############################################################
# Module  : Open Ngram and read linguistic pattern
# Date    : April 3rd, 2017
# Author  : Xiao Ling, merle
############################################################

import os
import gzip
from utils import *

############################################################
'''
	@Use   : Open all ngrams in ngram_dir and stream output as tuple of (ngram, count)
	@Input : - ngram_dir :: String
	         - debug     :: Bool,  if true then only output parts of stream
	@Output: Iterator output ngrams of form:
				(ngram, count) :: Iterator (String, String)

			Throw: NameError if path does not exists
'''
def with_ngram(ngram_dir, debug = False):

	if not os.path.exists(ngram_dir):
		raise NameError('Path not found at ' + ngram_dir)

	else:

		ngram_paths = [os.path.join(ngram_dir, p) for \
		               p in os.listdir(ngram_dir) if '.txt' in p]	

		if not ngram_paths:
			raise NameError('Directory Empty at ' + ngram_dir)

		if debug:
			ngram_paths = [ngram_paths[0]]		              

		for path in ngram_paths:

			with open(path, 'rb') as h:
				for line in h:
					xsn = line.split('\t')
					if len(xsn) == 2:
						xs,n = xsn
						n,_  = n.split('\n')
						yield (xs,n)

'''
	@Use: stream normalized ngrams directly from zipped file
'''
def with_zip_ngram(in_dir, debug = False):

	if debug:
		suffix = 'debug mode'
	else:
		suffix = ' production mode'

	print('\n>> unpack raw zip ngrams in ' + suffix)

	Tok = Tokenizer(casefold=True, elim_punct=True)

	paths = [os.path.join(in_dir,q) for q in os.listdir(in_dir) if 'gz' in q]

	if debug:
		paths = [paths[-5]]

	print('\n>> unpacking ' + str(len(paths)) + ' raw n-gram files')

	for in_path in paths:

		print('\n>> opening ' + in_path)

		with gzip.open(in_path,'rb') as inh:
			for raw in inh:
				proc = norm(Tok,raw)
				if len(proc.split('\t')) == 2:
					gm, n = proc.split('\t')
					yield (gm, int(n))

def norm(Tok, rs):
    ts = rs.decode('utf-8')
    ts = Tok.tokenize(ts)
    ys = '\t'.join(ts)
    ys = ys.encode('utf-8')
    return ys.strip()

############################################################
'''
	@Use: Given path to linguistic pattern, output pattern
'''
def read_pattern(pattern_path):

	if os.path.exists(pattern_path):

		strong_weak, weak_strong  = open(pattern_path,'rb').read().split('=== weak-strong')
		strong_weak = [p for p in strong_weak.split('\n') if p][1:]
		weak_strong = [p for p in weak_strong.split('\n') if p][:-1]

		return {'strong-weak': strong_weak, 'weak-strong': weak_strong}

	else:
		raise NameError('Cannot find pattern at path ' + pattern_path)
