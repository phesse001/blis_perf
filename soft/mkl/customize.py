#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
#

##############################################################################
# get version from path

import os

def version_cmd(i):

    ck=i['ck_kernel']

    full_path=i['full_path']
    fn=os.path.basename(full_path)

    rfp=os.path.realpath(full_path)
    rfn=os.path.basename(rfp)

    ver=''

    if rfn.startswith(fn):
       ver=rfn[len(fn)+1:]
       if ver!='':
          ver='api-'+ver

    return {'return':0, 'cmd':'', 'version':ver}

##############################################################################
# setup environment setup

def setup(i):
    """
    Input:  {
              cfg              - meta of this soft entry
              self_cfg         - meta of module soft
              ck_kernel        - import CK kernel module (to reuse functions)

              host_os_uoa      - host OS UOA
              host_os_uid      - host OS UID
              host_os_dict     - host OS meta
              
              target_os_uoa    - target OS UOA
              target_os_uid    - target OS UID
              target_os_dict   - target OS meta

              target_device_id - target device ID (if via ADB)

              tags             - list of tags used to search this entry

              env              - updated environment vars from meta
              customize        - updated customize vars from meta

              deps             - resolved dependencies for this soft

              interactive      - if 'yes', can ask questions, otherwise quiet
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              bat          - prepared string for bat file
            }

    """

    import os

    # Get variables
    ck=i['ck_kernel']
    s=''

    iv=i.get('interactive','')

    env=i.get('env',{})
    cfg=i.get('cfg',{})
    deps=i.get('deps',{})
    tags=i.get('tags',[])
    cus=i.get('customize',{})

    target_d=i.get('target_os_dict',{})
    win=target_d.get('windows_base','')
    remote=target_d.get('remote','')
    mingw=target_d.get('mingw','')
    tbits=target_d.get('bits','')

    envp=cus.get('env_prefix','')
    pi=cus.get('path_install','')

    host_d=i.get('host_os_dict',{})
    op_s = host_d['ck_name']
    sdirs=host_d.get('dir_sep','')

    fp=cus['full_path']
    lib_parent_dir = os.path.dirname(os.path.realpath(fp))
    #get perm path that won't manipulate
    path_lib = lib_parent_dir 

    ep=cus['env_prefix']
    env[ep]=fp

    ################################################################
    if win=='yes':
       if remote=='yes' or mingw=='yes': 
          sext='.a'
          dext='.so'
       else:
          sext='.lib'
          dext='.dll'
    else:
       sext='.a'
       dext='.so'

    cus['path_lib'] = path_lib
    file_root_name = cus.get('file_root_name')
    file_root_names = cus.get('file_root_names')
    env_prefix = cus.get('env_prefix','')

    if op_s == 'win':
      for name in file_root_names:
        cus['extra_static_libs'][name] = name

    r = ck.access({'action': 'lib_path_export_script', 'module_uoa': 'os', 'host_os_dict': host_d, 
      'lib_path': cus.get('path_lib', '')})
    if r['return']>0: return r
    s += r['script']

    cus['path_lib'] = path_lib

    if op_s == 'win':
      cus['static_lib']   = file_root_name + sext
      cus['dynamic_lib']  = file_root_name + dext
    elif op_s == 'linux':
      cus['static_lib']   = 'lib_' + file_root_name + sext
      cus['dynamic_lib']  = 'lib_' + file_root_name + dext


    if op_s == 'win':
      for fn in file_root_names:
        env['CK_EXTRA_LIB_'+fn.upper()] = "-l" + fn
        cus['extra_dynamic_libs'][fn] = "mkl_" + fn + dext
        cus['extra_static_libs'][fn] = "mkl_" + fn + sext

    elif op_s == 'linux':
      for fn in file_root_names:
        env['CK_EXTRA_LIB_'+fn.upper()] = "-lmkl_" + fn
        cus['extra_dynamic_libs'][fn] = "libmkl_" + fn + dext
        cus['extra_static_libs'][fn] = "libmkl_" + fn + sext


    env[env_prefix] = path_lib

    return {'return': 0, 'bat':s}
