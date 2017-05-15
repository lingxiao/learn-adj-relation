############################################################
# Module  : estimate missing edge using bag of coins model
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
from experiments.bag_coins import *

############################################################
'''
	different graph parameters
'''
edge        = [ 'edge-wt' ]

topo        = [ 'ppdb-ngram'
              , 'ppdb'
              , 'ngram' 
              ]

alphas      = [ 0.8 ]
graph_names = [t + '|' + e + '|' + str(a) for t in topo for e in edge for a in alphas]              

keys        = [e + '-' + t for e in edge for t in topo]
degree_dirs = data_dirs( 'out-degree' , keys )
ppr_dirs    = data_dirs( 'ppr' , [s + '-' + str(_a) for s in keys for _a in alphas ])

asset_dirs  = { k : v for k,v in list(degree_dirs.iteritems())
                               + list(ppr_dirs.iteritems())  }

work_dir = locate_dirs( get_path('bag-coins'), ['results'
	                                           ,'script'
	                                           ,'shells'])

baseline = locate_dirs( get_path('baseline'), ['no-data'] )

############################################################
'''
	graphs
'''
try:
	G_ppdb, G_ngram, G_ppng, G_ppdb_1, G_pnng_1
except:	
	G_ppdb   = Graph( 'ppdb|edge-wt|0.8'       , asset_dirs )
	G_ngram  = Graph( 'ngram|edge-wt|0.8'      , asset_dirs )
	G_ppng   = Graph( 'ppdb-ngram|edge-wt|0.8' , asset_dirs )

GRAPH = {
          'ppdb'        : G_ppdb
		 ,'ngram'       : G_ngram
		 ,'ppdb-ngram'  : G_ppng
		 }

############################################################
'''
	get no data pairs
'''

no_data_gold = lambda p : no_data_pairs(p)[2]

ngram_gr = { 
      'ccb': no_data_gold(os.path.join( baseline['no-data']
      	                 , 'baseline-ngram-ccb-no-data.pkl')),

      'moh': no_data_gold(os.path.join( baseline['no-data']
      	                 , 'baseline-ngram-moh-no-data.pkl')),

      'bcs': no_data_gold(os.path.join( baseline['no-data']
      	                 , 'baseline-ngram-bcs-no-data.pkl'))
	   }     


ppdb_gr = { 

      'ccb': no_data_gold(os.path.join( baseline['no-data']
      	                 , 'baseline-ppdb-ccb-no-data.pkl')),

      'moh': no_data_gold(os.path.join( baseline['no-data']
      	                 , 'baseline-ppdb-moh-no-data.pkl')),

      'bcs': no_data_gold(os.path.join( baseline['no-data']
      	                 , 'baseline-ppdb-bcs-no-data.pkl'))
	   }     


both_gr = { 

      'ccb': no_data_gold(os.path.join( baseline['no-data']
      	                 , 'baseline-ppdb-ngram-ccb-no-data.pkl')),

      'moh': no_data_gold(os.path.join( baseline['no-data']
      	                 , 'baseline-ppdb-ngram-moh-no-data.pkl')),

      'bcs': no_data_gold(os.path.join( baseline['no-data']
      	                 , 'baseline-ppdb-ngram-bcs-no-data.pkl'))
	   }   

############################################################
'''
	load test sets
'''
print('\n\t>> load base-comparative-superlative')
bcs = join(_xs for _, _xs in train_vertices(get_path('bcs')).iteritems())
bcs = [[[w] for w in _ws] for _ws in bcs]

print('\n\t>> load turk')
ccb = read_gold( get_path('ccb') )

print('\n\t>> load moh')
moh = read_gold( get_path('moh') )

print('\n\t>> load moh-ppdb')
moh_ppdb = read_gold( get_path('moh-ppdb') )

print('\n\t>> load moh-no-tie')
mohn = read_gold( get_path('moh-no-tie') )

print('\n\t>> load turk-no-tie')
ccbn = read_gold( get_path('ccb-no-tie') )


full_test = {
	  'bcs'       : bcs
	, 'ccb'       : ccb
	, 'moh'       : moh 
	, 'moh-ppdb'  : moh_ppdb
	, 'moh-no-tie': mohn
	, 'ccb-no-tie': ccbn
	}



