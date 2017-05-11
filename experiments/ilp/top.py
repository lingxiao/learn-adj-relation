# ############################################################
# # Module  : ILP 
# # Date    : April 12th
# # Author  : Xiao Ling, merle
# ############################################################

# import os
# import shutil

# from scripts import *
# from utils   import *
# from app     import *

# from experiments.ilp import *

# # from pulp    import *

# from collections import Counter

# ############################################################
# '''
# 	open gold
# '''
# exp_root = get_path('ilp')
# ccb      = read_gold(get_path('ccb'))
# moh      = read_gold(get_path('bansal'))


# '''
# 	@Use: compute pairwise comparison score where if no edge exist,
# 	      then predict outgoing edge from `s` using function `out_at`
# 	@Input: `word_pair_path`  :: String, path to .txt with word pairs in form:
# 											word1, word2
# 			`out_path`        :: String, path to save results										
# 			`refresh`         :: Bool, if true do not recompute value
# 	@Returns: None			
# '''
# # def versus(word_pair_path, out_path, refresh = True):

# word_pair_path = '/Users/lingxiao/Documents/research/code/learn-adj-relation/deploy/words/train-pairs/batch-0.txt'
# out_path = os.path.join(exp_root,'temp.txt')
# refresh = True

# '''
# 	open graph
# E,V = load_as_list(get_path('graph'))

# '''
# 	open all results from last session. 
# 	otherwise immediately ping out_path with empty file
# '''
# last_session = []

# if refresh: 

# 	if os.path.exists(out_path):
# 		with open(out_path, 'rb') as h:
# 			for stv in h:
# 				if len(stv.split(': ')) == 2:
# 					st, v = stv.split(': ')
# 					s,t   = st.split(', ')
# 					last_session.append((s,t))
# 	else:
# 		h = open(out_path, 'wb')
# 		h.close()

# '''
# '''
# 	remove computed values so we don't have to recompute 
# 	values from last time if we are resuming.
# pairs     = [x.split(', ') for x in open(word_pair_path,'rb').read().split('\n') \
#             if len(x.split(', ')) == 2]
# pairs     = [(s,t) for s,t in pairs if (s,t) not in last_session]		

# print('\n>> Found ' + str(len(pairs)) + ' pairs since last session')


# pairs = pairs + [('helpless','run')]


# scores = dict()

# # for s,t in pairs:
# for s,t in [pairs[-1]]:

# 	Es_both = Ev(s,E)
# 	Es_neg  = Ev_neg(s,E)
# 	Es_pos  = Ev_pos(s,E)


# 	s_ge_t = s + '>' + t
# 	t_ge_s = t + '>' + s


# 	if s_to_t or t_to_s:

# 		tot = float(len(s_to_t) + len(t_to_s))

# 		scores[s_ge_t] = len(s_to_t)/tot
# 		scores[t_ge_s] = len(t_to_s)/tot

# 	else:
# 		print('here')

# 		s_to_t = [(x,y,z) for x,y,z in E if x == s]

# '''

# ############################################################
# '''
# 	Computing expected values over subsets
# '''

# '''
# 	@Use   : compute the expected value of vertex `s`
# 	         over integers {-K,K}
# 	@Output: E[x] :: Float  
# '''
# def Ev(s,E):
# 	return Ev_neg(s,E) + Ev_pos(s,E)


# '''
# 	@Use   : compute the expected value of vertex `s`
# 	         over integers {0,K}
# 	@Output: E[x] :: Float  
# '''
# def Ev_pos(s,E):

# 	eps = 1e-5
# 	K   = 40 + 1

# 	# x -> s
# 	in_neigh = [(x,y,z) for x,y,z in E if s == y]


# 	# batch the neighbors by unique (s,t) pairs
# 	in_neighs  = [[k,]*v for k,v in Counter([(x,y) for x,y,_ in in_neigh]).items()]

# 	'''
# 		construct distribution over {0, +K}
# 	'''
# 	dist = {k : 0 for k in range(K)}

# 	for ins in in_neighs:
# 		dist[len(ins)] += 1

# 	'''
# 		smooth out the distribution
# 	'''
# 	for k in dist:
# 		if dist[k] == 0: dist[k] = eps

# 	'''	
# 		compute the expected value
# 	'''	
# 	ev = sum(k * v for k,v in dist.iteritems())

# 	return ev


# '''
# 	@Use   : compute the expected value of vertex `s`
# 	         over integers {-K,0}
# 	@Output: E[x] :: Float  
# '''
# def Ev_neg(s,E):

# 	eps = 1e-5
# 	K   = 40 + 1

# 	# s -> y
# 	out_neigh  = [(x,y,z) for x,y,z in E if s == x]
# 	out_neighs = [[k,]*v for k,v in Counter([(x,y) for x,y,_ in out_neigh]).items()]

# 	'''
# 		construct distribution over {-K, +K}
# 	'''
# 	dist = {-k : 0 for k in range(K) }


# 	for outs in out_neighs:
# 		dist[-len(outs)] += 1

# 	'''
# 		smooth out the distribution
# 	'''
# 	for k in dist:
# 		if dist[k] == 0: dist[k] = eps

# 	'''	
# 		compute the expected value
# 	'''	
# 	ev = sum(k * v for k,v in dist.iteritems())

# 	return ev






















