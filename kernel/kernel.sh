#!/usr/bin/bash
FEDORA_KERNEL_VERSION=6.5.5-200.fc38
PATCHES_COMMIT=3aeff9385079f5f362a5447cdb9f4e2b48962c92

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

git clone --quiet --single-branch --branch main https://github.com/t2linux/linux-t2-patches patches && cd patches
git checkout --quiet ${PATCHES_COMMIT}
cd ..

cat patches/extra_config > kernel-local
cat patches/*.patch > linux-kernel-test.patch
