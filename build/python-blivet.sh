#!/bin/bash

cd /root/rpmbuild/SPECS

echo "=====DOWNLOADING SOURCES====="
mkdir -p /tmp/extract-blivet
cd /root/rpmbuild/SOURCES
koji download-build --arch=src python-blivet-3.5.0-1.fc37

echo "=====EXTRACTING SOURCES====="
rpmdev-extract python-blivet-*.src.rpm
mv /repo/specs/python-blivet.spec /root/rpmbuild/SPECS/
cp -r python-blivet-*.src/* /root/rpmbuild/SOURCES/
cp /repo/sources/python-blivet/0002-add-t2-support-blivet.patch /root/rpmbuild/SOURCES/

echo "=====PREPARING SOURCES====="
cd /root/rpmbuild/SPECS 
dnf -y builddep python-blivet.spec

echo "=====BUILDING====="
cd /root/rpmbuild/SPECS
rpmbuild -bb ./python-blivet.spec
