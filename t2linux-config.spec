Name: t2linux-config
Version: 6.0.8
Release: 1%{?dist}
Summary: System configuration for linux on t2 macs.
License: MIT

%undefine _disable_source_fetch

URL: https://t2linux.org
Source0: https://wiki.t2linux.org/tools/rmmod_tb.sh


%global audio_config_commit_long e46839a28963e2f7d364020518b9dac98236bcae
%global audio_config_commit %(c=%{audio_config_commit_long}; echo ${c:0:7})  

Source1: https://github.com/kekrby/t2-better-audio/archive/%{audio_config_commit_long}/t2-better-audio-%{audio_config_commit}.tar.gz
%description
Configuration files for linux on t2 macs. Everything works except for TouchId, eGPU, and audio switching.

%prep
cp %{_sourcedir}/rmmod_tb.sh %{_builddir}
tar -xf %{_sourcedir}/t2-better-audio-%{audio_config_commit}.tar.gz

%build
echo -e 'apple_bce\nsnd-seq' > t2linux.conf

echo -e 'add_drivers+=" apple_bce snd_seq "' > t2linux-install.conf

%install
mkdir -p %{buildroot}/etc/dracut.conf.d/
mv apple_bce_install.conf %{buildroot}/etc/dracut.conf.d/t2linux-install.conf

mkdir -p %{buildroot}/etc/modules-load.d/
mv apple_bce.conf %{buildroot}/etc/modules-load.d/t2linux.conf

mkdir -p %{buildroot}/lib/systemd/system-sleep
mv %{_builddir}/rmmod_tb.sh %{buildroot}/lib/systemd/system-sleep/rmmod_tb.sh
chmod +x %{buildroot}/lib/systemd/system-sleep/*

mkdir -p %{buildroot}/usr/lib/udev/rules.d/
cp -r %{_builddir}/t2-better-audio-%{audio_config_commit_long}/files/91-audio-custom.rules %{buildroot}/usr/lib/udev/rules.d/

for dir in %{buildroot}/usr/share/alsa-card-profile/mixer %{buildroot}/usr/share/pulseaudio/alsa-mixer
do
    mkdir -p $dir
    cp -r %{_builddir}/t2-better-audio-%{audio_config_commit_long}/files/profile-sets $dir
    cp -r %{_builddir}/t2-better-audio-%{audio_config_commit_long}/files/paths $dir
done

%post
grubby --remove-args="efi=noruntime" --update-kernel=ALL
grubby --args="intel_iommu=on iommu=pt pcie_ports=compat" --update-kernel=ALL

%files
/etc/modules-load.d/t2linux.conf
/lib/systemd/system-sleep/rmmod_tb.sh
/etc/dracut.conf.d/t2linux-install.conf
/usr/share/alsa-card-profile/mixer
/usr/share/pulseaudio/alsa-mixer
/usr/lib/udev/rules.d/
