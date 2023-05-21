#!/usr/bin/env bash

# Sources are in $BASE_DIR/$PACKAGE_NAME
BASE_DIR=$1

# Name of spec file without the extension
# EXAMPLE: foo.spec -> foo
PACKAGE_NAME=$2

# Name of package to download from koji.fedoraproject.org
# EXAMPLE: python-blivet-3.5.0-1.fc37
if [ -n "$3" ]; then
    KOJI_VERSION="$3"
fi

cd /root/rpmbuild/SPECS

if [ -n "$KOJI_VERSION" ]; then
    echo "=====DOWNLOADING SOURCES====="
    mkdir -p /tmp/koji-download && cd /tmp/koji-download
    koji download-build --arch=src "$KOJI_VERSION"
    rpmdev-extract "$KOJI_VERSION".src.rpm
    mv -f "$KOJI_VERSION".src/"$PACKAGE_NAME".spec /root/rpmbuild/SPECS/ 
    mv "$KOJI_VERSION".src/* /root/rpmbuild/SOURCES/ 
fi

echo "=====PREPARING SOURCES====="
cp -f "$BASE_DIR"/"$PACKAGE_NAME"/*.spec /root/rpmbuild/SPECS/
cp -fr "$BASE_DIR"/"$PACKAGE_NAME"/* /root/rpmbuild/SOURCES/

echo "=====INSTALLING DEPENDENCIES====="
cd  /root/rpmbuild/SPECS/
dnf -y --quiet builddep "$PACKAGE_NAME".spec

echo "=====BUILDING PACKAGE====="
cd /root/rpmbuild/SPECS/
rpmbuild -bb "$PACKAGE_NAME".spec
