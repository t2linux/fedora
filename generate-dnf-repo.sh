dnf install -y --quiet createrepo
cd /rpm-repo
cp /repo/_output/*.rpm .
rm *.src.rpm
createrepo .
