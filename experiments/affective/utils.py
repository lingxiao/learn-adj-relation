############################################################
# Module  : affective norm utils
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os
import pickle
import numpy as np
import networkx as nx


from app     import *
from utils   import *
from scripts import *
from scripts.graph import *
from experiments.argmax import *
from experiments.rank_all import *
from experiments.elastic_net import *

def open_norm(path):

	with open(path,'rb') as h:
		out = h.read().split('\n')

	out = [o.split(' ') for o in out if len(o.split(' ')) == 2]
	out = { w : float(n) for w,n in out }

	return out


