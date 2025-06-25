#!/usr/bin/bash
set -e

KERNEL_VERSION=6.15.3-200.fc42

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
cat << 'EOF' > "kernel-local"
CONFIG_SPI_HID_APPLE_OF=y
CONFIG_HID_DOCKCHANNEL=y
CONFIG_APPLE_DOCKCHANNEL=y
CONFIG_APPLE_RTKIT_HELPER=m
CONFIG_DRM_APPLETBDRM=m
CONFIG_HID_APPLETB_BL=m
CONFIG_HID_APPLETB_KBD=m
CONFIG_APFS_FS=y
CONFIG_INPUT_SPARSEKMAP=y
EOF

function write_kconfig_to_file {
  config_opt=$(echo "$1" | cut -d'=' -f1)
  if [[ "$config_opt" =~ '# '(.+)' is not set' ]]; then
    config_opt="${BASH_REMATCH[1]}"
  fi
  sed -i "/# $config_opt is not set/d" "$2"
  sed -i "/$config_opt=/d" "$2"
  echo "$1" >> "$2"
}

function set_kconfig_x86_64 {
  for file in \
    "kernel-x86_64-fedora.config" \
    "kernel-x86_64-rt-debug-fedora.config" \
    "kernel-x86_64-rt-fedora.config" \
    "kernel-x86_64-debug-fedora.config"
  do
    write_kconfig_to_file "$1" "$file"
  done
}

set_kconfig_x86_64 'CONFIG_APPLE_BCE=m'
set_kconfig_x86_64 'CONFIG_MODULE_FORCE_UNLOAD=y'
set_kconfig_x86_64 'CONFIG_CMDLINE="intel_iommu=on iommu=pt mem_sleep=s2idle pcie_ports=native"'
set_kconfig_x86_64 'CONFIG_CMDLINE_BOOL=y'
set_kconfig_x86_64 '# CONFIG_CMDLINE_OVERRIDE is not set'

cat "linux-t2-patches"/*.patch > "t2linux-combined.patch"
