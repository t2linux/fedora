Name: t2linux-audio
Version: 0.3.0
Release: 1%{?dist}
Summary: Speaker and mic config for T2 macs
License: MIT
URL: https://wiki.t2linux.org/guides/audio-config/
BuildArch: noarch

Requires: pipewire
Requires: wireplumber

Source0: https://github.com/lemmyg/t2-apple-audio-dsp/archive/refs/tags/%{version}.tar.gz
Source1: https://github.com/kekrby/t2-better-audio/archive/e46839a28963e2f7d364020518b9dac98236bcae.tar.gz

Patch0: 01-disable-rnnoise.patch

%description
Configuration files for audio on T2 macs. This fixes the mic volume, and also 
enables the internal speakers. It is highly recommended to install this, even
if you do not use the speakers.

%prep
%setup -n t2-apple-audio-dsp-%{version}
%setup -D -a 1 -n t2-apple-audio-dsp-%{version}
mv t2-better-audio*/* .
rmdir t2-better-audio*
%patch 0

%build

%install

# Mic filterchain
install -D -m 644 config/10-t2_mic.conf %{buildroot}/%{_datadir}/pipewire/pipewire.conf.d/10-t2_mic.conf

# 16,1 speakers
install -d -m 755 %{buildroot}/%{_datadir}/pipewire/devices/apple/
install -D -m 644 config/10-t2_161_speakers.conf %{buildroot}/%{_datadir}/pipewire/pipewire.conf.d/10-t2_161_speakers.conf
install -m 644 firs/t2_161/*.wav %{buildroot}/%{_datadir}/pipewire/devices/apple/

install -D -m 644 files/91-audio-custom.rules %{buildroot}/usr/lib/udev/rules.d/91-audio-t2.rules

install -d -m 755 %{buildroot}/%{_datadir}/alsa-card-profile/mixer/paths
install -m 644 files/paths/* %{buildroot}/%{_datadir}/alsa-card-profile/mixer/paths/

install -d -m 755 %{buildroot}/%{_datadir}/alsa-card-profile/mixer/profile-sets
install -m 644 files/profile-sets/* %{buildroot}/%{_datadir}/alsa-card-profile/mixer/profile-sets/

%package mbp16-1
Summary: DSP config to improve speaker quality on the MacBookPro16,1

%description mbp16-1
Experimental DSP config for improving audio quality on the Macbook Pro 16-inch 2019 model. This should only be used on the 16,1.

%package mic
Summary: Pipewire filters for better mic quality and noise cancelation
Requires: ladspa-swh-plugins

%description mic
Pipewire filters for better mic quality. This uses RNNoise to remove background noise.

%files
%{_datadir}/alsa-card-profile/mixer/paths/*
%{_datadir}/alsa-card-profile/mixer/profile-sets/*
/usr/lib/udev/rules.d/91-audio-t2.rules

%files mic
%{_datadir}/pipewire/pipewire.conf.d/10-t2_mic.conf

%files mbp16-1
%{_datadir}/pipewire/devices/apple/*.wav
%{_datadir}/pipewire/pipewire.conf.d/10-t2_161_speakers.conf
