############################################################
# Module  : Bansal paper milp
# Date    : December 10th
# Author  : Xiao Ling
############################################################

from pulp    import *
from prelude import * 
from utils   import *
from server  import * 
from client  import * 
from app     import * 
from nltk.corpus import wordnet as wn


############################################################
# All

def milp(app):

  two       = app.TwoSided
  ranking   = [milp_no_syn(gold,app) for _,_,gold in two.test()]

  taus      = [r['tau']             for r in ranking]
  taus2     = [r['tau-notie']       for r in ranking]
  taus_max  = [r['tau-max']         for r in ranking]
  taus2_max = [r['tau-notie-max']   for r in ranking]
  pairs     = [r['pairwise']        for r in ranking]

  avg_tau      = sum(taus)                  / sum(taus_max)
  avg_abs_tau  = sum(abs(t) for t in taus)  / sum(abs(t) for t in taus_max)
  avg_tau2     = sum(taus2)                 / sum(taus2_max)
  avg_abs_tau2 = sum(abs(t) for t in taus2) / sum(abs(t) for t in taus_max)
  avg_pair     = sum(pairs)                 / len(pairs)


  avg_tau_max     = sum(taus_max)                 / len(taus_max)
  avg_abs_tau_max = sum(abs(t) for t in taus_max) / len(taus_max)
  avg_tau2_max    = sum(taus2_max)                 / len(taus_max)
  avg_abs_tau2_max= sum(abs(t) for t in taus2_max) / len(taus_max)

  return {'ranking' : ranking
         ,'pattern' : two.pattern()
         ,'average' : {'tau'                 : avg_tau
                      ,'tau-notie'           : avg_tau2
                      ,'absolute-tau'        : avg_abs_tau
                      ,'absolute-tau-no-tie' : avg_abs_tau2
                      ,'pair-wise'           : avg_pair 
                      # 
                      ,'regret-tau'          : avg_tau_max
                      ,'regret-|tau|'        : avg_tau_max
                      ,'regret-tau-no-tie'   : avg_tau_max
                      ,'regret-|tau|-no-tie' : avg_tau_max
                      }  
         }

############################################################
# rank each cluster

'''
  @Use: Given gold standard and server,
        output algo ranking
        no synonyms considered
'''
def milp_no_syn(gold, app):

  print ('ranking words ' + str(gold))

  words      = join(gold)

  for k in range(0,10): shuffle(words)

  pairs      = [u + '=' + v for u in words for v in words if u != v]
  (scores,C) = to_score(pairs,app)

  no_data = all(v == 0 for v in [scores[k] for k in scores])


  '''
    If absolutely no data for any pairs of words, output ties
    If there is any data at all, run Bansal' method
  '''
  if no_data: algo = [words]
  else      : algo = bansal_milp(words,pairs,scores,C)

  return {'gold'           : gold
          ,'algo'          : algo
          ,'tau'           : tau (gold,algo)
          ,'tau-max'       : tau (gold,gold)   # need this since max tau not necessarily 1.0
          ,'tau-notie'     : tau2(gold,algo)
          ,'tau-notie-max' : tau2(gold,gold)
          ,'pairwise'      : pairwise_accuracy(gold,algo)
          ,'raw-score'     : scores
          ,'raw-stat'      : dict()}

'''
  Banasl's Milp method
'''
def bansal_milp(words,pairs,scores,C):

  '''
    initialize problem
  '''  
  prob = LpProblem('-'.join(words), LpMaximize)

  '''
    initialize variables
  '''  
  x = dict()     # real value of each x_i on [0,1]
  d = dict()     # real value of distance between every x_i, x_j, i != j
  w = dict()     # integral value where w_ij => i < j
  s = dict()     # integral value where s_ij => i > j

  for uv in pairs:
    w[uv] = LpVariable('w_' + uv, 0, 1, LpInteger   )
    s[uv] = LpVariable('s_' + uv, 0, 1, LpInteger   )
    d[uv] = LpVariable('d_' + uv, 0, 1, LpContinuous)

  for u in words:
    x[u] = LpVariable('x_' + u, 0, 1, LpContinuous) 


  '''
    objective function
  '''
  objective = [ (w[ij] - s[ij]) * scores[ij] \
                for ij in pairs ]

  prob += lpSum(objective)

  '''
    constraints
  '''
  # d_ij = x_j - x_i
  for ij in pairs:
    [i,j] = ij.split('=')
    prob += x[j] - x[i] == d[ij]

  # d_ij - w_ij * C <= 0
  for ij in pairs:
    prob += d[ij] - w[ij] * C <= 0

  # d_ij + (1 - w_ij) * C > 0
  for ij in pairs:
    prob += d[ij] + (1 - w[ij]) * C >= 0

  # d_ij + s_ij * C >= 0
  for ij in pairs:
    prob += d[ij] + s[ij] * C >= 0

  # d_ij - (1 - sij) * C < 0
  for ij in pairs:
    prob += d[ij] - (1 - s[ij]) * C <= 0

  '''
    solve and interpret data
  '''

  prob.solve()

  algo = prob_to_algo_rank(prob,words)

  return algo  


############################################################
# scores

def is_synonym(u,v):
  u_syns = join([x.lemma_names() for x in wn.synsets(u)])
  v_syns = join([x.lemma_names() for x in wn.synsets(v)])
  return u in v_syns or v in u_syns


'''
  @Use: given list of form ['word1-word2', ...]
        output dictonary mapping 'word1-word2' to
        their score, and the normalization constant

  to_score :: [String] -> App -> (Dict String Float, Float)
'''
def to_score(pairs,app):

  one    = app.OneSided
  two    = app.TwoSided
  scores = dict()

  # compute scores
  for uv in pairs:

    [u,v] = uv.split('=')
    s     = paper_score(u,v,two)
    scores[uv] = s 


  rescale = [abs(scores[uv]) for uv in scores \
            if abs(scores[uv]) != 0]
  
  if rescale: rescale = min(rescale)
  else:       rescale = 1.0

  # normalize scores
  for uv,s in scores.items(): scores[uv] = s/rescale

  C  = sum(abs(scores[uv]) for uv in scores) * 1000

  return (scores, C)


# paper score
def paper_score(ai,ak,two):
  w1  = W1(two,ai,ak)
  w2  = W2(two,ai,ak)
  s1  = S1(two,ai,ak)
  s2  = S1(two,ai,ak)
  d   = two.data(ai,ak)
  nai = d[ai] + 1
  nak = d[ak] + 1
  return ((w1 - s1) - (w2 - s2))/(nai * nak)


def W1(two,ai,ak):
  P_ws = sum(n for _,n in two.data(ai,ak)['weak-strong']) + 1e-10
  P1   = two.norm()['weak-strong'] + 1e-10
  return P_ws/P1


def S1(two,ai,ak):
  P_sw = sum(n for _,n in two.data(ai,ak)['strong-weak']) + 1e-10
  P2   = two.norm()['strong-weak'] + 1e-10
  return P_sw/P2


def W2(two,ai,ak):
  return W1(two,ak,ai)

def S2(two,ai,ak):
  return S1(two,ak,ai)



def milp_syn(gold,app):

  words      = join(gold)
  pairs      = [u + '-' + v for u in words for v in words if u != v]
  (scores,C) = to_score(pairs,app)

  # build synonym set
  synonyms   = [(u,v) for [u,v] in [x.split('=') for x in pairs] \
               if is_synonym(u,v)]
  '''
    initialize problem
  '''  
  prob = LpProblem('-'.join(words), LpMaximize)


  '''
    initialize variables
  '''  
  x = dict()     # real value of each x_i on [0,1]
  d = dict()     # real value of distance between every x_i, x_j, i != j
  w = dict()     # integral value where w_ij => i < j
  s = dict()     # integral value where s_ij => i > j

  for uv in pairs:
    w[uv] = LpVariable('w_' + uv, 0, 1, LpInteger   )
    s[uv] = LpVariable('s_' + uv, 0, 1, LpInteger   )
    d[uv] = LpVariable('d_' + uv, 0, 1, LpContinuous)

  for u in words:
    x[u] = LpVariable('x_' + u, 0, 1, LpContinuous) 

  '''
    non-synonym and snynonym pairs
  '''  

  syn_pairs     = [u + '-' + v for u,v in synonyms]
  non_syn_pairs = [uv for uv in pairs if uv not in syn_pairs]

  print ('=== ', syn_pairs)  


  '''
  objective function
  '''
  objective = [ (w[ij] - s[ij]) * scores[ij] \
              for ij in non_syn_pairs      ] \
            + [ -1 * C * (w[ij] + s[ij]) for ij in syn_pairs]

  prob += lpSum(objective)


  '''
    constraints
  '''
  # d_ij = x_j - x_i
  for ij in pairs:
    [i,j] = ij.split('=')
    prob += x[j] - x[i] == d[ij]

  # d_ij - w_ij * C <= 0
  for ij in pairs:
    prob += d[ij] - w[ij] * C <= 0

  # d_ij + (1 - w_ij) * C > 0
  for ij in pairs:
    prob += d[ij] + (1 - w[ij]) * C >= 0

  # d_ij + s_ij * C >= 0
  for ij in pairs:
    prob += d[ij] + s[ij] * C >= 0

  # d_ij - (1 - sij) * C < 0
  for ij in pairs:
    prob += d[ij] - (1 - s[ij]) * C <= 0


  '''
    solve and interpret data
  ''' 

  prob.solve()


  algo = prob_to_algo_rank(prob,words)

  return {'gold'            : gold
        ,'algo'          : algo
        ,'tau'           : tau (gold,algo)
        ,'tau-max'       : tau (gold,gold)   # need this since max tau not necessarily 1.0
        ,'tau-notie'     : tau2(gold,algo)
        ,'tau-notie-max' : tau2(gold,gold)
        ,'pairwise'      : pairwise_accuracy(gold,algo)
        ,'raw-score'     : scores
        ,'raw-stat'      : dict()
        }







