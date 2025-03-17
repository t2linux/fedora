#!/usr/bin/bash
set -ex

KERNEL_VERSION=6.13.6-200.fc41 

cd "$sourcedir"
koji download-build --quiet --arch=src "kernel-$KERNEL_VERSION"
rpmdev-extract -q "kernel-$KERNEL_VERSION.src.rpm"
mv -n "kernel-$KERNEL_VERSION.src"/* .
rm -r "kernel-$KERNEL_VERSION.src.rpm" "kernel-$KERNEL_VERSION.src"

# Set buildid to .t2
sed -i 's/# define buildid .local/%define buildid .t2/g' "kernel.spec"

# Bump release
sed -i 's/%define specrelease 200/%define specrelease 210/g' "kernel.spec"

# Disable debug kernels
sed -i "/%define with_debug /c %define with_debug 0" "kernel.spec"

# Disable debuginfo
sed -i "/%define with_debuginfo /c %define with_debuginfo 0" "kernel.spec"

# Add our patches
sed -i "/Patch1:/a Patch2: t2linux-combined.patch" "kernel.spec"
sed -i "/ApplyOptionalPatch patch-%{patchversion}-redhat.patch/a ApplyOptionalPatch t2linux-combined.patch" "kernel.spec"

cat "linux-t2-patches/extra_config" > "kernel-local"

function apply_kconfig {
  kconfig="kernel-x86_64-fedora.config"
  config_opt=$(echo "$1" | cut -d'=' -f1)
  sed -i "/# $config_opt is not set/d" "$kconfig"
  sed -i "/$config_opt=/d" "$kconfig"
  echo "$1" >> "$kconfig"
}

apply_kconfig 'CONFIG_MODULE_FORCE_UNLOAD=y'
apply_kconfig 'CONFIG_CMDLINE="intel_iommu=on iommu=pt mem_sleep=s2idle pcie_ports=native"'
apply_kconfig 'CONFIG_CMDLINE_BOOL=y'
echo "# CONFIG_CMDLINE_OVERRIDE is not set" >> kernel-x86_64-fedora.config

cat "linux-t2-patches"/*.patch > "t2linux-combined.patch"
