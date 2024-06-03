%global debug_package %{nil}

%global forgeurl https://github.com/linux-apfs/linux-apfs-rw
Version: 0.3.9
%forgemeta

%global buildforkernels akmod

%define kmod_name apfs
%define src_name linux-apfs-rw

Name: %{kmod_name}-kmod
Release: 1%{?dist}
Summary: APFS module for linux, with experimental write support
URL: %{forgeurl}
Source: %{forgesource}
License: GPL-2.0

BuildRequires: kmodtool

%description
The Apple File System (APFS) is the copy-on-write filesystem currently used on
all Apple devices. This module provides a degree of experimental support on Linux.

This module is the result of reverse engineering and testing has been limited.
If you make use of the write support, expect data corruption. Encryption is not
yet implemented even in read-only mode, and neither are fusion drives.

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{kmod_name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%prep

# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%forgeautosetup

./genver.sh

for kernel_version  in %{?kernel_versions}; do
    cp -a $PWD %{_builddir}/_kmod_build_${kernel_version%%___*}
done

%build

for kernel_version in %{?kernel_versions}; do
    make modules %{?_smp_mflags} \
        -C ${kernel_version##*___} \
        M=%{_builddir}/_kmod_build_${kernel_version%%___*}
done

%install

for kernel_version in %{?kernel_versions}; do
    make install \
        -C ${kernel_version##*___} \
        M=%{_builddir}/_kmod_build_${kernel_version%%___*} \
        DESTDIR=%{buildroot} \
        KMODPATH=%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
done

%{?akmod_install}

%changelog
