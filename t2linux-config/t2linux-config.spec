Name: t2linux-config
Version: 11.5.0
Release: 1%{?dist}
Summary: System configuration for linux on t2 macs.
License: MIT

Requires: t2linux-audio
Recommends: rust-tiny-dfr
Recommends: t2fanrd

URL: https://t2linux.org

Source1: firmware.sh

%description
Configuration and tools for linux on T2 macs.

%prep

%build
echo -e 'apple_bce\nsnd-seq' > t2linux-modules.conf
echo -e 'add_drivers+=" apple_bce snd_seq "' > t2linux-modules-install.conf

echo -e 'SUBSYSTEM=="net", ACTION=="add", ATTR{address}=="ac:de:48:00:11:22", NAME="t2_ncm"' > 99-network-t2-ncm.rules
echo -e '[main]\nno-auto-default=t2_ncm' > 99-network-t2-ncm.conf

%install

install -D -m 755 %{SOURCE1} %{buildroot}/%{_bindir}/firmware.sh

install -D -m 644 t2linux-modules-install.conf %{buildroot}/etc/dracut.conf.d/t2linux-modules-install.conf

install -D -m 644 t2linux-modules.conf %{buildroot}/etc/modules-load.d/t2linux-modules.conf

install -D -m 644 99-network-t2-ncm.rules /etc/udev/rules.d/99-network-t2-ncm.rules
install -D -m 644 99-network-t2-ncm.conf /etc/NetworkManager/conf.d/99-network-t2-ncm.conf

%post
grubby --args="intel_iommu=on iommu=pt mem_sleep_default=s2idle" --update-kernel=ALL
grubby --remove-args="pcie_ports=compat" --update-kernel=ALL

%files
/etc/modules-load.d/t2linux-modules.conf
/etc/dracut.conf.d/t2linux-modules-install.conf
%{_bindir}/firmware.sh
/etc/udev/rules.d/99-network-t2-ncm.rules
/etc/NetworkManager/conf.d/99-network-t2-ncm.conf
