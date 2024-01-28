%global forgeurl https://github.com/GnomedDev/T2FanRD
%global commit 68859ca5f858d542444c64391faa90678afb6995
%forgemeta -iv

%bcond_without check

# prevent library files from being installed
%global __cargo_is_lib() 0

%global crate t2fanrd

Name:           t2fanrd
Version:        0.1.0
Release:        1%{?dist}
Summary:        Simple Fan Daemon for T2 Macs

SourceLicense:  GPL-3.0-or-later
License: GPL-3.0-or-later AND Apache-2.0 OR MIT AND MIT

URL:            %{forgeurl}
Source0:        %{forgesource}
Source1: t2fanrd.service

BuildRequires:  cargo-rpm-macros >= 24
BuildRequires: systemd-rpm-macros

%description
Simple Fan Daemon for T2 Macs.

%prep
%forgeautosetup -p1
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies

%install
%cargo_install
install -Dpm0644 -t %{buildroot}%{_unitdir} %{SOURCE1}

%if %{with check}
%check
%cargo_test
%endif

%post
%systemd_post %{crate}.service

%preun
%systemd_preun %{crate}.service

%postun
%systemd_postun_with_restart %{crate}.service

%files
%license LICENCE
%license LICENSE.dependencies
%doc README.md
%{_bindir}/%{crate}
%{_unitdir}/%{crate}.service

%changelog
%autochangelog
