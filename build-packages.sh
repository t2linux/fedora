#!/usr/bin/bash

source /repo/util.sh

sign_packages() {
    # Takes private key called T2Linux Fedora
    echo $1 | base64 -d | gpg --import
    echo -e "%_signature gpg\n%_gpg_name T2Linux Fedora" > ~/.rpmmacros
    rpm --addsign /output/*.rpm
}

echo "=====INSTALLING DEPENDENCIES====="
dnf install -y --quiet koji git curl pesign rpmdevtools rpm-sign rpm-build mock

echo "=====BUILDING====="
mkdir -p /output
cd /repo

for i in t2linux-config t2linux-repo t2linux-audio; do
    build_spec $i
done

/repo/kernel/kernel.sh

sign_packages $RPM_SIGNING_PRIVATE_KEY_B64
