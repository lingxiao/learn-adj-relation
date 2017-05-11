############################################################
# Module  : compute dot product between two word vectors
# Date    : December 22nd
# Author  : Xiao Ling
# Source  : http://www.enchantedlearning.com/grammar/partsofspeech/adjectives/comparatives.shtml
############################################################

import os
import numpy as np
from utils import *


'''
	@Use: compute word2vec values for all words and save
		  if word is out of vocabulary, then default its vector to be (0,0,...)
	@Input: `word_2_vec_path` :: String, path to word2vec .txt file
			`word_pair_path`  :: String, path to .txt with word pairs in form:
											word1, word2
			`out_path`        :: String, path to save results										
			`refresh`         :: Bool, if true do not recompute value

	@Returns: None			
'''
def dot(word_vector_path, word_pair_path, out_path, refresh = True):

	print('\n>> running `dot` with refresh = ' + str(refresh))

	'''
		open all results from last session. 
		otherwise immediately ping out_path with empty file
	'''
	last_session = []

	if refresh: 

		if os.path.exists(out_path):
			with open(out_path, 'rb') as h:
				for stv in h:
					if len(stv.split(': ')) == 2:
						st, v = stv.split(': ')
						s,t   = st.split(', ')
						last_session.append((s,t))
		else:
			h = open(out_path, 'wb')
			h.close()

	'''
		open word2vec.
		out of vecab word default to zero vector
	'''
	vector,ws = read_vector(word_vector_path)
	oov_vec   =  np.array([0]*len(vector[ws[0]]))


	'''
		remove computed values so we don't have to recompute 
		values from last time if we are resuming.
	'''
	pairs     = [x.split(', ') for x in open(word_pair_path,'rb').read().split('\n') \
	            if len(x.split(', ')) == 2]
	pairs     = [(s,t) for s,t in pairs if (s,t) not in last_session]		

	print('\n>> Found ' + str(len(pairs)) + ' pairs since last session')


	'''
		open file handle to save words
	'''	
	for s,t in pairs:

		if s not in vector: 
			vector[s] = oov_vec

		if t not in vector: 
			vector[t] = oov_vec

		v = np.dot(vector[s], vector[t])

	 	with open(out_path,'a') as out:
			out.write(s + ', ' + t + ': ' + str(v) + '\n') 



def to_path(s,t,out_dir):
	return os.path.join(out_dir, s +'-' + t + '.txt')



def read_vector(word_2_vec_path):

	vector = dict()
	words  = []

	with open(word_2_vec_path,'rb') as vec:
		for v in vec:
			if v:
				v = v.split(' ')
				word = v[0]
				v    = [float(x) for x in v[1:-1]]

				if word != '\n':
					vector[word] = np.asarray(v)
					words.append(word)

	return vector, words

