#!/usr/bin/bash
set -e

packages=( "t2linux-config" "t2linux-audio" "rust-tiny-dfr" "kernel" "copr-sharpenedblade-t2linux-release" )

mkdir -p /repo/builddir
builddir=$(mktemp -d -p "/repo/builddir"); export builddir
function cleanup {
  rm -rf "$builddir"
}
trap cleanup EXIT

for current_package in "${packages[@]}"; do

    [[ -d "/repo/$current_package" ]] || exit 10

    export package_builddir="$builddir/$current_package"
    mkdir -p "$package_builddir"

    cp -fr "/repo/$current_package"/* "$package_builddir" 
    if [ "$current_package" == "kernel" ]; then
        /repo/kernel/kernel.sh
    fi

    export specfile="$package_builddir/$current_package.spec"
    [[ -f "$specfile" ]] || exit 11

    spectool -g -C "$package_builddir" "$specfile"
    mock --buildsrpm --spec "$specfile" --sources "$package_builddir" --resultdir "$builddir"
done

mock --rebuild --chain "$builddir"/*.src.rpm --localrepo "$builddir"
mkdir -p /repo/builddir/packages
cp -f "$builddir"/results/*/*/*.rpm /repo/builddir/packages/
cleanup
