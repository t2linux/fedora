dnf install -y --quiet createrepo
cd /repo
mkdir ./dnf-repo && cd ./dnf-repo
cp /repo/_output/*.rpm .
rm *.src.rpm
createrepo .
