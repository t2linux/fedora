%global forgeurl https://github.com/kekrby/tiny-dfr/
%global commit 61223862921d2b1d4f88436ad9c89ddc879a5699
%forgemeta

Name: rust-tiny-dfr
Version: 0.1.2
Release: 1%{?dist}
Summary: The most basic dynamic function row daemon possible
License: MIT AND Apache-2.0
URL: %{forgeurl}
Source: %{forgesource} 

# Use librsvg 2.57.0
Patch0: fix-librsvg-metadata.patch

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
%{_bindir}/tiny-dfr
%{_datadir}/tiny-dfr/*
%{_udevrulesdir}/*.rules
%{_unitdir}/tiny-dfr.service

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
mkdir -p %{buildroot}%{_datadir}/
cp -r -t %{buildroot}%{_datadir}/ share/tiny-dfr
install -Dpm0644 -t %{buildroot}%{_udevrulesdir} etc/udev/rules.d/*.rules
install -Dpm0644 -t %{buildroot}%{_unitdir} etc/systemd/system/tiny-dfr.service

%post
%systemd_post tiny-dfr.service

%preun
%systemd_preun tiny-dfr.service

%postun
%systemd_postun_with_restart tiny-dfr.service
