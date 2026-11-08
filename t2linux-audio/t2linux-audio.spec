%global forgeurl https://github.com/kaiT2en/KaiT2en-Fedora
%global commit 8de95468f08c6db37924bcb8f9adc12c769add71
%forgemeta -iv

Name: t2linux-audio
Version: 3.0.0
Release: 1%{?dist}
Summary: Speaker, mic, and DSP config for T2 macs
License: GPL-3.0-or-later
URL: https://kait2en.org
BuildArch: noarch

Requires: pipewire >= 1.0
Requires: wireplumber >= 0.5.13
Requires: pipewire-module-filter-chain-lv2
Requires: lsp-plugins-lv2 >= 1.2.13-2
Requires: lv2-bankstown >= 1.1.0
Requires: systemd-udev

BuildRequires: forge-srpm-macros
BuildRequires: python3
BuildRequires: systemd-rpm-macros

Source0: %{forgesource}
Source1: 52-t2-dsp-profiles.conf

%description
Configuration files for audio on T2 macs. This fixes the mic volume, and also
enables and calibrates the internal speakers. It is highly recommended to
install this, even if you do not use the speakers.

%prep
%forgeautosetup -p1

%build
python3 dsp/tools/build.py --output dsp/build --datadir %{_datadir}

%install
install -d -m 0755 %{buildroot}/%{_datadir}/alsa/ucm2
cp -a modules/t2bce_audio-alsa-ucm-conf/ucm2/. %{buildroot}/%{_datadir}/alsa/ucm2

install -d -m 0755 %{buildroot}/%{_datadir}/t2-dsp
cp -a dsp/build/profiles/. %{buildroot}/%{_datadir}/t2-dsp/profiles
rm %{buildroot}/%{_datadir}/t2-dsp/profiles/*/README.md

install -D -m 0644 dsp/build/51-t2-dsp.conf %{buildroot}/%{_datadir}/wireplumber/wireplumber.conf.d/51-t2-dsp.conf
install -D -m 0644 %{SOURCE1} %{buildroot}/%{_datadir}/wireplumber/wireplumber.conf.d/52-t2-dsp-profiles.conf
install -D -m 0644 dsp/integration/wireplumber/t2-default-output.lua %{buildroot}/%{_datadir}/wireplumber/scripts/t2-default-output.lua
install -D -m 0644 dsp/build/89-t2-dsp.rules %{buildroot}/%{_udevrulesdir}/89-t2-dsp.rules

%files
%license LICENSE LICENSING.md LICENSES/GPL-3.0-or-later.txt
%doc dsp/README.md
%{_datadir}/alsa/ucm2/AppleT2/
%{_datadir}/alsa/ucm2/conf.d/AppleT2x2/
%{_datadir}/alsa/ucm2/conf.d/AppleT2x4/
%{_datadir}/alsa/ucm2/conf.d/AppleT2x6/
%{_datadir}/t2-dsp/
%{_datadir}/wireplumber/wireplumber.conf.d/51-t2-dsp.conf
%{_datadir}/wireplumber/wireplumber.conf.d/52-t2-dsp-profiles.conf
%{_datadir}/wireplumber/scripts/t2-default-output.lua
%{_udevrulesdir}/89-t2-dsp.rules
