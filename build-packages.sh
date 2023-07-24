#!/usr/bin/bash
source /repo/util.sh

cd /repo

if [ "$PACKAGE" == "kernel" ]; then
    /repo/kernel/kernel.sh
fi

cd /repo/$PACKAGE
build_package $PACKAGE.spec
rm /repo/_output/*.log
