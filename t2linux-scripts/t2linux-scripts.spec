%global wiki_commit f71483df460fb97d5c39edf3af03dfc5f6be9a7c

Name: t2linux-scripts
Version: 2.2.0
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

%install

install -D -m 755 %{SOURCE0} %{buildroot}/%{_libexecdir}/get-apple-firmware
install -D -m 644 %{SOURCE1} %{buildroot}/%{_unitdir}/get-apple-firmware.service


%post
%systemd_post get-apple-firmware.service


%preun
%systemd_preun get-apple-firmware.service


%postun
%systemd_postun get-apple-firmware.service


%files
%{_libexecdir}/get-apple-firmware
%{_unitdir}/get-apple-firmware.service
