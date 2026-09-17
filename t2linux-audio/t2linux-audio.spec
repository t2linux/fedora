%global forgeurl https://github.com/sharpenedblade/KaiT2en-Fedora
%global commit 9527bffcd9d2293345ce89112329780e1b66b501
%forgemeta -iv

Name: t2linux-audio
Version: 2.2.0
Release: 1%{?dist}
Summary: Speaker, mic, and DSP config for T2 macs
License: MIT
URL: https://wiki.t2linux.org/guides/audio-config/
BuildArch: noarch

Requires: pipewire >= 1.0
Requires: wireplumber >= 0.5.1-2
Requires: pipewire-module-filter-chain-lv2
Requires: lsp-plugins-lv2 >= 1.2.13-2
Requires: lv2-bankstown >= 1.1.0
Requires: lv2-triforce >= 0.2.0
Requires: lv2-swh-plugins

BuildRequires: systemd-rpm-macros

Source0:        %{forgesource}

%description
Configuration files for audio on T2 macs. This fixes the mic volume, and also 
enables and calibrates the internal speakers. It is highly recommended to
install this, even if you do not use the speakers.

%prep
%forgeautosetup -p1

%build

%install
install -d -m 0755 %{buildroot}/%{_datadir}/alsa/ucm2
cp -a modules/t2bce_audio-alsa-ucm-conf/ucm2/. %{buildroot}/%{_datadir}/alsa/ucm2

install -d -m 0755 %{buildroot}/%{_datadir}/wireplumber/wireplumber.conf.d
cp -a modules/t2bce_audio-dsp/wireplumber.conf %{buildroot}/%{_datadir}/wireplumber/wireplumber.conf.d/99-t2-audio.conf

install -d -m 0755 %{buildroot}/%{_udevrulesdir}
cp -a modules/t2bce_audio-dsp/99-t2-audio-rename.rules %{buildroot}/%{_udevrulesdir}

install -d -m 0755 %{buildroot}/%{_datadir}/t2linux-audio/
cp -a modules/t2bce_audio-dsp/firs/. %{buildroot}/%{_datadir}/t2linux-audio


%files
%{_datadir}/alsa/ucm2/*
%{_datadir}/t2linux-audio/
%{_datadir}/wireplumber/wireplumber.conf.d/99-t2-audio.conf
/%{_udevrulesdir}/99-t2-audio-rename.rules
