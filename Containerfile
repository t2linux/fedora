FROM fedora:38
RUN dnf install -y koji git rpmdevtools rpm-sign mock ccache zstd &&\
    dnf clean all &&\
    echo 'config_opts["plugin_conf"]["package_state_enable"] = False
    config_opts["macros"]["%_smp_mflags"] = "-j8"
    config_opts["plugin_conf"]["ccache_opts"]["compress"] = True
    config_opts["plugin_conf"]["root_cache_opts"]["compress_program"] = "zstd"
    config_opts["plugin_conf"]["root_cache_opts"]["extension"] = ".zst"
    config_opts["plugin_conf"]["hw_info_enable"] = False' > /etc/mock/site-defaults.cfg
WORKDIR /repo