%global forgeurl https://github.com/kaiT2en/KaiT2en-Fedora
%global commit 3cd03334448ed7d37c1ecf11f48baa24d10770b7
%forgemeta -iv

Name: t2linux-audio
Version: 2.0.0
Release: 1%{?dist}
Summary: Speaker and mic config and dsp for T2 macs
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

Source0:        %{forgesource}

%description
Configuration files for audio on T2 macs. This fixes the mic volume, and also 
enables the internal speakers. It is highly recommended to install this, even
if you do not use the speakers.

%prep
%forgeautosetup -p1

%build

%install
install -d -m 0755 %{buildroot}/%{_datadir}/alsa/ucm2
cp -a modules/t2bce_audio-alsa-ucm-conf/ucm2/. %{buildroot}/%{_datadir}/alsa/ucm2

install -d -m 0755 %{buildroot}/%{_datadir}/wireplumber/wireplumber.conf.d
cp -a modules/t2bce_audio-dsp/wireplumber.conf %{buildroot}/%{_datadir}/wireplumber/wireplumber.conf.d/99-t2-audio.conf

install -d -m 0755 %{buildroot}/%{_libdir}/udev/rules.d/
cp -a modules/t2bce_audio-dsp/99-t2-audio-rename.rules %{buildroot}/%{_libdir}/udev/rules.d/

install -d -m 0755 %{buildroot}/%{_datadir}/t2linux-audio/
cp -a modules/t2bce_audio-dsp/firs/. %{buildroot}/%{_datadir}/t2linux-audio


%files
%{_datadir}/alsa/ucm2/*
%{_datadir}/t2linux-audio/
%{_datadir}/wireplumber/wireplumber.conf.d/99-t2-audio.conf
%{_libdir}/udev/rules.d/99-t2-audio-rename.rules
