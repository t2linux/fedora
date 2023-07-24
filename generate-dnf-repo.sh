#!/usr/bin/bash

cd /repo
mkdir ./dnf-repo && cd ./dnf-repo
cp /repo/_output/*.rpm .
rm *.src.rpm
createrepo .
