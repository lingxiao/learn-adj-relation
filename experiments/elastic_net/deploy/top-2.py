############################################################
# Module  : pointwise estimation baeline
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

############################################################
'''
	different graph parameters
'''
edge        = [ 'edge-wt' ]
topo        = [ 'ppdb-ngram', 'ppdb', 'ngram' ]
alphas      = [ 0.8 ]
graph_names = [t + '|' + e + '|' + str(a) for t in topo for e in edge for a in alphas]              

keys        = [e + '-' + t for e in edge for t in topo]
degree_dirs = data_dirs( 'out-degree' , keys )
ppr_dirs    = data_dirs( 'ppr' , [s + '-' + str(_a) for s in keys for _a in alphas ])

asset_dirs  = { k : v for k,v in list(degree_dirs.iteritems())
                               + list(ppr_dirs.iteritems())  }

work_dir = locate_dirs( get_path('elastic-net'), ['results'
	                                             ,'script'
	                                             ,'shells'
	                                             ,'assets'])

baseline = locate_dirs( get_path('baseline'), ['no-data'] )

############################################################
'''
	graphs
'''
try:
	G_ppdb, G_ngram, G_ppng
except:	
	G_ppdb  = Graph( 'ppdb|edge-wt|0.8'       , asset_dirs )
	G_ngram = Graph( 'ngram|edge-wt|0.8'      , asset_dirs )
	G_ppng  = Graph( 'ppdb-ngram|edge-wt|0.8' , asset_dirs )


GRAPH = {
          'ppdb'       : G_ppdb
		 ,'ngram'      : G_ngram
		 ,'ppdb-ngram' : G_ppng
		 }

############################################################
'''
	get no data pairs
'''
ngram_gr = { 
      'ccb': os.path.join( baseline['no-data']
      	                 , 'baseline-ngram-ccb-no-data.pkl'),

      'moh': os.path.join( baseline['no-data']
      	                 , 'baseline-ngram-moh-no-data.pkl'),

      'bcs': os.path.join( baseline['no-data']
      	                 , 'baseline-ngram-bcs-no-data.pkl')
	   }     


ppdb_gr = { 

      'ccb': os.path.join( baseline['no-data']
      	                 , 'baseline-ppdb-ccb-no-data.pkl'),

      'moh': os.path.join( baseline['no-data']
      	                 , 'baseline-ppdb-moh-no-data.pkl'),

      'bcs': os.path.join( baseline['no-data']
      	                 , 'baseline-ppdb-bcs-no-data.pkl')
	   }     


both_gr = { 

      'ccb': os.path.join( baseline['no-data']
      	                 , 'baseline-ppdb-ngram-ccb-no-data.pkl'),

      'moh': os.path.join( baseline['no-data']
      	                 , 'baseline-ppdb-ngram-moh-no-data.pkl'),

      'bcs': os.path.join( baseline['no-data']
      	                 , 'baseline-ppdb-ngram-bcs-no-data.pkl')
	   }   


############################################################
'''
	make word2index dicts
'''
def make_word2index():
	print('\n\t>> [ Making w2idx, id2w dicts ]')
	# for num in [10, 20, 30, 40, 50,100,200,300,400,500,605]:
	for num in [40,50,100]:
		encode(G_ppng, num, work_dir['assets'])

make_word2index()

