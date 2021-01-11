#! /bin/bash

#
# Installation script for PAPI
#
#

# PACKAGE_DIR
# INSTALL_DIR

cd ${INSTALL_DIR}/${PACKAGE_SUB_DIR}

############################################################
echo ""
echo "Configuring package ..."

./configure auto

if [ "${?}" != "0" ] ; then
  echo "Error: configure failed!"
  exit 1
fi

############################################################

############################################################
echo ""
echo "Building package ..."

#obscure way to set the path based on output of makefile
make ${CK_MAKE_BEFORE} -j ${CK_HOST_CPU_NUMBER_OF_PROCESSORS} ${CK_MAKE_EXTRA}
if [ "${?}" != "0" ] ; then
  echo "Error: build failed!"
  exit 1
fi

############################################################

return 0