#!/usr/bin/bash
set -e

SIGNING_KEY_UID=$( \
  echo "$SIGNING_KEY" \
  | gpg --show-key --with-colons \
  | awk -F: '$1=="uid"{print $10}' \
  )
echo -e "%_signature gpg\n%_gpg_name $SIGNING_KEY_UID" > ~/.rpmmacros

echo "$SIGNING_KEY" | gpg --import
unset SIGNING_KEY

# shellcheck disable=SC2164
mkdir -p /repo/builddir/dnf-repo && cd /repo/builddir/dnf-repo
echo "Signature: 8a477f597d28d172789f06886806bc55" > /repo/builddir/CACHEDIR.TAG
cp /repo/builddir/packages/*.rpm .
rm ./*.src.rpm
rpm --addsign ./*.rpm
createrepo .
