#!/usr/bin/bash

build_srpm() {
    cd $1
    spectool -g $1.spec
    mock --quiet --buildsrpm --spec $1.spec --sources . --resultdir /tmp`/_mock
    cp /tmp/_mock/*.src.rpm /repo/_output
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