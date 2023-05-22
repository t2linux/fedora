#!/bin/bash

echo "=====INSTALLING DEPENDENCIES====="
dnf install -y --quiet koji git curl pesign rpmdevtools rpm-sign rpm-build mock

echo "=====IMPORTING KEYS====="
gpg --import /repo/rpm_signing_key
rm -rfv /repo/rpm_signing_key
echo -e "%_signature gpg\n%_gpg_name T2Linux Fedora" > ~/.rpmmacros

echo "=====BUILDING====="
mkdir -p /output
/repo/scripts/t2linux-fedora.sh
/repo/scripts/kernel.sh
rpm --addsign /output/*.rpm
