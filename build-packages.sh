#!/usr/bin/bash

source /repo/util.sh

sign_packages() {
    # Takes private key called T2Linux Fedora
    echo $1 | base64 -d | gpg --import
    echo -e "%_signature gpg\n%_gpg_name T2Linux Fedora" > ~/.rpmmacros
    rpm --addsign /output/*.rpm
}

dnf install -y --quiet koji git curl pesign rpmdevtools rpm-sign rpm-build mock zstd

# Optimize mock
echo 'config_opts["plugin_conf"]["package_state_enable"] = False
config_opts["macros"]["%_smp_mflags"] = "-j8"
config_opts["plugin_conf"]["ccache_opts"]["compress"] = True
config_opts["plugin_conf"]["root_cache_opts"]["compress_program"] = "zstd"
config_opts["plugin_conf"]["root_cache_opts"]["extension"] = ".zst"
config_opts["plugin_conf"]["hw_info_enable"] = False' > /etc/mock/site-defaults.cfg

mkdir -p /output
cd /repo

if [ "$PACKAGE" == "kernel" ]; then
    /repo/kernel/kernel.sh
fi

build_srpm $PACKAGE

mock --quiet --rebuild /output/*.src.rpm --resultdir ./_mock_bin
cp ./_mock_bin/*.rpm /output

sign_packages $RPM_SIGNING_PRIVATE_KEY_B64
