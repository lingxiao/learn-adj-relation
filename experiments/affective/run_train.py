############################################################
# Module  : run train elastic net regression
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os
import math
import numpy as np
from sklearn.linear_model import ElasticNet
import pickle
import matplotlib.pyplot as plt

from app     import *
from utils   import *
from scripts import *
from experiments.argmax import *
from experiments.rank_all import *
from experiments.affective import *
from experiments.elastic_net import train, encode_decode

############################################################
'''
  Training config
'''
w2idx = { cat : k for k,cat in enumerate(NORM) }

alpha      = 0.5
l1_ratio   = 0.5

data_set   = 'affective'

fix, phi   = ''  , phi_baseline( NORM, w2idx )
OP , op    = '`dot`' , phi_dot
SAVE       = True

em = to_x(phi,op)

############################################################
'''
	full train and validation data 
'''
if data_set == 'ppdb-ngram':
	gold = both_gr
elif data_set == 'ppdb':
	gold = ppdb_gr
elif data_set == 'ngram':
	gold = ngram_gr
elif data_set == 'affective':
	gold = affective

train_X, train_y, train_gold = no_data_pairs(gold['bcs'])

X    = to_X(train_X, phi, op)
y    = np.array(train_y)

############################################################
'''
	Train 
'''
dir_name = data_set + '|'                 \
         + '[phi^'+ fix + '(s)' + OP + 'phi^' + fix + '(t)]|'  \
         + 'alpha='   + str(alpha)   + '|'  \
         + 'l1='      + str(l1_ratio)   


print('\n\t>> Training ' + dir_name)
exec_train( dir_name = dir_name

	      , alpha    = alpha
	      , l1_ratio = l1_ratio

	      , rho      = phi
	      , op       = op
	      , w2idx    = w2idx

	      , train    = no_data_pairs (gold['bcs'])
	      , valid    = no_data_pairs (gold['ccb'])
	      , test     = no_data_pairs (gold['moh'])

	      , out_root = work_dir['results']
	      , save     = SAVE

	      )



