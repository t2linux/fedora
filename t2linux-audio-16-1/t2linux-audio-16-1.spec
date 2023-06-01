Name: t2linux-audio-16-1
Version: 0.2.0
Release: 1%{?dist}
Summary: Experimintal audio config for the MacBook Pro 16,1
License: MIT
URL: https://github.com/lemmyg/asahi-audio/tree/macbookT2_16_1

Requires: pipewire
Requires: wireplumber

Source0: https://github.com/lemmyg/asahi-audio/archive/refs/tags/%{version}.tar.gz

%description
Experimental DSP config for improving audio quality on the Macbook Pro 16-inch 2019 model. Using this has the risk of damaging the speakers.

%prep
%autosetup -n asahi-audio-%{version}

%install

install -Dm 644 conf/t2_161.conf %{buildroot}/%{_datadir}/pipewire/pipewire.conf.d/10-t2_161-sink.conf
mkdir -p %{buildroot}/%{_datadir}/pipewire/devices/apple/
install -m 644 firs/t2_161/* -t %{buildroot}/%{_datadir}/pipewire/devices/apple/
%files
%dir %{_datadir}/pipewire/devices/apple/
%{_datadir}/pipewire/devices/apple/*
%{_datadir}/pipewire/pipewire.conf.d/10-t2_161-sink.conf
