dnf install -y createrepo
mkdir -p /tmp/repo
cd /tmp/repo
cp /repo/*.rpm .
createrepo .
