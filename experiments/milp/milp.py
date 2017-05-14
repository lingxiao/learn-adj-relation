############################################################
# Module  : Bansal paper milp
# Date    : December 10th
# Author  : Xiao Ling
############################################################


import os
import pickle
from pulp    import *
from scripts import *
from utils   import *


############################################################

'''
  @Use: rank using paper's milp 
'''
def paper_milp(ngram_dir, stat, count):

  def fn(gold):

    print('\n\t>> milping: ' + str(gold))

    words = join(gold)
    pairs = [ (s,t) for s in words for t in words if s != t ]


    '''
      compute score     
    '''  
    scores,C  = to_score( pairs
                      , paper_score(ngram_dir, stat, count)
                      )

    no_data = all(v == 0 for _,v in scores.iteritems() )

    if no_data:
      return [words], scores

    else:

      prob = LpProblem('-'.join(words), LpMaximize)

      '''
        initialize variables
      '''  
      X = dict()     # real value of each x_i on [0,1]
      D = dict()     # real value of distance between every x_i, x_j, i != j
      W = dict()     # integral value where w_ij => i < j
      S = dict()     # integral value where s_ij => i > j

      for s,t in pairs:
        st = s + '=' + t
        W[st] = LpVariable('w_' + st, 0, 1, LpInteger   )
        S[st] = LpVariable('s_' + st, 0, 1, LpInteger   )
        D[st] = LpVariable('d_' + st, 0, 1, LpContinuous)

      for s in words:
        X[s] = LpVariable('x_' + s, 0, 1, LpContinuous) 


      '''
        objective function
      '''
      objective = [ (W[s + '=' + t] - S[s + '=' + t]) * scores[(s,t)] \
                  for s,t in pairs ]

      prob += lpSum(objective)


      '''
        constraints
      '''
      # d_ij = x_j - x_i
      for i,j in pairs:
        prob += X[j] - X[i] == D[ i + '=' + j ]

      # d_ij - w_ij * C <= 0
      for i,j in pairs:
        prob += D[ i + '=' + j ] - W[ i + '=' + j ] * C <= 0

      # d_ij + (1 - w_ij) * C > 0
      for i,j in pairs:
        prob += D[ i + '=' + j ] + (1 - W[i + '=' + j]) * C >= 0

      # d_ij + s_ij * C >= 0
      for i,j in pairs:
        prob += D[ i + '=' + j ] + S[i + '=' + j] * C >= 0

      # d_ij - (1 - sij) * C < 0
      for i,j in pairs:
        prob += D[ i + '=' + j ] - (1 - S[i + '=' + j]) * C <= 0


      '''
        solve and interpret data
      '''
      prob.solve()

      algo = prob_to_algo_rank(prob,words)

      return algo, scores

  return fn

############################################################

'''
  @Use: compute scores
'''
def to_score(pairs, compute_score):

  scores = [ (s,t,compute_score(s,t)) for s,t in pairs ]

  no_data = all(v == 0 for _,_,v in scores)

  if no_data:
    scores = { (s,t): n for s,t,n in scores }
    return scores, 1000

  else:

    max_s  = min ( abs(n) for _,_,n in scores if n != 0 )

    scores = [ (s,t, n/max_s) for s,t,n in scores ]

    C = sum(abs(n) for _,_,n in scores ) * 1000
    scores = { (s,t): n for s,t,n in scores }

    return scores, C

'''
  @Use: parse file for s,t if it exists
      and output counts of W1, S1, W2, S2
'''
def get_scores(ngram_dir, stat, s,t):

  path = os.path.join(ngram_dir, s + '-' + t + '.pkl')

  if os.path.exists(path):

    with open(path,'rb') as h:
      data = pickle.load(h)

    s_sw_t =  s + '<strong-weak>' + t 
    t_ws_s =  t + '<weak-strong>' + s 
    t_sw_s =  t + '<strong-weak>' + s 
    s_ws_t =  s + '<weak-strong>' + t 

    S1 = sum( n for _,n in data[s_sw_t] )/stat['strong-weak']
    W1 = sum( n for _,n in data[s_ws_t] )/stat['weak-strong']
    S2 = sum( n for _,n in data[t_sw_s] )/stat['strong-weak']
    W2 = sum( n for _,n in data[t_ws_s] )/stat['weak-strong']

    return S1, W1, S2, W2

  else:
    return 0.0, 0.0, 0.0, 0.0

'''
  @Use: compute score 
'''
def paper_score(ngram_dir, stat, count):

  def fn(s,t):

    s1, w1, s2, w2 = get_scores(ngram_dir, stat, s, t)
    top = (w1 - s1) - (w2 - s2)
    bot = count[s] * count[t]

    return top/bot

  return fn

############################################################

'''
  @Use: given milp object, output ranking
        as list of lists

  prob_to_algo_rank :: MILP -> [[String]] -> [[String]]
'''  
def prob_to_algo_rank(prob,words):

  '''
    interpret score as ranking
  '''
  raw0 = [tuple(v.name.split('_'))                    
          for v in prob.variables() if v.varValue == 1.0]

  '''
    words of form wo-rd need to be taken care of
  # '''

  raw1 = []

  for t in raw0:

    if len(t) == 2: 

      (x,uv) = t
      [u,v]  = uv.split('=')
      raw1.append((x,u,v))

    elif len(t) == 3:

      (x,u,v) = t

      if '=' in u:
        [word1,word2a] = u.split('=')
        raw1.append((x, word1, word2a + '-' + v))
      elif '=' in v:
        [word1b,word2] = v.split('=')
        raw1.append((x, u + '-' + word1b, word2))

  # if we have s_ij and w_ij, then we have a contradiction
  contradiction = [(s,u,v)                  \
                  for (s,u,v) in raw1       \
                  for (w,u1,v1) in raw1     \
                  if s == 's' and w == 'w'  \
                  and u == u1 and v == v1]

  raw  = [(u,v) for (x,u,v) in raw1 if x == 's']

  # # construct graph :: dictionary for topological sort
  order = dict()        

  for s,w in raw:
    if s in order:
      order[s] += [w]
    else:
      order[s] = [w]

  # complete the sink in the dictonary
  for w in words:
    if w not in order: order[w] = []

  algo = [[w] for w in toposort(order)]


  return algo

