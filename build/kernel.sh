#!/bin/bash

FEDORA_KERNEL_VERSION=6.1.13-200.fc37
PATCHES_GIT=https://github.com/t2linux/linux-t2-patches
PATCHES_COMMIT=e27261e64d9169c21046d0b1e59ce436c28de10b

echo "=====INSTALLING DEPENDENCIES====="
dnf install -y ncurses-devel libbpf fedpkg rpmdevtools ccache openssl-devel libkcapi libkcapi-devel libkcapi-static libkcapi-tools

cd "/root/rpmbuild"/SPECS

echo "=====DOWNLOADING SOURCES====="
mkdir -p /tmp/extract-kernel
cd /tmp/extract-kernel
koji download-build --arch=src kernel-${FEDORA_KERNEL_VERSION}

echo "=====EXTRACTING SOURCES====="
rpmdev-extract kernel-${FEDORA_KERNEL_VERSION}.src.rpm
mv kernel-*.src/kernel.spec /root/rpmbuild/SPECS/
cp -r kernel-*.src/* /root/rpmbuild/SOURCES/

echo "=====PREPARING SOURCES===="
cd /root/rpmbuild/SPECS 
# Fedora devs are against merging kernel-local for all architectures when keys are not properly specified, so we have to patch it in.
sed -i "s@for i in %{all_arch_configs}@for i in *.config@g" kernel.spec 
sed -i 's/# define buildid .local/%define buildid .t2/g' kernel.spec
# sed -i 's/%define specrelease 200%{?buildid}%{?dist}/%define specrelease 202%{?buildid}%{?dist}/' kernel.spec
# sed -i 's/%define pkgrelease 200/%define pkgrelease 202/' kernel.spec
dnf -y builddep kernel.spec

echo "======DOWNLOADING PATCHES====="
rm -rf /tmp/download /tmp/src
mkdir /tmp/download && cd /tmp/download 
git clone --single-branch --branch 6.1 ${PATCHES_GIT}
cd *
git checkout ${PATCHES_COMMIT}

cd ~/rpmbuild/SPECS
# cat /tmp/download/*/extra_config > /root/rpmbuild/SOURCES/kernel-local
cat /tmp/download/*/extra_config > /root/rpmbuild/SOURCES/kernel-local
cat /tmp/download/*/*.patch > /root/rpmbuild/SOURCES/linux-kernel-test.patch

echo "=====BUILDING====="
cd /root/rpmbuild/SPECS
rpmbuild -bb --target=x86_64 .//kernel.spec
