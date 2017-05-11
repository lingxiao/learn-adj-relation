############################################################
# Module  : pick out subgraph with base comparative and
#           superlative pairs
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

from app     import *
from scripts import *
from utils import *

'''
    @Use: construct subgraph with all base, comparatives, and superlative edges
    @Input : - vertices :: [(String, String)]
             - G        :: Graph
    @Output: iterator outputting all edges between vertices
'''
def train_edges(vertices, G):


    '''
        get the base comparative and superlative triples
        that have edges in the graph
    '''
    G_base_compare    = [(s,t,v) for s,t,v in edges if base_compare(s,t)   ]
    G_compare_base    = [(s,t,v) for s,t,v in edges if compare_base(s,t)   ]
    G_base_superla    = [(s,t,v) for s,t,v in edges if base_superla(s,t)   ]
    G_superla_base    = [(s,t,v) for s,t,v in edges if superla_base(s,t)   ]
    G_compare_superla = [(s,t,v) for s,t,v in edges if compare_superla(s,t)]
    G_superla_compare = [(s,t,v) for s,t,v in edges if superla_compare(s,t)]

    subgraph = G_base_compare        \
             + G_compare_superla     \
             + G_base_superla        \
             + G_superla_base        \
             + G_compare_superla     \
             + G_superla_compare

    return subgraph


'''
    @Use: get base comparative superlative triples
        and base compare, base super, and compare super pairs

    @Input: train_dir :: String  directory to training data
    @Output: dictionary with key and value types:
                base-compare  :: [(String, String)]
                compare-super :: [(String, String)]
                base-super    :: [(String, String)]   
                triples       :: [(String, String, String)]
'''
def train_vertices(train_dir):

    paths    = [os.path.join(train_dir, p) for p in os.listdir(train_dir)]

    base_compare_path  = [p for p in paths if 'base-compara' in p ]
    base_super_path    = [p for p in paths if 'base-superla' in p   ]
    compare_super_path = [p for p in paths if 'comparative-super' in p]
    triple_path        = [p for p in paths if 'base-compare-super' in p]

    if base_compare_path   \
    and base_super_path    \
    and compare_super_path \
    and triple_path:
        
        tup       = lambda xs : (xs[0], xs[1])
        trip      = lambda xs : (xs[0], xs[1], xs[2])
        open_file = lambda path, f : [f(x.split(' ')) for x in \
                                     open(path[0],'rb').read().split('\n') \
                                     if len(x.split(' ')) >= 2]

        base_compare  = open_file(base_compare_path, tup)
        base_super    = open_file(base_super_path  , tup)
        compare_super = open_file(compare_super_path, tup)
        triples       = open_file(triple_path, trip)

        return {'base-compare' : base_compare
               ,'base-super'   : base_super
               ,'compare-super': compare_super
               , 'triples'     : triples}

    else:
        raise NameError('Cannot locate assets')


'''
    @Deprciated
'''
def _train_edges(edges, vertices):

    '''
        get the base comparative and superlative triples
        that have edges in the graph
    '''
    G_base_compare    = [(s,t,v) for s,t,v in edges if base_compare(s,t)   ]
    G_compare_base    = [(s,t,v) for s,t,v in edges if compare_base(s,t)   ]
    G_base_superla    = [(s,t,v) for s,t,v in edges if base_superla(s,t)   ]
    G_superla_base    = [(s,t,v) for s,t,v in edges if superla_base(s,t)   ]
    G_compare_superla = [(s,t,v) for s,t,v in edges if compare_superla(s,t)]
    G_superla_compare = [(s,t,v) for s,t,v in edges if superla_compare(s,t)]

    subgraph = G_base_compare        \
             + G_compare_superla     \
             + G_base_superla        \
             + G_superla_base        \
             + G_compare_superla     \
             + G_superla_compare

    return subgraph

