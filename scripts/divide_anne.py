############################################################
# Module  : divide anne's clusters
# Date    : December 22nd
# Author  : Xiao Ling
############################################################

from app     import *
from utils   import *
from scripts import *

############################################################
'''
	read set
'''
big   = read_gold(get_path('anne-125'))
small = read_gold(get_path('anne-25' ))
both  = chunks(big + small,3)


out_dir = os.path.join(get_path('data-root'), 'inputs/test/anne')

if True:

	cnt = 1

	for golds in both:
		out = os.path.join(out_dir, 'cluster-' + str(cnt) + '.txt')
		cluster = {k:gold for k,gold in enumerate(golds)}
		write_gold(out, cluster)
		cnt += 1




