%global forgeurl https://github.com/sharpenedblade/tiny-dfr
%global commit 82d80aef1a6e7ce2c5bd3dd766e6c658ed4a51da
%global crate tiny-dfr
%forgemeta

Name: rust-%{crate}
Version: 0.2.0
Release: 6%{?dist}
Summary: The most basic dynamic function row daemon possible
License: MIT AND Apache-2.0
URL: %{forgeurl}
Source: %{forgesource} 

%{?fc39:Patch: 0002-downgrade-cairo-rs.patch}

BuildRequires: rust-packaging >= 23
BuildRequires: systemd-rpm-macros
 
%description
The most basic dynamic function row daemon possible 

License: Apache-2.0 AND BSD-3-Clause AND CC0-1.0 AND ISC AND LGPL-2.1-or-later AND MIT AND MPL-2.0 AND Unicode-DFS-2016 AND (Apache-2.0 OR MIT) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND (MIT OR Apache-2.0 OR Zlib) AND (Unlicense OR MIT)
 
%files
%license LICENSE
%license LICENSE.material
%license LICENSE.dependencies
%doc README.md
%{_bindir}/%{crate}
%{_datadir}/%{crate}/
%{_udevrulesdir}/*.rules
%{_unitdir}/*.service

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
install -Dpm0644 -t %{buildroot}%{_datadir}/%{crate} share/%{crate}/*
install -Dpm0644 -t %{buildroot}%{_udevrulesdir} etc/udev/rules.d/*.rules
install -Dpm0644 -t %{buildroot}%{_unitdir} etc/systemd/system/*.service

%post
%systemd_post %{crate}.service

%preun
%systemd_preun %{crate}.service

%postun
%systemd_postun_with_restart %{crate}.service
