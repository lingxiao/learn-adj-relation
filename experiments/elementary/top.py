############################################################
# Module  : Experiment functions
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import pickle
import operator
from collections import Counter

from app     import *
from utils   import *
from scripts import *
from experiments import *
from experiments.rank_all import *

############################################################
'''

	@Use: given data_root directory path 
	      pickle load all data into one dictionary
'''
def load_probs_table(src):

	paths    = [os.path.join(src,p)     \
	           for p in os.listdir(src) \
	           if '.pkl' in p]

	data = {}

	for p in paths:
		d = pickle.load(open(p,'rb'))
		data = dict(data, **d)

	return data

############################################################
'''
	elementary decision functions

	@Use: decision using coin
'''
def decide_coin(probs):
	def fn(s):
		return probs[s]['H']
	return fn

def decide_die(probs):
	def fn(s):
		if s in probs:
			max_prob = 0.0
			max_face = None
			for o,p in with_Omega(probs[s]):
				if p > max_prob:
					max_prob = p
					max_face = o
			return max_face
		else:
			return 0.0

	return fn

def decide_coin_bet(probs):
	def fn(s):
		d = probs[s]
		H = d['|H|']
		T = d['|T|']
		tot = float(H + T)
		if not tot:
			tot = 1e-5
		return (H - T)/tot
	return fn

def decide_die_bet(probs):
	def fn(s):
		'''
			use dense reconstruction of
			entire elementary event space
		'''
		if s in probs:
			omega_sparse = probs[s]	

			ev  = 1.0
			tot = 0

			for o,p in with_Omega(omega_sparse):
				ev += (o*p)
				tot += 1.0

			return ev/tot
		else:
			return 0.0

	return fn

'''
	@Input: Ews :: [(String,Float)]
'''
def to_algo(raw):

	algo = dict()

	for s,v in raw:
		if v in algo: algo[v].append(s)
		else: algo[v] = [s]

	algo = [(k,ws) for k,ws in algo.iteritems()]	
	algo = sorted(algo, key = lambda tup : tup[0])
	algo = [ws for _,ws in algo]
	return algo

'''
	@Use: given gold set and decision function
		  output ranking over all gold set
	@Input - golds     :: [[[String]]]
	       - decide_fn :: String -> Float
	@output: Dict String _
'''
def decide(golds, decide_fn, out_path):

	print('\n\t>> removing existing file at outpath if it exists')
	if os.path.exists(out_path):
		os.remove(out_path)

	report = dict()
	num    = 0

	print('\n\t>> ranking adjectives')
	for gold in golds:
		ws  = join(gold)
		Ews = [(s,decide_fn(s)) for s in ws]

		algo     = to_algo(Ews)
		pairwise = pairwise_accuracy(gold, algo)
		ktau     = tau(gold,algo)

		report[num] = {'gold'    : gold
		              ,'algo'    : algo
		              ,'tau'     : ktau
		              ,'|tau|'   : abs(ktau)
		              ,'pairwise': pairwise
		              ,'raw'     : Ews}
		num +=1             

	print('\n\t>> computing averages')
	avg_pair    = sum(d['pairwise'] for _,d in report.iteritems())
	avg_tau     = sum(d['tau']      for _,d in report.iteritems())
	avg_abs_tau = sum(d['|tau|']    for _,d in report.iteritems())

	out = dict()
	out['pairwise'] = avg_pair/len(report)
	out['tau']      = avg_tau /len(report)
	out['|tau|']    = avg_abs_tau /len(report)
	out['ranking']  = report

	if out_path:

		name = out_path.split('/')[-1]

		print('\n\t>> testset: ' + name)
		print('\n\t>> pairwise: ' + str(out['pairwise']))
		print('\n\t>> tau: '      + str(out['tau']))
		print('\n\t>> |tau|: '    + str(out['|tau|']))
		print('\n\t>> saving results')

		save_results(out, out_path)
		print('\n' + '-'*50)

	return out









