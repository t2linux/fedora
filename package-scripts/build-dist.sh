#!/bin/bash

cd /root/rpmbuild/SPECS

echo "=====BUILDING====="
cd /root/rpmbuild/SPECS
/repo/build-spec.sh /repo t2linux-config
/repo/build-spec.sh /repo t2linux-repo
