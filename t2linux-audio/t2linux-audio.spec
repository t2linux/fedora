%global forgeurl https://github.com/deqrocks/t2bce
%global commit 69bebad9349cb47f5c939829a4bef47b988da209
%forgemeta -iv

Name: t2linux-audio
Version: 1.0.0
Release: 1%{?dist}
Summary: Speaker and mic config for T2 macs
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
cp -a t2bce_audio-alsa-ucm-conf/ucm2/. %{buildroot}/%{_datadir}/alsa/ucm2


%files
%{_datadir}/alsa/ucm2/*
