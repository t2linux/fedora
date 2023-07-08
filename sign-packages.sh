#!/usr/bin/bash
source /repo/util.sh
dnf install --quiet -y rpm-sign rpmdevtools

cd /repo/_output
sign_packages $RPM_SIGNING_PRIVATE_KEY_B64 "T2Linux Fedora"
