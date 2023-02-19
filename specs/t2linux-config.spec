Name: t2linux-config
Version: 7.0.0
Release: 1%{?dist}
Summary: System configuration for linux on t2 macs.
License: MIT

%undefine _disable_source_fetch

URL: https://t2linux.org

%global audio_config_commit_long e46839a28963e2f7d364020518b9dac98236bcae
%global audio_config_commit %(c=%{audio_config_commit_long}; echo ${c:0:7})  

Source1: https://github.com/kekrby/t2-better-audio/archive/%{audio_config_commit_long}/t2-better-audio-%{audio_config_commit}.tar.gz
Source2: rmmod_tb.sh
Source3: touchbar.sh
Source4: firmware.sh

%description
Configuration and tools for linux on t2 macs. Fixes suspend and audio.

%prep
tar -xf %{_sourcedir}/t2-better-audio-%{audio_config_commit}.tar.gz

%build
echo -e 'apple_bce\nsnd-seq' > t2linux.conf

echo -e 'add_drivers+=" apple_bce snd_seq "' > t2linux-install.conf

%install

mkdir -p %{buildroot}/usr/lib/systemd/system-sleep/
mv %{_sourcedir}/rmmod_tb.sh %{buildroot}/usr/lib/systemd/system-sleep/rmmod_tb.sh
chmod +x %{buildroot}/usr/lib/systemd/system-sleep/rmmod_tb.sh

mkdir -p %{buildroot}/usr/bin/
mv %{_sourcedir}/firmware.sh %{buildroot}/usr/bin/firmware
mv %{_sourcedir}/touchbar.sh %{buildroot}/usr/bin/touchbar
chmod +x %{buildroot}/usr/bin/*

mkdir -p %{buildroot}/etc/dracut.conf.d/
mv t2linux-install.conf %{buildroot}/etc/dracut.conf.d/t2linux-install.conf

mkdir -p %{buildroot}/etc/modules-load.d/
mv t2linux.conf %{buildroot}/etc/modules-load.d/t2linux.conf

mkdir -p %{buildroot}/usr/lib/udev/rules.d/
cp -r %{_builddir}/t2-better-audio-%{audio_config_commit_long}/files/91-audio-custom.rules %{buildroot}/usr/lib/udev/rules.d/

for dir in %{buildroot}/usr/share/alsa-card-profile/mixer %{buildroot}/usr/share/pulseaudio/alsa-mixer
do
    mkdir -p $dir
    cp -r %{_builddir}/t2-better-audio-%{audio_config_commit_long}/files/profile-sets $dir
    cp -r %{_builddir}/t2-better-audio-%{audio_config_commit_long}/files/paths $dir
done

%post
grubby --args="intel_iommu=on iommu=pt pcie_ports=compat" --update-kernel=ALL

%files
/usr/lib/systemd/system-sleep/rmmod_tb.sh
/etc/modules-load.d/t2linux.conf
/etc/dracut.conf.d/t2linux-install.conf
/usr/share/alsa-card-profile/mixer
/usr/share/pulseaudio/alsa-mixer
/usr/lib/udev/rules.d/
/usr/bin/firmware
/usr/bin/touchbar
