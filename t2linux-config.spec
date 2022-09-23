Name: linux-t2
Version: 5.19.9
Release: 1%{?dist}
Summary: System configuration for linux on t2 macs.

License: MIT
URL: https://t2linux.org
Source0: https://wiki.t2linux.org/tools/rmmod_tb.sh
Source1: https://github.com/kekrby/t2-better-audio/archive/5a46dcb9f274c503802d77a0b11034312ef20f5d/t2-better-audio-5a46dcb.tar.gz

%description
Configuration files for linux on t2 macs. Everything works except for TouchId, eGPU, and audio switching.

%prep
cp %{_sourcedir}/rmmod_tb.sh %{_builddir}
tar -xf t2-better-audio-*.tar.gz
cp -r t2-better-audio-* %{_builddir}

%build
echo -e 'hid-apple\nbcm5974\nsnd-seq\napple_bce' > apple_bce.conf

echo -e 'add_drivers+=" hid_apple snd-seq apple_bce "\nforce_drivers+=" hid_apple snd-seq apple_bce "' > apple_bce_install.conf

%install
mkdir -p %{buildroot}/etc/dracut.conf.d/
mv apple_bce_install.conf %{buildroot}/etc/dracut.conf.d/apple_bce_install.conf

mkdir -p %{buildroot}/etc/modules-load.d/
mv apple_bce.conf %{buildroot}/etc/modules-load.d/apple_bce.conf

mkdir -p %{buildroot}/lib/systemd/system-sleep
mv %{_builddir}/rmmod_tb.sh %{buildroot}/lib/systemd/system-sleep/rmmod_tb.sh
chmod +x %{buildroot}/lib/systemd/system-sleep/rmmod_tb.sh

mkdir -p %{buildroot}/usr/share/alsa/ucm2
cp -r %{_builddir}/t2-better-audio-*/files/ucm2/* %{buildroot}/usr/share/alsa/ucm2

%post
grubby --remove-args="efi=noruntime" --update-kernel=ALL
grubby --args="intel_iommu=on iommu=pt pcie_ports=compat" --update-kernel=ALL

%files
/etc/modules-load.d/apple_bce.conf
/lib/systemd/system-sleep/rmmod_tb.sh
/etc/dracut.conf.d/apple_bce_install.conf
