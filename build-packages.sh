#!/usr/bin/bash
source /repo/util.sh

if [[ -z "$PACKAGE" ]]; then
    PACKAGE=""
    echo "Available packages: t2linux-config, t2linux-repo, t2linux-config, or kernel"
    read -p "Name of package to build: " PACKAGE
fi

cd /repo

if [ "$PACKAGE" == "kernel" ]; then
    /repo/kernel/kernel.sh
fi

cd /repo/$PACKAGE
build_package $PACKAGE.spec
