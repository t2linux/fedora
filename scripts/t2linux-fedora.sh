#!/bin/bash

cd /root/rpmbuild/SPECS

echo "=====BUILDING====="
cd /root/rpmbuild/SPECS
/repo/scripts/build-rpm-from-repo.sh /repo t2linux-config
/repo/scripts/build-rpm-from-repo.sh /repo t2linux-repo
