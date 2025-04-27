Name: t2linux-config
Version: 15.0.0
Release: 1%{?dist}
Summary: System configuration for linux on t2 macs.
License: MIT
URL: https://t2linux.org

BuildRequires: systemd

%description
System configuration for linux on T2 macs.

%prep

%build
cat << EOF > t2linux-modules.conf
apple_bce
snd-seq
EOF
echo -e 'add_drivers+=" apple_bce snd_seq "' > t2linux-modules-install.conf

echo -e 'SUBSYSTEM=="net", ACTION=="add", ATTR{address}=="ac:de:48:00:11:22", NAME="t2_ncm"' > 90-network-t2-ncm.rules
cat << EOF > 90-network-t2-ncm.conf
[main]
no-auto-default=t2_ncm
EOF

cat << EOF > 91-t2linux.preset
enable get-apple-firmware.service
enable t2fanrd.service
EOF

%install

install -D -m 644 t2linux-modules-install.conf %{buildroot}/usr/lib/dracut/dracut.conf.d/t2linux-modules-install.conf

install -D -m 644 t2linux-modules.conf %{buildroot}/usr/lib/modules-load.d/t2linux-modules.conf

install -D -m 644 90-network-t2-ncm.rules %{buildroot}%{_udevrulesdir}/90-network-t2-ncm.rules
install -D -m 644 90-network-t2-ncm.conf %{buildroot}/usr/lib/NetworkManager/conf.d/90-network-t2-ncm.conf

install -D -m 644 91-t2linux.preset %{buildroot}/usr/lib/systemd/system-preset/91-t2linux.preset

%files
/usr/lib/modules-load.d/t2linux-modules.conf
/usr/lib/dracut/dracut.conf.d/t2linux-modules-install.conf
%{_udevrulesdir}/90-network-t2-ncm.rules
/usr/lib/NetworkManager/conf.d/90-network-t2-ncm.conf
/usr/lib/systemd/system-preset/91-t2linux.preset
