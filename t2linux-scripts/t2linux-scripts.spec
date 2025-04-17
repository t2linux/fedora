%global wiki_commit f71483df460fb97d5c39edf3af03dfc5f6be9a7c

Name: t2linux-scripts
Version: 2.0.0
Release: 1%{?dist}
Summary: t2linux support scripts
License: MIT
URL: https://wiki.t2linux.org/
BuildArch: noarch

BuildRequires: systemd-rpm-macros

Source0: https://raw.githubusercontent.com/t2linux/wiki/%{wiki_commit}/docs/tools/firmware.sh
Source1: https://raw.githubusercontent.com/t2linux/wiki/%{wiki_commit}/docs/tools/get-apple-firmware.service

%description
t2linux first boot and support scripts

%prep

%build

cat << EOF > 55-get-apple-firmware.preset
enable get-apple-firmware.service
EOF

%install

install -D -m 755 %{SOURCE0} %{buildroot}/%{_libexecdir}/get-apple-firmware
install -D -m 644 %{SOURCE1} %{buildroot}/%{_unitdir}/get-apple-firmware.service
install -D -m 644 55-get-apple-firmware.preset %{buildroot}/usr/lib/systemd/system-preset/55-get-apple-firmware.preset


%files
%{_libexecdir}/get-apple-firmware
%{_unitdir}/get-apple-firmware.service
/usr/lib/systemd/system-preset/55-get-apple-firmware.preset
