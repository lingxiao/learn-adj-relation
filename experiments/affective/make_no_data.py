############################################################
# Module  : find subset of pairs with no data and have affective labelsa
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os
import math
import numpy as np
import networkx as nx
from sklearn.metrics import r2_score
from sklearn.linear_model import ElasticNet
import pickle

from app     import *
from utils   import *
from scripts import *
from scripts.graph import *
from experiments.argmax import *
from experiments.rank_all import *
from experiments.affective import *

############################################################
'''
  construct subset of pairs that appear in norms
'''
_, _, ccb_gold = no_data_pairs(test['ccb'])
_, _, moh_gold = no_data_pairs(test['moh'])
_, _, bcs_gold = no_data_pairs(test['bcs'])


def make_no_data(gold, name):

  out_path = os.path.join(work_dir['no-data'], name + '.pkl')

  norms    = []

  cats = [cat for _,cat in NORM.iteritems()]

  for [s],[t] in gold:

    s_in = sum([int(s in cat) for cat in cats])
    t_in = sum([int(t in cat) for cat in cats])

    if s_in >= 1 and t_in >= 1:
      norms.append((s,t))


  norms = { k : [t] for k,t in enumerate(list(set(norms)))}

  with open(out_path,'wb') as h:
    pickle.dump(norms,h)


make_no_data(bcs_gold, 'bcs')
make_no_data(ccb_gold, 'ccb')
make_no_data(moh_gold, 'moh')















