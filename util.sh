#!/usr/bin/bash

build_package() {
    cd $1
    spectool -g $1.spec
    mock --quiet --buildsrpm --spec $1.spec --sources . --resultdir /repo/_output
    mock --quiet --rebuild /repo/_output/*.src.rpm --resultdir /repo/_output
    cd ..
}

download_koji_sources() {
    # Takes full koji build name as input
    START_DIR=$PWD
    mkdir -p /tmp/koji-download && cd /tmp/koji-download
    koji download-build --arch=src $1
    rpmdev-extract $1.src.rpm
    mv -n $1.src/* $START_DIR
    cd $START_DIR
}

sign_packages() {
    echo $1 | base64 -d | gpg --import
    echo -e "%_signature gpg\n%_gpg_name $2" > ~/.rpmmacros
    rpm --addsign *.rpm
}
