dnf install -y --quiet createrepo
mkdir -p /tmp/repo
cd /tmp/repo
cp /repo/output/RPMS/*/*.rpm .
createrepo .
