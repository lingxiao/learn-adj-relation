############################################################
# Module  : All System Paths
# Date    : March 23rd, 2017
# Author  : Xiao Ling
############################################################

import os
import shutil
import glob
from utils import Writer

############################################################
'''
    System Root
'''
root = os.getcwd()

# local
if root[0:6] == '/Users':
    # output of processing data over ngram and word2vec from the grid
    data_root     = '/Users/lingxiao/Documents/research/code/learn-adj-relation-data'
    input_dir     = os.path.join(data_root, 'inputs')
    data_root_big = data_root

# nlp grid
elif root[0:5] == '/mnt/':
    data_root     = '/nlp/data/xiao/learn-adj-relation-data'
    data_root_big = data_root
    input_dir = os.path.join(data_root, 'inputs')

# tesla
else:
    data_root = ''

############################################################
'''
    System Environment
'''
PATH = {
        'data-root': data_root_big,

        # directories that should exist before application runs
        'critical-directories'      : {
            'data-root'    : data_root
           ,'deploy-code'  : os.path.join(root     , 'deploy')
           ,'deploy-data'  : os.path.join(data_root, 'deploy')
           ,'log'          : os.path.join(data_root, 'logs'   )
           ,'inputs'       : os.path.join(data_root, 'inputs' )
           ,'tests'        : os.path.join(input_dir, 'test')
           ,'results'      : os.path.join(data_root, 'results')
        },

        # path to files that must exist before application runs
        'small-inputs': {
            # training sets
            'bcs'      : os.path.join(input_dir, 'train')

            # test sets
           ,'ccb'         : os.path.join(input_dir, 'test/ccb.txt'     )
           ,'ccb-no-tie'  : os.path.join(input_dir, 'test/ccb-no-tie.txt')
           ,'moh-no-tie'  : os.path.join(input_dir, 'test/moh-no-tie.txt')
           ,'moh'         : os.path.join(input_dir, 'test/moh.txt'     )
           ,'moh-ppdb'    : os.path.join(input_dir, 'test/moh-ppdb.txt')
           ,'moh!ppdb'    : os.path.join(input_dir, 'test/moh-ngram.txt')
           ,'anne-25'     : os.path.join(input_dir, 'test/anne-25.txt' )
           ,'anne-125'    : os.path.join(input_dir, 'test/anne-125.txt')
           },

        # path to very big files that may not be on local, but is on nlpgrid
        'big-inputs': {
               '1-gram'     : os.path.join(data_root_big, 'ngrams/vocab_cs.txt')
              ,'2-gram-raw' : os.path.join(data_root_big, 'ngrams/2gms-raw')
              ,'word2vec'   : os.path.join(data_root_big, 'word2vec/GoogleNews-vectors-negative300.txt')
              ,'word2vec-sm': os.path.join(data_root_big, 'word2vec/small.txt')
              ,'ngram-grep' : os.path.join(data_root_big, 'ngrams/grepped')
              ,'ngram-sm'   : os.path.join(data_root_big, 'ngrams/small'  )
              ,'affective-data'  : os.path.join(data_root_big, 'affective'     )
        },

        # outputs computed by experiments
        'outputs': {
              # varous kind of graphs in txt form
             'ppdb-txt'            : os.path.join(input_dir, 'raw-graph/ppdb.json')
           , 'ngram-txt'           : os.path.join(input_dir, 'raw-graph/ngram-txt')
           , 'ngram-bool-txt'      : os.path.join(input_dir, 'raw-graph/ngram-bool-txt')
           , 'ppdb-ngram-txt'      : os.path.join(input_dir, 'raw-graph/ppdb-ngram-txt')
           , 'ppdb-ngram-bool-txt' : os.path.join(input_dir, 'raw-graph/ppdb-ngram-bool-txt')

              # varous kind of graphs in pkl form
           , 'ppdb'                  : os.path.join(input_dir, 'raw-graph/ppdb')
           , 'ngram'                 : os.path.join(input_dir, 'raw-graph/ngram')
           , 'ngram-bool'            : os.path.join(input_dir, 'raw-graph/ngram-bool')
           , 'ppdb-ngram'            : os.path.join(input_dir, 'raw-graph/ppdb-ngram')
           , 'ppdb-ngram-bool'       : os.path.join(input_dir, 'raw-graph/ppdb-ngram-bool')
           , 'ppdb-ngram-full'       : os.path.join(input_dir, 'raw-graph/ppdb-ngram-full' )
           , 'ppdb-one-event-no-loop': os.path.join(input_dir, 'raw-graph/ppdb-one-event-no-loop')
           , 'ppdb-one-event-ngram-no-loop' : os.path.join(input_dir, 'raw-graph/ppdb-one-event-ngram-no-loop')

           # linguistic patterns
           , 'patterns'        : os.path.join(input_dir, 'patterns/two-sided-patterns.txt')

           # 1-gram counts
           , 'word-freq'    : os.path.join(input_dir, 'raw-graph/word-freq.pkl')
           , 'bigram-freq'  : os.path.join(input_dir, 'raw-graph/bigram-freq.pkl')
           },         

        'experiments': {
                'least-squares': os.path.join(root, 'experiments/least_squares')
              , 'baseline'     : os.path.join(root, 'experiments/baseline')
              , 'elementary'   : os.path.join(root, 'experiments/elementary')
              , 'ilp'          : os.path.join(root, 'experiments/ilpe')
              , 'ppr'          : os.path.join(root, 'experiments/ppr')
              , 'log-regress'  : os.path.join(root, 'experiments/log_reg')
              , 'elastic-net'  : os.path.join(root, 'experiments/elastic_net')
              , 'pagerank'     : os.path.join(root, 'experiments/pagerank')
              , 'affective'    : os.path.join(root, 'experiments/affective')

        },                   

    }

############################################################
'''
  directory logic
'''
def setup(PATH):

    os.system('clear')

    log_dir = PATH['critical-directories']['log']

    if not os.path.exists(log_dir):
      os.mkdir(log_dir)

    writer = Writer(log_dir)
    writer.tell('Initializing application [ learn-adj-relation ] ...')

    for _,path in PATH['critical-directories'].iteritems():
        if not os.path.exists(path):
            writer.tell('making directory at ' + path)
            os.mkdir(path)
        else:
            writer.tell('directory ' + path + ' already exists')

    for _,path in PATH['small-inputs'].iteritems():

        name = path.split('/')[-1]

        if not os.path.exists(path):
            writer.tell('Fatal Error: critical asset ' + name + ' not found at ' + path)
            raise NameError('Error: path not found: ' + path)
        else:
            writer.tell('Located critical asset ' + name + ' at ' + path)

    writer.tell('complete application setup!')

'''
  @Use: given name path or directory, locate full path 
'''
def get_path(path):
  for _,dirs in PATH.iteritems():
    if path in dirs: return dirs[path]
  else:
    return ''

'''
  @Use: given name of working directory, and list of subdirectories,
        if sub-directories do not exist, then make them
        else output path
'''
def working_dirs(dir_name, subdirs):

  code_dir = os.path.join(PATH['critical-directories']['deploy-code'],dir_name)
 
  dirs = { d : os.path.join(code_dir,d) for d in subdirs }

  for _,path in dirs.iteritems():
    if not os.path.exists(path):
      os.mkdir(path)

  dirs['work']    = code_dir
  dirs['log']     = PATH['critical-directories']['log']
 
  return dirs

def result_dirs(dir_name, subdirs):

  code_dir = os.path.join(PATH['critical-directories']['results'],dir_name)
 
  dirs = { d : os.path.join(code_dir,d) for d in subdirs }

  for _,path in dirs.iteritems():
    if not os.path.exists(path):
      os.mkdir(path)

  dirs['work']    = code_dir
  dirs['log']     = PATH['critical-directories']['log']
 
  return dirs

'''
  @Use: given name of data directory, and list of subdirectories,
        if sub-directories do not exist, then make them
        else output path
'''
def data_dirs(dir_name, subdirs):

  data_dir = os.path.join(PATH['critical-directories']['deploy-data'], dir_name)

  if not os.path.exists(data_dir):
    os.mkdir(data_dir)

  dirs = { d : os.path.join(data_dir,d) for d in subdirs }

  for _,path in dirs.iteritems():
    if not os.path.exists(path):
      os.mkdir(path)

  dirs['root']   = data_dir
  dirs['log']    = PATH['critical-directories']['log']

  return dirs

'''
  @Use: given absolute path `root` to directory
        make all subdirs if not refresh
        else grab the subdirs if the exists
'''
def locate_dirs(root, subdirs, rewrite = False):

  print('\n>> finding or making directories')
  
  if not os.path.exists(root):

    print('\n>> making root directory at ' + root)
    os.mkdir(root)

  elif rewrite:

    print('\n>> removing and remaking root directory at ' + root)

    shutil.rmtree(root)
    os.mkdir(root)

    print('\n>> adding init file')
    with open(os.path.join(root,'__init__.py'),'wb') as h:
      h.write('# auto generated init file')

  else:
    print('\n>> root directory already exists')

  paths = dict()

  for subdir in subdirs:
    path = os.path.join(root, subdir)
    if os.path.exists(path):
      print('\n>> sub-directory already exists at root/' + subdir)
      paths[subdir] = path
    else:
      print('\n>> making sub-directory at root/' + subdir)
      os.mkdir(path)

  paths['root'] = root
  return paths



 
############################################################
'''
  setup
'''

setup(PATH)


