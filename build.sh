#!/bin/bash

FEDORA_KERNEL_VERSION=5.18.6-200.fc36
PATCHES_GIT=https://github.com/AdityaGarg8/linux-t2-patches
PATCHES_COMMIT=5de541ee8cd4d8cf54a25d35c9eb95c6fca0603e

# Dependencies
dnf install -y fedora-packager git curl pesign ncurses-devel libkcapi libkcapi-devel libkcapi-static libkcapi-tools libbpf fedpkg rpmdevtools dwarves

# Set home build directory
rpmdev-setuptree

# Get kernel source and install dependencies
cd /root/rpmbuild/SOURCES
koji download-build --arch=src kernel-${FEDORA_KERNEL_VERSION}
rpm -Uvh kernel-${FEDORA_KERNEL_VERSION}.src.rpm
cd /root/rpmbuild/SPECS 
dnf -y builddep kernel.spec

# Download patches
mkdir /tmp/download && cd /tmp/download 
git clone --single-branch --branch main ${PATCHES_GIT}
cd *
git checkout ${PATCHES_COMMIT}
for f in *.patch; do mv "$f" "$f.t2"; done
cp *.patch.t2 /root/rpmbuild/SOURCES/

# Apply patches
cd /root/rpmbuild/SPECS
echo "CONFIG_APPLE_BCE=m" >> "/root/rpmbuild/SOURCES/kernel-local"
echo "CONFIG_APPLE_IBRIDGE=m" >> "/root/rpmbuild/SOURCES/kernel-local"
sed -i "s/# define buildid.*/%define buildid .t2/" "/root/rpmbuild"/SPECS/kernel.spec

for i in /root/rpmbuild/SOURCES/*.patch.t2; do
    PATCH_ID=$(($(grep ^Patch "/root/rpmbuild/SPECS/kernel.spec" | tail -n2 | head -n1 | awk '{ print $1 }' | sed s/Patch// | sed s/://) + 1 ))
    sed -i "s@# END OF PATCH DEFINITIONS@Patch$PATCH_ID: $i\n\n# END OF PATCH DEFINITIONS@g" /root/rpmbuild/SPECS/kernel.spec
done;

# Build non-debug rpms
cd "/root/rpmbuild"/SPECS
rpmbuild -bb --with baseonly --without debug --without debuginfo --target=x86_64 kernel.spec

# Copy artifacts to shared volume
cd "/repo"
mkdir -p ./output
mkdir -p ./output/RPMS
cp -rfv /root/rpmbuild/RPMS/* ./output/RPMS/
