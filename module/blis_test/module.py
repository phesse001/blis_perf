#
# Collective Knowledge (Allows compilation with cmake)
#
# 
# 
#
# Developer: 
#

cfg={}  # Will be updated by CK (meta description of this module)
work={} # Will be updated by CK (temporal data)
ck=None # Will be updated by CK (initialized CK kernel) 

import os
import ck.kernel as ck
from pathlib import Path

# Local settings

##############################################################################
# Initialize module

def init(i):
    """

    Input:  {}

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """
    return {'return':0}

##############################################################################
# test

def test(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """
    duoa = i.get('data_uoa','')
    if duoa == '':
      print('Please provide data entry (ex. ck compile blis_test:make)')
      ck.err(i)

    muoa = i.get('module_uoa', '')

    r=ck.access({'action':'load', 'module_uoa': muoa, 'data_uoa': duoa})
    if r['return']>0: return r # use standard error handling in the CK

    path = r['path']
    '''
    ops = ['gemv','ger','hemv','her','her2','trmv','trsv','gemm','hemm','herk','her2k','trmm','trsm']
    
    for op in ops:
      i = {'repo_uoa':'ck-blis', 'module_uoa':'results', 'data_uoa':op + '_results', 'data_name':op, 'tags': [op + '_test']}
      r = ck.add(i)
      #don't return r in this case - this just lets the user know that the entry already exists
      if r['return']>0:  print(r['error'])
    '''
    '''
    calling runme here because the current bach process will have all of the vars it needs (otherwise have to call source for intel compiler vars)
    '''
    shell_cmd = 'cd ' + path + ' && make && runme.sh'
    i = {'action':'virtual', 'module_uoa':'env',
         'tag_groups':'compiler,lang-cpp openblas mkl,lp64 mkl,core mkl,sequential lib,pthread lib,blis', 
         'shell_cmd': shell_cmd, 'verbose':'yes'}

    r=ck.access(i)
    if r['return']>0: return r # use standard error handling in the CK

    return {'return':0}

