#!/usr/bin/bash
set -e

if [ "$1" == "all" ]; then
    packages=( "t2linux-config" "t2linux-audio" "rust-tiny-dfr" "kernel" "copr-sharpenedblade-t2linux-release" "rust-arraydeque" "rust-nonempty" "rust-rust-ini0.20" "t2fanrd" "apfs" "apfs-kmod" )
else
    packages=( "$@" )
fi

builddir="/repo/builddir"; export builddir
rm -rf $builddir; mkdir -p $builddir

for current_package in "${packages[@]}"; do

    [[ -d "/repo/$current_package" ]] || exit 10

    export sourcedir="$builddir/sources/$current_package"
    mkdir -p "$sourcedir"

    cp -fr "/repo/$current_package"/* "$sourcedir" 
    if [ "$current_package" == "kernel" ]; then
        /repo/kernel/kernel.sh
    fi

    export specfile="$sourcedir/$current_package.spec"
    [[ -f "$specfile" ]] || exit 11

    spectool -g -C "$sourcedir" "$specfile"
    mock --buildsrpm --spec "$specfile" --sources "$sourcedir" --resultdir "$builddir/srpms/$current_package"
done

mock --rebuild --chain "$builddir"/srpms/*/*.src.rpm --localrepo "$builddir"
