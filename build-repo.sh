dnf install -y --quiet createrepo
mkdir -p /rpm-repo
cd /rpm-repo
cp /output/*.rpm .
createrepo .
