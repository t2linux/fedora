#!/usr/bin/bash
source /repo/util.sh

# Install dependencies
dnf install -y --quiet koji git curl pesign rpmdevtools rpm-sign rpm-build mock zstd

# Optimize mock
echo 'config_opts["plugin_conf"]["package_state_enable"] = False
config_opts["macros"]["%_smp_mflags"] = "-j8"
config_opts["plugin_conf"]["ccache_opts"]["compress"] = True
config_opts["plugin_conf"]["root_cache_opts"]["compress_program"] = "zstd"
config_opts["plugin_conf"]["root_cache_opts"]["extension"] = ".zst"
config_opts["plugin_conf"]["hw_info_enable"] = False' > /etc/mock/site-defaults.cfg

cd /repo

if [ "$PACKAGE" == "kernel" ]; then
    /repo/kernel/kernel.sh
fi

mkdir  /repo/_output
build_srpm $PACKAGE
rm /repo/_output/*.log

cd /repo/_output
sign_packages $RPM_SIGNING_PRIVATE_KEY_B64 "T2Linux Fedora"
