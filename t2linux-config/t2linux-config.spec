Name: t2linux-config
Version: 13.1.0
Release: 1%{?dist}
Summary: System configuration for linux on t2 macs.
License: MIT

Requires: t2linux-audio
Requires: t2linux-scripts
Recommends: rust-tiny-dfr
Recommends: t2fanrd

URL: https://t2linux.org

%description
Configuration and tools for linux on T2 macs.

%prep

%build
cat << EOF > t2linux-modules.conf
apple_bce
snd-seq
EOF
echo -e 'add_drivers+=" apple_bce snd_seq "' > t2linux-modules-install.conf

echo -e 'SUBSYSTEM=="net", ACTION=="add", ATTR{address}=="ac:de:48:00:11:22", NAME="t2_ncm"' > 99-network-t2-ncm.rules
cat << EOF > 99-network-t2-ncm.conf
[main]
no-auto-default=t2_ncm
EOF

%install

install -D -m 644 t2linux-modules-install.conf %{buildroot}/etc/dracut.conf.d/t2linux-modules-install.conf

install -D -m 644 t2linux-modules.conf %{buildroot}/etc/modules-load.d/t2linux-modules.conf

install -D -m 644 99-network-t2-ncm.rules %{buildroot}/etc/udev/rules.d/99-network-t2-ncm.rules
install -D -m 644 99-network-t2-ncm.conf %{buildroot}/etc/NetworkManager/conf.d/99-network-t2-ncm.conf

%post
grubby --args="intel_iommu=on iommu=pt mem_sleep_default=s2idle pcie_ports=native" --update-kernel=ALL

%files
/etc/modules-load.d/t2linux-modules.conf
/etc/dracut.conf.d/t2linux-modules-install.conf
/etc/udev/rules.d/99-network-t2-ncm.rules
/etc/NetworkManager/conf.d/99-network-t2-ncm.conf
