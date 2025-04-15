#!/usr/bin/bash

git clone --recurse-submodules https://github.com/t2linux/fedora t2-fedora
cd t2-fedora/kernel
export package_builddir="$PWD"
./kernel.sh
