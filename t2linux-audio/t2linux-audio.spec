%global forgeurl https://github.com/sharpenedblade/KaiT2en-Fedora
%global commit b45ca92cb9c5bdfd885068556733d44bfd3d5afe
%forgemeta -iv

Name: t2linux-audio
Version: 2.0.0
Release: 1%{?dist}
Summary: Speaker and mic config and dsp for T2 macs
License: MIT
URL: https://wiki.t2linux.org/guides/audio-config/
BuildArch: noarch

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
