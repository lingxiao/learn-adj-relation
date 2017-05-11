############################################################
# Module  : count number of words in ngrams for all words in ppdb
# Date    : April 17th.
# Author  : Xiao Ling
############################################################

import os
import shutil
import pickle
import json

from app import *
from scripts import *
from utils   import *

############################################################
'''
	@Use: compute frequency of words for all words that appear
	       in ppdb-ngram graph over ngram corpus
'''
def collect_vocab_freq(graph_path, one_gram_path, out_path):

	print('\n>> get all ppdb-ngram words')
	_,V = load_as_list(graph_path)

	print('\n>> making sure all words appear at least once')				

	words = { s : 1 for s in V }

	print('\n>> counting words')
	with open(one_gram_path,'rb') as ngram:
		for wordn in ngram:
			wordn = wordn.replace('\n','').split('\t')
			if len(wordn) == 2:
				word, n = wordn
				word = word.lower()
				if word in words:
					words[word] += int(n)
	
	print('\n>> Saving to ' + out_path)	
	with open(out_path,'wb') as f:
		pickle.dump(words,f)

	return words

############################################################
'''
	run
'''
graph_path    = get_path('ppdb-ngram')
one_gram_path = get_path('1-gram')
out_path      = get_path('word-freq')

# collect_vocab_freq(graph_path, one_gram_path, out_path)

with open(out_path,'rb') as h:
	xs = pickle.load(h)














