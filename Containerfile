FROM fedora:38
SHELL ["/usr/bin/env", "bash", "-c"]
RUN dnf install -y koji git rpmdevtools rpm-sign mock ccache zstd && \
    dnf clean all && \
    echo "\
    config_opts['plugin_conf']['package_state_enable'] = False \n\
    config_opts['macros']['_smp_mflags'] = '-j8' \n\
    config_opts['plugin_conf']['ccache_opts']['compress'] = True \n\
    config_opts['plugin_conf']['root_cache_opts']['compress_program'] = 'zstd' \n\
    config_opts['plugin_conf']['root_cache_opts']['extension'] = '.zst' \n\
    config_opts['plugin_conf']['hw_info_enable'] = False\n" > /etc/mock/site-defaults.cfg
WORKDIR /repo