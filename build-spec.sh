#!/usr/bin/env bash

# Location of sources/ and specs/
# Sources are in $BASE_DIR/sources/$PACKAGE_NAME
BASE_DIR=$1

# Name of spec file without the extension
# EXAMPLE: foo.spec -> foo
PACKAGE_NAME=$2

cd /root/rpmbuild/SPECS

echo "=====PREPARING SOURCES====="
cp "$BASE_DIR"/specs/"$PACKAGE_NAME".spec /root/rpmbuild/SPECS/
cp -r "$BASE_DIR"/sources/"$PACKAGE_NAME"/* /root/rpmbuild/SOURCES

echo "=====INSTALLING DEPENDENCIES====="
cd  /root/rpmbuild/SPECS/
dnf -y builddep "$PACKAGE_NAME".spec

echo "=====BUILDING PACKAGE====="
cd /root/rpmbuild/SPECS/
rpmbuild -bb "$PACKAGE_NAME".spec
