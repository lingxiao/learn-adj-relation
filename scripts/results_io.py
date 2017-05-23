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

'''
  save as text and pickle file
'''
def save_results(results, out_path, algo_only = False):

  if algo_only: 
    save_algo_results(results, out_path)
  else:
    save_all_results (results, out_path)

def save_all_results(results, out_path):

  demark = '------------------------------------------------\n'

  pickle_path = out_path.replace('.txt', '.pkl')  

  with open(pickle_path,'wb') as h:
    pickle.dump(results,h)

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
          raw_probs = rank['raw']
        elif type(rank['raw']) == dict:
          raw_probs = rank['raw'].iteritems()

        for key,val in raw_probs:
          if type(val) == list:
            f.write('\n' + key + ':\n')
            for v in val:
              f.write('\t' + str(v) + '\n')
          else:
            f.write(key + ':\t' + str(val))


        f.write('\n')

      f.write(demark)


    f.write('=== END')

def save_algo_results(results, out_path):

  demark = '------------------------------------------------\n'

  algos = [ {'algo': d['algo'], 'raw': d['raw']} for _,d in results['ranking'].iteritems() ]

  pickle_path = out_path.replace('.txt', '.pkl')  

  with open(pickle_path,'wb') as h:
    pickle.dump(algos,h)


  with open(out_path, 'wb') as f:

    name = out_path.split('/')[-1]
    f.write(name + '\n')
    f.write(str(datetime.datetime.now()) + '\n')

    for d in algos:

      algo = d['algo']
      raw  = d['raw']

      if type(raw) == list:
        raw_probs = raw
      elif type(raw) == dict:
        raw_probs = raw.iteritems()

      f.write(demark)

      f.write('=== algo: \n')      
      for w in algo:
        f.write(str(w) + '\n')
      f.write('\n')

      f.write('=== raw:\n')

      for key,val in raw_probs:
        if type(val) == list:
          f.write('\n' + key + ':\n')
          for v in val:
            f.write('\t' + str(v) + '\n')
        else:
          f.write(key + ':\t' + str(val))



      f.write('\n')

    f.write(demark)
    f.write('=== END')

############################################################
'''
  @Use: given path to gold directory 
      read ranking over all gold set
  @Input - results_dir :: String
  @output: Dict String _
'''
def read_results(results_dir):

  paths  = [os.path.join(results_dir, p) for p in os.listdir(results_dir) if 'pkl' in p]

  report = dict()

  incr = 1

  for path in paths:
    with open(path,'rb') as h:
      o = pickle.load(h)
      for _,ret in o['ranking'].iteritems():
        report[incr] = ret
        incr += 1 

  print('\n\t>> computing averages')
  avg_pair    = sum(d['pairwise'] for _,d in report.iteritems())
  avg_tau     = sum(d['tau']      for _,d in report.iteritems())
  avg_abs_tau = sum(d['|tau|']    for _,d in report.iteritems())

  out = dict()
  out['pairwise'] = avg_pair/len(report)
  out['tau']      = avg_tau /len(report)
  out['|tau|']    = avg_abs_tau /len(report)
  out['ranking']  = report

  return out





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





