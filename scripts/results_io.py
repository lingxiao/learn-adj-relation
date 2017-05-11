############################################################
# Module  : Results IO Scripts
# Date    : December 22nd
# Author  : Xiao Ling
# ############################################################

import os
import pickle
import datetime

from utils import *

############################################################

def save_ranking(results, out_path):

  print('\n>> saving ranking to ' + out_path)

  demark = '-'*50 + '\n'
  ranks  = results['ranking']

  with open(out_path, 'w') as f:

    f.write(name + '\n')
    f.write(str(datetime.datetime.now()) + '\n')
    f.write(demark)

    for _,rank in ranks.iteritems():
      for w in rank['algo']:
        f.write(', '.join(w) + '\n')
      f.write(demark)
    f.write('=== END')



'''
  save as text and pickle file
'''
def save_results(results, out_path):

  demark = '------------------------------------------------\n'

  # pkl,_ = out_path.split('.')
  # pkl   = pkl + '.pkl'

  # with open(pkl,'wb') as h:
  #   pickle.dump(results,h)

  ranking      = results['ranking']
  avg_taus     = results['tau']
  avg_abs_taus = results['|tau|']
  avg_pairwise = results['pairwise']

  with open(out_path,'w') as f:

    name = out_path.split('/')[-1]
    f.write(name + '\n')
    f.write(str(datetime.datetime.now()) + '\n')

    f.write(demark)
    f.write('average pairwise : ' + str(round(avg_pairwise*100)) + '%\n')
    f.write('average tau:  '      + str(round(avg_taus      ,2)) + '\n')
    f.write('average |tau|:'      + str(round(avg_abs_taus  ,2)) + '\n')
    f.write(demark)

    for _,rank in ranking.iteritems():
      
      f.write('=== tau:\n'               + str(rank['tau'])       + '\n\n')
      f.write('=== pairwise accuracy:\n' + str(rank['pairwise'])  + '\n\n')

      f.write('=== gold: \n')      
      for w in rank['gold']:
        f.write(str(w) + '\n')
      f.write('\n')

      f.write('=== algo: \n')      
      for w in rank['algo']:
        f.write(str(w) + '\n')
      f.write('\n')

      if 'raw' in rank:
        if type(rank['raw']) == list:
          raws = rank['raw']
        elif type(rank['raw']) == dict:
          raws = rank['raw'].iteritems()

        f.write('=== raw:\n')
        for raw in raws:
          f.write(str(raw) + '\n')

        f.write('\n')

      f.write(demark)


    f.write('=== END')








