#!/usr/bin/bash
set -e

KERNEL_VERSION=6.5.11-300.fc39

cd "$package_builddir"
koji download-build --quiet --arch=src "kernel-$KERNEL_VERSION"
rpmdev-extract -q -C "$package_builddir" "kernel-$KERNEL_VERSION.src.rpm"
mv -n "kernel-$KERNEL_VERSION.src"/* .
rm -r "kernel-$KERNEL_VERSION.src.rpm" "kernel-$KERNEL_VERSION.src"

# Fedora devs are against merging kernel-local for all architectures when keys are not properly specified, so we have to patch it in.
sed -i "s@for i in %{all_arch_configs}@for i in *.config@g" "$package_builddir/kernel.spec"

# Set buildid to .t2
sed -i 's/# define buildid .local/%define buildid .t2/g' "$package_builddir/kernel.spec"

# Disable debug kernels
sed -i "/%define with_debug /c %define with_debug 0" "$package_builddir/kernel.spec"

cat "$package_builddir/linux-t2-patches/extra_config" > "$package_builddir/kernel-local"
cat "$package_builddir/linux-t2-patches"/*.patch > "$package_builddir/linux-kernel-test.patch"

cd ..
