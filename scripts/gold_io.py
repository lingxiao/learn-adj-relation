############################################################
# Module  : Read and write Gold IO scripts
# Date    : December 22nd
# Author  : Xiao Ling
# ############################################################

import os
import datetime

############################################################
'''
	@Use: read gold test set
'''
def read_gold(path):
  gold = open(path,'r').read().split('===')[1:-1]
  gold = [rs.split('\n') for rs in gold if rs.split('\n')]
  gold = [rs[1:-1] for rs in gold]
  gold = [[r.split(', ') for r in val] for val in gold]
  return gold

'''
  @Use: write gold test so that
        read_gold(p) == (write_gold q golds >>=\q -> read_gold(q))
'''
def write_gold(path, golds):
  with open(path, 'wb') as h:
    for k,gold in golds.iteritems():
      h.write('=== ' + str(k) + '\n')
      for ws in gold:
        h.write(', '.join(ws) + '\n')
    h.write('=== END')
    h.close()
    return path










