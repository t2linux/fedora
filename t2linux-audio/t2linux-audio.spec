Name: t2linux-audio
Version: 0.3.0
Release: 1%{?dist}
Summary: Speaker and mic config for T2 macs
License: MIT
URL: https://wiki.t2linux.org/guides/audio-config/

Requires: pipewire
Requires: wireplumber

Source0: https://github.com/lemmyg/t2-apple-audio-dsp/archive/refs/tags/%{version}.tar.gz
Source1: https://github.com/kekrby/t2-better-audio/archive/t2-better-audio-e46839a.tar.gz

%description
Configuration files for audio on T2 macs. This fixes the mic volume, and also 
enables the internal speakers. It is highly recommended to install this, even
 if you do not use the speakers.

%prep
%autosetup -n t2-apple-audio-dsp-%{version}
%autosetup -n t2-better-audio-e46839a

%build

%install

install -D -m 644 conf/t2_161.conf %{buildroot}/%{_datadir}/pipewire/pipewire.conf.d/10-t2_161-sink.conf

install -d -m 755 %{buildroot}/%{_datadir}/pipewire/devices/apple/
install -m 644 firs/t2_161/* %{buildroot}/%{_datadir}/pipewire/devices/apple/

install -D -m 644 files/91-audio-custom.rules %{buildroot}/%{_libdir}/udev/rules.d/91-audio-t2.rules

install -d -m 755 %{buildroot}/%{_datdir}/alsa-card-profile/mixer
install -m 644 files/profile-sets/* files/paths/* %{buildroot}/%{_datdir}/alsa-card-profile/mixer 

install -d -m 755 %{buildroot}/%{_datadir}/pulseaudio/alsa-mixer
install -m 644 files/profile-sets/* files/paths/* %{buildroot}/%{_datdir}/pulseaudio/alsa-mixer  

%package mbp16-1
Summary: DSP config to improve speaker quality on the MacBookPro16,1

%description mbp16-1
Experimental DSP config for improving audio quality on the Macbook Pro 16-inch 2019 model. This should only be used on the 16,1.

%files
%{_datadir}/alsa-card-profile/mixer/*
%{_datadir}/pulseaudio/alsa-mixer/*
%{_libdir}/udev/rules.d/91-audio-t2.rules

%files mbp16-1
%{_datadir}/pipewire/devices/apple/*
%{_datadir}/pipewire/pipewire.conf.d/10-t2_161-sink.conf
