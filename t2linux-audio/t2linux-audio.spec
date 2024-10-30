Name: t2linux-audio
Version: 0.3.1
Release: 2%{?dist}
Summary: Speaker and mic config for T2 macs
License: MIT
URL: https://wiki.t2linux.org/guides/audio-config/
BuildArch: noarch

Source0: https://github.com/kekrby/t2-better-audio/archive/e46839a28963e2f7d364020518b9dac98236bcae.tar.gz

%description
Configuration files for audio on T2 macs. This fixes the mic volume, and also 
enables the internal speakers. It is highly recommended to install this, even
if you do not use the speakers.

%prep
%setup -n t2-better-audio-e46839a28963e2f7d364020518b9dac98236bcae

%build

%install

install -D -m 644 files/91-audio-custom.rules %{buildroot}/usr/lib/udev/rules.d/91-audio-t2.rules

install -d -m 755 %{buildroot}/%{_datadir}/alsa-card-profile/mixer/paths
install -m 644 files/paths/* %{buildroot}/%{_datadir}/alsa-card-profile/mixer/paths/

install -d -m 755 %{buildroot}/%{_datadir}/alsa-card-profile/mixer/profile-sets
install -m 644 files/profile-sets/* %{buildroot}/%{_datadir}/alsa-card-profile/mixer/profile-sets/

install -d -m 755 %{buildroot}/%{_datadir}/pulseaudio/alsa-mixer/paths
install -m 644 files/paths/* %{buildroot}/%{_datadir}/pulseaudio/alsa-mixer/paths/

install -d -m 755 %{buildroot}/%{_datadir}/pulseaudio/alsa-mixer/profile-sets
install -m 644 files/profile-sets/* %{buildroot}/%{_datadir}/pulseaudio/alsa-mixer/profile-sets/

%files
%{_datadir}/alsa-card-profile/mixer/paths/*
%{_datadir}/alsa-card-profile/mixer/profile-sets/*
%{_datadir}/pulseaudio/alsa-mixer/paths/*
%{_datadir}/pulseaudio/alsa-mixer/profile-sets/*
/usr/lib/udev/rules.d/91-audio-t2.rules
