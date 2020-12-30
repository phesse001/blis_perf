#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Flavio Vella, flavio@dividiti.com
# OSX port:  Leo Gordon, leo@dividiti.com
#

import os

##############################################################################
# get version from path

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
    cus=i.get('customize',{})
    full_path=cus.get('full_path','')

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    # Check platform
    tplat=hosd.get('ck_name','')

    env=i['env']


    # Looking for the parent of the 'include' dir that contains our include_file:
    #
    lib_parent_dir = os.path.dirname(os.path.realpath(full_path))
    #get perm path that won't manipulate
    path_lib = lib_parent_dir 
    print("lib dir is " + lib_parent_dir)
    #if cloned from github and configured, there will be an intermediate directory with the name of the arc
    #if library was installed alone to be linked against the library resides in */blis/lib rather than */blis/lib/arc
    if os.path.basename(lib_parent_dir) != 'lib':
      cus['arc_specific'] = 'no'
      cus['arc'] = ''
    else:
      cus['arc_specific'] = 'yes'
      cus['arc'] = str(os.path.basename(lib_parent_dir))

    include_file_name=cus.get('include_file','')

    found = False
    while found == False:
      print(lib_parent_dir)
      if os.path.isdir(os.path.join(os.path.dirname(lib_parent_dir),"include")):
        if(cus['arc_specific'] == 'yes'):
          include_path = os.path.join(os.path.dirname(lib_parent_dir),"include", cus['arc'])
          found = True
          break
        else:
          include_path = os.path.join(os.path.dirname(lib_parent_dir),"include", 'blis')
          found = True
          break
      #go up a directory
      lib_parent_dir = os.path.dirname(lib_parent_dir)
      if os.path.basename(lib_parent_dir) == "":
        return {'return':1, 'error':'can\'t find include file... select installation with include file in \'include\' sub directory'}


    file_extensions     = hosd.get('file_extensions',{})    # not clear whether hosd or tosd should be used in soft detection
    file_root_name     = os.path.basename(full_path).split(".")[0]
    cus['path_lib']     = path_lib
    cus['static_lib']   = file_root_name + file_extensions.get('lib','')
    cus['dynamic_lib']  = file_root_name + file_extensions.get('dll','')
    cus['path_include'] = include_path
    cus['include_name'] = include_file_name

    r = ck.access({'action': 'lib_path_export_script', 'module_uoa': 'os', 'host_os_dict': hosd, 'lib_path': path_lib})
    if r['return']>0: return r
    shell_setup_script_contents = r['script']

    env_prefix          = cus.get('env_prefix','')
    install_root        = include_path    # or should lib_parent_dir be used instead? Not clear.
    env[env_prefix]     = install_root

    path_bin=os.path.join(install_root,'bin')
    if os.path.isdir(path_bin):
       env[env_prefix+'_BIN']=path_bin
       cus['path_bin']=path_bin
       if tplat=='win':
          shell_setup_script_contents += '\nset PATH='+path_bin+';%PATH%\n\n'

    env[env_prefix+'_INCLUDE_NAME'] = cus.get('include_name','')
    env[env_prefix+'_STATIC_NAME']  = cus.get('static_lib','')
    env[env_prefix+'_DYNAMIC_NAME'] = cus.get('dynamic_lib','')

    return {'return':0, 'bat':shell_setup_script_contents}

