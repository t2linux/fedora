#!/usr/bin/bash
source /repo/util.sh

if [[ -z "$1" ]]; then
    packages=""
    echo "Available packages: t2linux-config, t2linux-repo, t2linux-config, or kernel"
    read -p "What package(s) do you want to build: " -a packages 
else
    packages=( "$@" )
fi

for current_package in ${packages[@]}; do
    if [ "$current_package" == "kernel" ]; then
        /repo/kernel/kernel.sh
    fi
    cd /repo/$current_package
    build_package $current_package.spec
done
