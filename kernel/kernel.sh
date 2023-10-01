#!/usr/bin/bash
FEDORA_KERNEL_VERSION=6.5.5-200.fc38
cd /repo/kernel
koji download-build --quiet --arch=src "kernel-${FEDORA_KERNEL_VERSION}"
rpmdev-extract -q "kernel-${FEDORA_KERNEL_VERSION}".src.rpm
mv -n "kernel-${FEDORA_KERNEL_VERSION}".src/* .

# Fedora devs are against merging kernel-local for all architectures when keys are not properly specified, so we have to patch it in.
sed -i "s@for i in %{all_arch_configs}@for i in *.config@g" kernel.spec 

# Set buildid to .t2
sed -i 's/# define buildid .local/%define buildid .t2/g' kernel.spec

# Disable debug kernels
sed -i "/%define with_debug /c %define with_debug 0" kernel.spec

cat linux-t2-patches/extra_config > kernel-local
cat linux-t2-patches/*.patch > linux-kernel-test.patch

cd ..
