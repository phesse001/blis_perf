
import os
##############################################################################
#used to find path to specified file
def find_files(filename, search_path):
   result = []
   for root, dir, files in os.walk(search_path):
      if filename in files:
         result.append(os.path.join(root, filename))
   return result

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

    # Get variables
    env=i.get('env',{})
    deps=i.get('deps',{})
    tags=i.get('tags',[])
    cus=i.get('customize',{})
    tosd=i['target_os_dict']
    sep=tosd.get('dir_sep','')
    op_s = tosd.get('ck_name', '')

    fp=cus.get('full_path','')
    #for some reason filename isn't added to full path so we can just use the full path found without going up a dir
    cus['path_lib'] = fp
    
    #check that header file is there
    include_paths = find_files("blis.h",os.path.dirname(fp))
    if len(include_paths) > 0:
      pi = include_paths[0]
    else:
      return {'return':1, 'error':'can\'t find include file... select installation with include file in \'include\' sub directory'}

    #adding to cus for what program module looks for
    cus['path_include']=sep.join(pi.split(sep)[:-1])
    cus['dynamic_lib'] = cus['soft_file'][op_s]

    ep=cus.get('env_prefix','')
    if fp!='' and ep!='':
       env[ep]=fp
    #add extra lib path for linking to mingw
    lib = cus['dynamic_lib']
    env['CK_EXTRA_LIB_BLIS'] = "\"" + fp + sep + lib + "\""

    return {'return':0, 'bat': ''}
