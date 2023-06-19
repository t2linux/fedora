#!/bin/bash

echo "=====INSTALLING DEPENDENCIES====="
dnf install -y --quiet koji git curl pesign rpmdevtools rpm-sign rpm-build mock

echo "=====IMPORTING KEYS====="
gpg --import /repo/rpm_signing_key
rm -rfv /repo/rpm_signing_key
echo -e "%_signature gpg\n%_gpg_name T2Linux Fedora" > ~/.rpmmacros

echo "=====BUILDING====="
mkdir -p /output
cd /repo

/repo/rpm-build-in-mock.sh t2linux-config
/repo/rpm-build-in-mock.sh t2linux-repo
/repo/rpm-build-in-mock.sh t2linux-audio
/repo/kernel/kernel.sh

rpm --addsign /output/*.rpm
