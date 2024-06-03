%global debug_package %{nil}

%global forgeurl https://github.com/linux-apfs/linux-apfs-rw
Version: 0.3.9
%forgemeta

Name: apfs
Release: 1%{?dist}
Summary: APFS module for linux, with experimental write support
URL: %{forgeurl}
Source: %{forgesource}
License: GPL-2.0

Provides: %{name}-kmod-common = %{version}
Requires: %{name}-kmod >= %{version}

%description
The Apple File System (APFS) is the copy-on-write filesystem currently used on
all Apple devices. This module provides a degree of experimental support on Linux.

This module is the result of reverse engineering and testing has been limited.
If you make use of the write support, expect data corruption. Encryption is not
yet implemented even in read-only mode, and neither are fusion drives.

%prep

%forgeautosetup

%build

%install

%files

%doc README.rst
%license LICENSE

%changelog
