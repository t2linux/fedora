#!/usr/bin/env bash

# Name of dir and spec file
# EXAMPLE: foo.spec -> foo
PACKAGE_NAME=$1

# Name of package to download from koji.fedoraproject.org
# EXAMPLE: python-blivet-3.5.0-1.fc37
if [ -n "$2" ]; then
    KOJI_VERSION="$3"
fi

if [ -n "$KOJI_VERSION" ]; then
    echo "=====DOWNLOADING SOURCES====="
    mkdir -p /tmp/koji-download && cd /tmp/koji-download
    koji download-build --arch=src "$KOJI_VERSION"
    rpmdev-extract "$KOJI_VERSION".src.rpm

    mkdir -p "$BASE_DIR"/"$PACKAGE_NAME"
    mv -n "$KOJI_VERSION".src/* "$BASE_DIR"/"$PACKAGE_NAME"
fi

cd $PACKAGE_NAME
spectool -g $PACKAGE_NAME.spec
mock --buildsrpm --spec $PACKAGE_NAME.spec --sources . --resultdir ./_mock
mock --rebuild ./_mock/*.src.rpm --resultdir ./_mock
cp ./_mock/*.rpm /output