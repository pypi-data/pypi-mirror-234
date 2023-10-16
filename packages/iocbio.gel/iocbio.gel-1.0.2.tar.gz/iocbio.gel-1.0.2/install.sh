#!/usr/bin/env bash

#
# This script installs IOCBio gel program to python virtual environment iocbio-gel
#

set -e
RNAME=iocbio-gel_requirements.txt
python3 -m venv iocbio-gel
if command -v wget &> /dev/null
then
  wget -q -O $RNAME https://gitlab.com/iocbio/gel/-/raw/main/requirements.txt
else
  curl https://gitlab.com/iocbio/gel/-/raw/main/requirements.txt --output $RNAME
fi
iocbio-gel/bin/pip3 install -r $RNAME
rm $RNAME
# iocbio-gel/bin/pip3 install git+https://gitlab.com/iocbio/gel
iocbio-gel/bin/pip3 install iocbio.gel

echo Start the program by running iocbio-gel/bin/iocbio-gel
