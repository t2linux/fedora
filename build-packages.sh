#!/usr/bin/bash
source /repo/util.sh

if [[ -z "$1" ]]; then
    package=""
    echo "Available packages: t2linux-config, t2linux-repo, t2linux-config, or kernel"
    read -p "Name of package to build: " package
else
    package="$1"
fi

cd /repo

if [ "$package" == "kernel" ]; then
    /repo/kernel/kernel.sh
fi

cd /repo/$package
build_package $package.spec
