############################################################
# Module  : Experiment functions
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import pickle

from app     import *
from utils   import *
from scripts import *

############################################################
'''
	@Use: given gold set and decision function
		  output ranking over all gold set
	@Input - golds     :: [[[String]]]
	       - decide_fn :: String -> Float
	@output: Dict String _
'''
def rank_all_gold(golds, decide_fn, out_path, refresh = True, save = True):

	if refresh and os.path.exists:

		print('\n\t>> Refreshing... found path. Skipping.')
		return None

	else:
		if os.path.exists(out_path):
			print('\n\t>> Removing existing file at outpath if it exists')
			os.remove(out_path)
		return go_rank(golds, decide_fn, out_path, save)



############################################################
'''
	helper
'''
def go_rank(golds, decide_fn, out_path, save):

	report = dict()
	num    = 0

	print('\n\t>> ranking adjectives')
	for gold in golds:

		algo, raw = decide_fn(gold)
		pairwise  = pairwise_accuracy(gold, algo)
		ktau      = tau(gold,algo)

		report[num] = {'gold'    : gold
		              ,'algo'    : algo
		              ,'pairwise': pairwise
		              ,'tau'     : ktau
		              ,'|tau|'   : abs(ktau)
		              ,'raw'     : raw
		              }

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

	print('\n\t>> averages:')
	print('\n\t\t pairwise: ' + str(round(out['pairwise']*100,2)))
	print('\n\t\t tau:      ' + str(out['tau']))
	print('\n\t\t |tau|:    ' + str(out['|tau|']))

	if save and out_path:
		name = out_path.split('/')[-1]
		save_results(out, out_path)
		print('\n' + '-'*50)

	return out








