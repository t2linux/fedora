#!/bin/bash

FEDORA_KERNEL_VERSION=6.0.13-300.fc37
PATCHES_GIT=https://github.com/t2linux/linux-t2-patches
PATCHES_COMMIT=3a916b371ced596485ef0937b1de0a3fafb896b3

echo "=====INSTALLING DEPENDENCIES====="
dnf install -y fedpkg koji fedora-packager git curl pesign rpmdevtools rpm-sign

rpmdev-setuptree
cd "/root/rpmbuild"/SPECS

echo "=====DOWNLOADING SOURCES====="
cd /root/rpmbuild/SOURCES
koji download-build --arch=src python-blivet-3.5.0-1.fc37
rpm -Uvh python-blivet-3.5.0-1.fc37.src.rpm
cd /root/rpmbuild/SPECS 
dnf -y builddep python-blivet.spec

echo "=====PREPARING SOURCES====="
cd ~/rpmbuild/SPECS
cp /repo/0002-add-t2-support.patch /root/rpmbuild/SOURCES/0002-add-t2-support.patch
mv -f /repo/python-blivet.spec /repo/rpmbuild/SPECS/python-blivet.spec

echo "=====IMPORTING KEYS====="
gpg --import /repo/rpm_signing_key
rpm --import /repo/repo/t2linux-fedora-ci.pub
rm -rfv /repo/rpm_signing_key
echo -e "%_signature gpg\n%_gpg_name t2linux-fedora CI" > ~/.rpmmacros

echo "=====BUILDING====="
cd "/root/rpmbuild"/SPECS
cp /repo/*.spec .
cp /repo/repo/* /root/rpmbuild/SOURCES
rpmbuild -bb python-blivet.spec
rpm --addsign /root/rpmbuild/RPMS/x86_64/*.rpm


# Copy artifacts to shared volume
cd "/repo"
mkdir -p ./output
mkdir -p ./output/RPMS
cp -rfv /root/rpmbuild/RPMS/* ./output/RPMS/
