#!/usr/bin/bash
packages=( "t2linux-config" "t2linux-repo" "t2linux-audio" "kernel")

mkdir -p /repo/_output
for current_package in "${packages[@]}"; do
    if [ "$current_package" == "kernel" ]; then
        /repo/kernel/kernel.sh
    fi
    cd /repo/"$current_package" || echo "ERROR: Package $current_package not found"
    spectool -g "$current_package".spec
    mock --buildsrpm --spec "$current_package".spec --sources . --resultdir /repo/_output
done

mock --rebuild /repo/_output/*.src.rpm --resultdir /repo/_output
