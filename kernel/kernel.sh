#!/usr/bin/bash

FEDORA_KERNEL_VERSION=6.3.8-200.fc38
PATCHES_GIT=https://github.com/t2linux/linux-t2-patches
PATCHES_COMMIT=13dee3659d1ef17c5ea588c8be629fe693045496

source /repo/util.sh

echo "=====INSTALLING DEPENDENCIES====="
dnf install -y --quiet ncurses-devel libbpf fedpkg ccache openssl-devel libkcapi libkcapi-devel libkcapi-static libkcapi-tools

mkdir -p /repo/kernel && cd /repo/kernel
download_koji_sources kernel-${FEDORA_KERNEL_VERSION}

echo "=====PREPARING SOURCES===="
# Fedora devs are against merging kernel-local for all architectures when keys are not properly specified, so we have to patch it in.
sed -i "s@for i in %{all_arch_configs}@for i in *.config@g" kernel.spec 
sed -i 's/# define buildid .local/%define buildid .t2/g' kernel.spec
# sed -i 's/%define specrelease 200%{?buildid}%{?dist}/%define specrelease 202%{?buildid}%{?dist}/' kernel.spec
# sed -i 's/%define pkgrelease 200/%define pkgrelease 202/' kernel.spec
sed -i "/%define with_debug /c %define with_debug 0" kernel.spec

echo "======DOWNLOADING PATCHES====="
rm -rf /tmp/download && mkdir /tmp/download && cd /tmp/download 
git clone --quiet --single-branch --branch main ${PATCHES_GIT}
cd *
git checkout ${PATCHES_COMMIT}

cd /repo/kernel
cat /tmp/download/*/extra_config > kernel-local
cat /tmp/download/*/*.patch > linux-kernel-test.patch
