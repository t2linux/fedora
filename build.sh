#!/bin/bash
set -eu -o pipefail

FEDORA_KERNEL_VERSION=5.18.6-200.fc36
REPO_PWD=$(pwd)

### Dependencies
dnf install -y fedpkg fedora-packager rpmdevtools ncurses-devel pesign git libkcapi libkcapi-devel libkcapi-static libkcapi-tools curl dwarves libbpf zip

## Set home build directory
rpmdev-setuptree

## Install the kernel source and finish installing dependencies
cd /root/rpmbuild/SOURCES
koji download-build --arch=src kernel-${FEDORA_KERNEL_VERSION}
rpm -Uvh kernel-${FEDORA_KERNEL_VERSION}.src.rpm

cd /root/rpmbuild/SPECS
dnf -y builddep kernel.spec

### Create patch file with custom drivers
FEDORA_KERNEL_VERSION=${FEDORA_KERNEL_VERSION} "/repo"/patch_driver.sh

### Apply patches
mkdir -p "/repo"/patches
while IFS= read -r file
do
  "/repo"/patch_kernel.sh "$file"
done < <(find "/repo"/patches -type f -name "*.patch" | sort)

echo "CONFIG_APPLE_BCE=m" >> "/root/rpmbuild/SOURCES/kernel-local"
echo "CONFIG_APPLE_IBRIDGE=m" >> "/root/rpmbuild/SOURCES/kernel-local"

### Change buildid to mbp
sed -i "s/# define buildid.*/%define buildid .t2/" "/root/rpmbuild"/SPECS/kernel.spec

### Build non-debug rpms
cd "/root/rpmbuild"/SPECS
rpmbuild -bb --with baseonly --without debug --without debuginfo --target=x86_64 kernel.spec

### Copy artifacts to shared volume
cd "/repo"
mkdir -p ./output
mkdir -p ./output/RPMS
cp -rfv /root/rpmbuild/RPMS/* ./output/RPMS/
