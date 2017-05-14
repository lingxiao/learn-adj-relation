############################################################
# Module  : combine models
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os
import pickle


from app     import *
from utils   import *
from scripts import *
from scripts.graph import *
from experiments.argmax import *
from experiments.rank_all import *
from experiments.milp import *


############################################################
'''
	run on all data set
'''
decide      = paper_milp(ngram_dir, stat, count)	
SAVE        = True
results_dir = work_dir['results']

if not os.path.exists(results_dir):
	os.mkdir(results_dir)

print('\n\t>> ranking moh-no-ties milp ...')
rank_all_gold( test['moh-no-tie']
	         , decide
	         , os.path.join(results_dir, 'moh-no-tie.txt')
	         , refresh = False
	         , save    = SAVE )

print('\n\t>> ranking ccb-no-ties milp ...')
rank_all_gold( test['ccb-no-tie']
	         , decide
	         , os.path.join(results_dir, 'ccb-no-tie.txt')
	         , refresh = False
	         , save    = SAVE )


print('\n\t>> ranking bcs with milp ...')
rank_all_gold( test['bcs']
	         , decide
	         , os.path.join(results_dir, 'bcs.txt')
	         , refresh = False
	         , save    = SAVE )

print('\n\t>> ranking ccb with milp ...')
rank_all_gold( test['ccb']
	         , decide
	         , os.path.join(results_dir, 'ccb.txt')
	         , refresh = False
	         , save    = SAVE )

print('\n\t>> ranking moh with milp ...')
rank_all_gold( test['moh']
	         , decide
	         , os.path.join(results_dir, 'moh.txt')
	         , refresh = False
	         , save    = SAVE )











