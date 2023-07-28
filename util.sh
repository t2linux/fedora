#!/usr/bin/bash

build_package() {
    spectool -g "$1"
    mkdir -p /repo/_output
    mock --buildsrpm --spec "$1" --sources . --resultdir /repo/_output
    mock --rebuild /repo/_output/*.src.rpm --resultdir /repo/_output
}

download_koji_sources() {
    # Takes full koji build name as input
    koji download-build --arch=src "$1"
    rpmdev-extract "$1".src.rpm
    mv -n "$1".src/* .
    rm -r "$1".src "$1".src.rpm
}

sign_packages() {
    echo "$1" | base64 -d | gpg --import
    echo -e "%_signature gpg\n%_gpg_name $2" > ~/.rpmmacros
    rpm --addsign ./*.rpm
}
