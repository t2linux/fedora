#!/usr/bin/bash
set -e

KERNEL_VERSION=6.10.12-200.fc40

cd "$sourcedir"
koji download-build --quiet --arch=src "kernel-$KERNEL_VERSION"
rpmdev-extract -q "kernel-$KERNEL_VERSION.src.rpm"
mv -n "kernel-$KERNEL_VERSION.src"/* .
rm -r "kernel-$KERNEL_VERSION.src.rpm" "kernel-$KERNEL_VERSION.src"

# Set buildid to .t2
sed -i 's/# define buildid .local/%define buildid .t2/g' "kernel.spec"

# Bump release
# sed -i 's/%define specrelease 200/%define specrelease 202/g' "kernel.spec"

# Disable debug kernels
sed -i "/%define with_debug /c %define with_debug 0" "kernel.spec"

# Add our patches
sed -i "/Patch1:/a Patch2: t2linux-combined.patch" "kernel.spec"
sed -i "/ApplyOptionalPatch patch-%{patchversion}-redhat.patch/a ApplyOptionalPatch t2linux-combined.patch" "kernel.spec"

cat "linux-t2-patches/extra_config" > "kernel-local"
echo "CONFIG_MODULE_FORCE_UNLOAD=y" >> "kernel-local"
cat "linux-t2-patches"/*.patch > "t2linux-combined.patch"
