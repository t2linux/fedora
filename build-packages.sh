#!/usr/bin/bash
set -e

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

mock --rebuild --chain /repo/_output/*.src.rpm --localrepo /repo/_output/mock_repo
cp -f /repo/_output/mock_repo/results/*/*/*.rpm /repo/_output
rm -rf /repo/_output/*.log
