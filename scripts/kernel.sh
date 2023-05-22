#!/bin/bash

FEDORA_KERNEL_VERSION=6.3.3-200.fc38
PATCHES_GIT=https://github.com/t2linux/linux-t2-patches
PATCHES_COMMIT=d0e70c9396db0c97b47155a649838bb7ba82a690

echo "=====INSTALLING DEPENDENCIES====="
dnf install -y --quiet ncurses-devel libbpf fedpkg ccache openssl-devel libkcapi libkcapi-devel libkcapi-static libkcapi-tools

cd "/root/rpmbuild"/SPECS

echo "=====DOWNLOADING SOURCES====="
mkdir -p /tmp/extract-kernel
cd /tmp/extract-kernel
koji download-build --arch=src kernel-${FEDORA_KERNEL_VERSION}

echo "=====EXTRACTING SOURCES====="
rpmdev-extract kernel-${FEDORA_KERNEL_VERSION}.src.rpm
mkdir -p /kernel-build
mv -n kernel-*.src/* /kernel-build

echo "=====PREPARING SOURCES===="
cd /kernel-build
# Fedora devs are against merging kernel-local for all architectures when keys are not properly specified, so we have to patch it in.
sed -i "s@for i in %{all_arch_configs}@for i in *.config@g" kernel.spec 
sed -i 's/# define buildid .local/%define buildid .t2/g' kernel.spec
# sed -i 's/%define specrelease 200%{?buildid}%{?dist}/%define specrelease 202%{?buildid}%{?dist}/' kernel.spec
# sed -i 's/%define pkgrelease 200/%define pkgrelease 202/' kernel.spec

echo "======DOWNLOADING PATCHES====="
rm -rf /tmp/download /tmp/src
mkdir /tmp/download && cd /tmp/download 
git clone --single-branch --branch main ${PATCHES_GIT}
cd *
git checkout ${PATCHES_COMMIT}

cd /kernel-build
cat /tmp/download/*/extra_config > kernel-local
cat /tmp/download/*/*.patch > linux-kernel-test.patch

echo "=====BUILDING====="
cd /kernel-build
mock --buildsrpm --spec ./kernel.spec --sources . --resultdir ./_mock
mock --rebuild ./_mock/*.src.rpm --resultdir ./_mock
cp ./_mock/*.rpm /output