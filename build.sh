#!/bin/bash

FEDORA_KERNEL_VERSION=5.18.19-200.fc36
PATCHES_GIT=https://github.com/Redecorating/linux-t2-arch
PATCHES_COMMIT=d1ba02f45198888016606b903f055a962de7eb81

# Dependencies
dnf install -y fedpkg koji fedora-packager git curl pesign ncurses-devel libbpf fedpkg rpmdevtools

# Set home build directory
rpmdev-setuptree
cd "/root/rpmbuild"/SPECS

# Get kernel source and install dependencies
cd /root/rpmbuild/SOURCES
koji download-build --arch=src kernel-${FEDORA_KERNEL_VERSION}
rpm -Uvh kernel-${FEDORA_KERNEL_VERSION}.src.rpm
cd /root/rpmbuild/SPECS 
sed -i 's/# define buildid .local/%define buildid .t2/g' kernel.spec
dnf -y builddep kernel.spec

curl "https://wiki.t2linux.org/tools/rmmod_tb.sh" > rmmod_tb.sh

# Download patches
mkdir /tmp/download && cd /tmp/download 
git clone --single-branch --branch main ${PATCHES_GIT}
cd *
git checkout ${PATCHES_COMMIT}
rm -rf 0001-arch-additions.patch
mkdir /root/a
cp *.patch /root/a

cd ~/rpmbuild/SPECS
rpmbuild -bp kernel.spec

# Get apple modules
mkdir /tmp/src && cd /tmp/src
cp "/root/rpmbuild/build/" .
KSV="*"
cp -r $KSV $KSV.new
KERNEL_TMP="$KSV.new"
cd $KERNEL_TMP
git clone --depth=1 https://github.com/t2linux/apple-bce-drv drivers/staging/apple-bce
git clone --depth=1 https://github.com/t2linux/apple-ib-drv drivers/staging/apple-ibridge
cp /root/a/* .
cat *.patch | patch -f -l -p1
echo "+++++++++++PATCHED++++++++++++++++"
./scripts/config --module BT_HCIBCM4377
./scripts/config --module APPLE_BCE
./scripts/config --module APPLE_IBRIDGE
echo "+_+++++++++++++config+++++++++++++"
cd ..
echo "+++++++++++++++++++++++++++++++DIFFF++++++++++++++"
diff -uNrp $KSV $KERNEL_TMP > /root/rpmbuild/SOURCES/linux-kernel-test.patch
echo "+++++++++++++++DIFFED++++++++++++"
sed -i "s@$KSV/@@" /root/rpmbuild/SOURCES/0001-apple.patch
sed -i "s@$KERNEL_TMP/@@" /root/rpmbuild/SOURCES/0001-apple.patch

# Apply patches
cd /root/rpmbuild/SPECS
echo "CONFIG_STAGING=y" >> "/root/rpmbuild/SOURCES/kernel-local"
echo "CONFIG_APPLE_BCE=y" >> "/root/rpmbuild/SOURCES/kernel-local"
echo "CONFIG_APPLE_IBRIDGE=y" >> "/root/rpmbuild/SOURCES/kernel-local"

# Build non-debug rpms
cd "/root/rpmbuild"/SPECS
cp /repo/*.spec .
echo "++++++++++++++++BUILD++++++++++++++++="
# rpmbuild -bb --target=x86_64 t2linux-config.spec || exit 0
rpmbuild -bb --with baseonly --without debug --without debuginfo --target=x86_64 kernel.spec


# Copy artifacts to shared volume
cd "/repo"
mkdir -p ./output
mkdir -p ./output/RPMS
cp -rfv /root/rpmbuild/RPMS/* ./output/RPMS/
