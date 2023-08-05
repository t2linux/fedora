#!/usr/bin/bash
source /repo/util.sh

FEDORA_KERNEL_VERSION=6.4.7-200.fc38
PATCHES_COMMIT=c908e506346681139a844d41c40b295cfad17ea8

cd /repo/kernel
download_koji_sources kernel-${FEDORA_KERNEL_VERSION}

# Fedora devs are against merging kernel-local for all architectures when keys are not properly specified, so we have to patch it in.
sed -i "s@for i in %{all_arch_configs}@for i in *.config@g" kernel.spec 

# Set buildid to .t2
sed -i 's/# define buildid .local/%define buildid .t2/g' kernel.spec

# Disable debug kernels
sed -i "/%define with_debug /c %define with_debug 0" kernel.spec

git clone --quiet --single-branch --branch main https://github.com/t2linux/linux-t2-patches patches && cd patches
git checkout ${PATCHES_COMMIT}
cd ..

cat patches/extra_config > kernel-local
cat patches/*.patch > linux-kernel-test.patch
