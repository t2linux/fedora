#!/bin/bash

cd /root/rpmbuild/SPECS

echo "=====EXTRACTING SOURCES====="
mv /repo/t2linux-*.spec /root/rpmbuild/SPECS/
cp /repo/repo/* /root/rpmbuild/SOURCES

echo "=====PREPARING SOURCES====="
cd /root/rpmbuild/SPECS 
dnf -y builddep t2linux-*.spec

echo "=====BUILDING====="
cd /root/rpmbuild/SPECS
rpmbuild -bb ./t2linux-config.spec
rpmbuild -bb ./t2linux-repo.spec
