#!/usr/bin/bash

cd /repo || exit 1
mkdir ./dnf-repo && cd ./dnf-repo || exit 2
cp /repo/_output/*.rpm .
rm ./*.src.rpm
createrepo .
