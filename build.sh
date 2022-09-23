#!/bin/bash

FEDORA_KERNEL_VERSION=5.19.9-200.fc36
PATCHES_GIT=https://github.com/Redecorating/linux-t2-arch
PATCHES_COMMIT=65a5575de77284c0a36c95510ebaaa8e8a867bc5

echo "=====INSTALLING DEPENDENCIES====="
dnf install -y fedpkg koji fedora-packager git curl pesign ncurses-devel libbpf fedpkg rpmdevtools ccache openssl-devel libkcapi libkcapi-devel libkcapi-static libkcapi-tools

rpmdev-setuptree
cd "/root/rpmbuild"/SPECS

echo "=====DOWNLOADING SOURCES====="
cd /root/rpmbuild/SOURCES
koji download-build --arch=src kernel-${FEDORA_KERNEL_VERSION}
rpm -Uvh kernel-${FEDORA_KERNEL_VERSION}.src.rpm
cd /root/rpmbuild/SPECS 
# Fedora devs are against merging kernel-local for all architectures, so we have to patch it in.
sed -i "s@for i in %{all_arch_configs}@for i in *.config@g" kernel.spec 
dnf -y builddep kernel.spec
cd /root/rpmbuild/SOURCES
curl "https://wiki.t2linux.org/tools/rmmod_tb.sh" > rmmod_tb.sh
curl "https://github.com/kekrby/t2-better-audio/archive/5a46dcb9f274c503802d77a0b11034312ef20f5d/t2-better-audio-5a46dcb.tar.gz" > t2-better-audio-5a46dcb.tar.gz

echo "======DOWNLOADING PATCHES====="
rm -rf /tmp/download /tmp/src
mkdir /tmp/download && cd /tmp/download 
git clone --single-branch --branch main ${PATCHES_GIT}
cd *
git checkout ${PATCHES_COMMIT}
rm -rf 0001-arch-additions.patch

echo "=====PREPARING SOURCES====="
cd ~/rpmbuild/SPECS
sed -i 's/# define buildid .local/%define buildid .t2/g' kernel.spec
echo "CONFIG_STAGING=y" >> "/root/rpmbuild/SOURCES/kernel-local"
echo "CONFIG_APPLE_IBRIDGE=m" >> "/root/rpmbuild/SOURCES/kernel-local"
echo "CONFIG_APPLE_BCE=m" >> "/root/rpmbuild/SOURCES/kernel-local"
echo "CONFIG_BT_HCIBCM4377=m" >> "/root/rpmbuild/SOURCES/kernel-local"
rpmbuild -bp kernel.spec

echo "=====COPYING SOURCE TREE====="
mkdir /tmp/src && cd /tmp/src
cp -r /root/rpmbuild/BUILD/* .
cd *
KSV=$(ls)
cp -r $KSV $KSV.new
KERNEL_TMP="$KSV.new"
cd $KERNEL_TMP

echo "=====PATCHING SOURCE TREE====="
git clone --depth=1 https://github.com/kekrby/apple-bce drivers/staging/apple-bce
git clone --depth=1 https://github.com/Redecorating/apple-ib-drv drivers/staging/apple-ibridge
cp /tmp/download/*/*.patch .
for i in *.patch; do 
    echo $i
    patch -f -l -p1 -N < $i;
done;
find . '(' \
    -name \*-baseline -o \
    -name \*-merge -o \
    -name \*-original -o \
    -name \*.orig -o \
    -name \*.rej \
')' -delete
rm -rf drivers/staging/*/.git
rm -rf *.patch
cd ..

echo "=====APPLYING PATCHES====="
diff -uNrp $KSV $KERNEL_TMP > /root/rpmbuild/SOURCES/linux-kernel-test.patch
sed -i "s@$KSV@@" /root/rpmbuild/SOURCES/linux-kernel-test.patch
sed -i "s@$KERNEL_TMP@@" /root/rpmbuild/SOURCES/linux-kernel-test.patch

echo "=====BUILDING====="
cd "/root/rpmbuild"/SPECS
cp /repo/*.spec .
rpmbuild -bb t2linux-config.spec
rpmbuild -bb --with baseonly --without debug --without debuginfo --target=x86_64 kernel.spec


# Copy artifacts to shared volume
cd "/repo"
mkdir -p ./output
mkdir -p ./output/RPMS
cp -rfv /root/rpmbuild/RPMS/* ./output/RPMS/
