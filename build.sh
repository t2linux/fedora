#!/bin/bash

FEDORA_KERNEL_VERSION=6.1.5-200.fc37
PATCHES_GIT=https://github.com/t2linux/linux-t2-patches
PATCHES_COMMIT=b35900bdab14c1b60e1f3ecaefb3c18006434105

echo "=====INSTALLING DEPENDENCIES====="
dnf install -y fedpkg koji fedora-packager git curl pesign ncurses-devel libbpf fedpkg rpmdevtools ccache openssl-devel libkcapi libkcapi-devel libkcapi-static libkcapi-tools rpm-sign

rpmdev-setuptree
cd "/root/rpmbuild"/SPECS

echo "=====DOWNLOADING SOURCES====="
cd /root/rpmbuild/SOURCES
koji download-build --arch=src kernel-${FEDORA_KERNEL_VERSION}
koji download-build --arch=src python-blivet-3.5.0-1.fc37
rpm -Uvh kernel-${FEDORA_KERNEL_VERSION}.src.rpm
rpm -Uvh python-blivet-3.5.0-1.fc37.src.rpm
cd /root/rpmbuild/SPECS 
# Fedora devs are against merging kernel-local for all architectures when keys are not properly specified, so we have to patch it in.
sed -i "s@for i in %{all_arch_configs}@for i in *.config@g" kernel.spec 
dnf -y builddep kernel.spec
dnf -y builddep python-blivet.spec

echo "======DOWNLOADING PATCHES====="
rm -rf /tmp/download /tmp/src
mkdir /tmp/download && cd /tmp/download 
git clone --single-branch --branch main ${PATCHES_GIT}
cd *
git checkout ${PATCHES_COMMIT}

echo "=====PREPARING SOURCES====="
cd ~/rpmbuild/SPECS
sed -i 's/# define buildid .local/%define buildid .t2/g' kernel.spec
mv -f /repo/python-blivet.spec /repo/rpmbuild/SPECS/python-blivet.spec
mv /repo/0002-add-t2-support.patch /root/rpmbuild/SOURCES/0002-add-t2-support.patch
cat /tmp/download/*/extra_config > /root/rpmbuild/SOURCES/kernel-local
rpmbuild -bp kernel.spec

echo "=====COPYING SOURCE TREE====="
mkdir /tmp/src && cd /tmp/src
cp -r /root/rpmbuild/BUILD/* .
cd *
KSV=$(realpath *)
cp -r $KSV $KSV.new
KERNEL_TMP="$KSV.new"
cd $KERNEL_TMP

echo "=====PATCHING SOURCE TREE====="
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

echo "=====IMPORTING KEYS====="
gpg --import /repo/rpm_signing_key
rpm --import /repo/repo/t2linux-fedora-ci.pub
rm -rfv /repo/rpm_signing_key
echo -e "%_signature gpg\n%_gpg_name t2linux-fedora CI" > ~/.rpmmacros

echo "=====BUILDING====="
cd "/root/rpmbuild"/SPECS
cp /repo/*.spec .
cp /repo/repo/* /root/rpmbuild/SOURCES
rpmbuild -bb t2linux-config.spec
rpmbuild -bb t2linux-repo.spec
rpmbuild -bb python-blivet.spec
rpmbuild -bb --with baseonly --without debug --without debuginfo --target=x86_64 kernel.spec
rpm --addsign /root/rpmbuild/RPMS/x86_64/*.rpm


# Copy artifacts to shared volume
cd "/repo"
mkdir -p ./output
mkdir -p ./output/RPMS
cp -rfv /root/rpmbuild/RPMS/* ./output/RPMS/
