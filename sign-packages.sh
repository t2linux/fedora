#!/usr/bin/bash
cd /repo/_output || exit 2

echo "$RPM_SIGNING_PRIVATE_KEY_B64" | base64 -d | gpg --import
rpm --addsign ./*.rpm
echo -e "%_signature gpg\n%_gpg_name T2Linux Fedora" > ~/.rpmmacros
