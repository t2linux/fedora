%global forgeurl https://github.com/kaiT2en/KaiT2en-Fedora
%global commit 8de95468f08c6db37924bcb8f9adc12c769add71
%forgemeta -iv

Name: t2linux-audio
Version: 3.0.0
Release: 2%{?dist}
Summary: Audio configuration for t2 macs
License: GPL-3.0-or-later
URL: https://kait2en.org
BuildArch: noarch

Requires: pipewire >= 1.0
Requires: wireplumber >= 0.5.13
Requires: alsa-ucm
Requires: systemd-udev
Recommends: %{name}-dsp = %{version}-%{release}

BuildRequires: forge-srpm-macros
BuildRequires: python3
BuildRequires: systemd-rpm-macros

Source0: %{forgesource}
Source1: build-wireplumber-config.py

%description
This is required for audio and mic support on t2 macs.

%package dsp
Summary: Speaker and mic DSP config for t2 macs
Requires: %{name} = %{version}-%{release}
Requires: pipewire >= 1.0
Requires: wireplumber >= 0.5.13
Requires: pipewire-module-filter-chain-lv2
Requires: lsp-plugins-lv2 >= 1.2.13-2
Requires: lv2-bankstown >= 1.1.0

%description dsp
Custom software DSP that makes the speakers sound significantly
better and fixes the mic volume on t2 macs.

%prep
%forgeautosetup -p1

%build
python3 dsp/tools/build.py --output dsp/build --datadir %{_datadir}
python3 %{SOURCE1} dsp/build %{_datadir}

%install
install -d -m 0755 %{buildroot}/%{_datadir}/alsa/ucm2
cp -a modules/t2bce_audio-alsa-ucm-conf/ucm2/. %{buildroot}/%{_datadir}/alsa/ucm2
install -D -m 0644 dsp/build/89-t2-dsp.rules %{buildroot}/%{_udevrulesdir}/89-t2-dsp.rules

install -d -m 0755 %{buildroot}/%{_datadir}/t2-dsp
cp -a dsp/build/profiles/. %{buildroot}/%{_datadir}/t2-dsp/profiles
rm dsp/build/profiles/*/README.md

install -D -m 0644 dsp/build/50-t2-dsp.conf %{buildroot}/%{_datadir}/wireplumber/wireplumber.conf.d/50-t2-dsp.conf

%files
%license LICENSE LICENSING.md LICENSES/GPL-3.0-or-later.txt
%{_datadir}/alsa/ucm2/AppleT2/
%{_datadir}/alsa/ucm2/conf.d/AppleT2x2/
%{_datadir}/alsa/ucm2/conf.d/AppleT2x4/
%{_datadir}/alsa/ucm2/conf.d/AppleT2x6/
%{_udevrulesdir}/89-t2-dsp.rules

%files dsp
%license LICENSE LICENSING.md LICENSES/GPL-3.0-or-later.txt
%doc dsp/README.md
%{_datadir}/t2-dsp/
%{_datadir}/wireplumber/wireplumber.conf.d/50-t2-dsp.conf
