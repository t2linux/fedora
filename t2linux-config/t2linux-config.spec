Name: t2linux-config
Version: 17.0.0
Release: 1%{?dist}
Summary: System configuration for linux on t2 macs.
License: MIT
URL: https://t2linux.org

BuildRequires: systemd
BuildRequires: systemd-rpm-macros

Requires: util-linux

%description
System configuration for linux on T2 macs.

%prep

%build
cat << EOF > t2linux-modules.conf
t2bce_dma
t2bce_core
t2bce_vhci
EOF
echo -e 'add_drivers+=" t2bce_dma t2bce_core t2bce_vhci "' > t2linux-modules-install.conf

echo -e 'SUBSYSTEM=="net", ACTION=="add", ATTR{address}=="ac:de:48:00:11:22", NAME="t2_ncm"' > 90-network-t2-ncm.rules
cat << EOF > 90-network-t2-ncm.conf
[main]
no-auto-default=t2_ncm
EOF

cat << 'EOF' > t2linux-hwclock.service
[Unit]
Description=Save system time to the hardware clock at shutdown
DefaultDependencies=no
After=local-fs.target
Before=shutdown.target
Conflicts=shutdown.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/bin/true
ExecStop=/bin/sh -c 'for r in /sys/class/rtc/rtc*; do grep -q ACPI000E "$r/name" 2>/dev/null && exec /usr/sbin/hwclock --rtc="/dev/${r##*/}" --systohc; done'

[Install]
WantedBy=multi-user.target
EOF

cat << EOF > 91-t2linux.preset
enable get-apple-firmware.service
enable t2fanrd.service
enable t2linux-hwclock.service
EOF

%install

install -D -m 644 t2linux-modules-install.conf %{buildroot}/usr/lib/dracut/dracut.conf.d/t2linux-modules-install.conf

install -D -m 644 t2linux-modules.conf %{buildroot}/usr/lib/modules-load.d/t2linux-modules.conf

install -D -m 644 90-network-t2-ncm.rules %{buildroot}%{_udevrulesdir}/90-network-t2-ncm.rules
install -D -m 644 90-network-t2-ncm.conf %{buildroot}/usr/lib/NetworkManager/conf.d/90-network-t2-ncm.conf

install -D -m 644 91-t2linux.preset %{buildroot}/usr/lib/systemd/system-preset/91-t2linux.preset

install -D -m 644 t2linux-hwclock.service %{buildroot}%{_unitdir}/t2linux-hwclock.service

%post
%systemd_post t2linux-hwclock.service

%preun
%systemd_preun t2linux-hwclock.service

%postun
%systemd_postun t2linux-hwclock.service

%files
%{_unitdir}/t2linux-hwclock.service
/usr/lib/modules-load.d/t2linux-modules.conf
/usr/lib/dracut/dracut.conf.d/t2linux-modules-install.conf
%{_udevrulesdir}/90-network-t2-ncm.rules
/usr/lib/NetworkManager/conf.d/90-network-t2-ncm.conf
/usr/lib/systemd/system-preset/91-t2linux.preset
