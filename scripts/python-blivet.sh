#!/bin/bash

cd /root/rpmbuild/SPECS

echo "=====BUILDING====="
cd /root/rpmbuild/SPECS
/repo/scripts/build-rpm-from-repo.sh /repo python-blivet python-blivet-3.5.0-1.fc37
