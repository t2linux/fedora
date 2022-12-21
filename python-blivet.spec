%define is_rhel 0%{?rhel} != 0
	
 
	
# python3 is not available on RHEL <=7
	
%if %{is_rhel} && 0%{?rhel} <= 7
	
# disable python3 by default
	
%bcond_with python3
	
%else
	
%bcond_without python3
	
%endif
	
 
	
# python2 is not available on RHEL > 7 and not needed on Fedora > 28
	
%if 0%{?rhel} > 7 || 0%{?fedora} > 28
	
# disable python2 by default
	
%bcond_with python2
	
%else
	
%bcond_without python2
	
%endif
	
 
	
Summary:  A python module for system storage configuration
	
Name: python-blivet
	
Url: https://storageapis.wordpress.com/projects/blivet
	
Version: 3.5.0
	
 
	
#%%global prerelease .b2
	
# prerelease, if defined, should be something like .a1, .b1, .b2.dev1, or .c2
	
Release: 2%{?prerelease}%{?dist}
	
Epoch: 1
	
License: LGPLv2+
	
%global realname blivet
	
%global realversion %{version}%{?prerelease}
	
Source0: http://github.com/storaged-project/blivet/archive/%{realname}-%{realversion}.tar.gz
	
Source1: http://github.com/storaged-project/blivet/archive/%{realname}-%{realversion}-tests.tar.gz
	
 
	
%if 0%{?rhel} >= 9
	
Patch0: 0001-remove-btrfs-plugin.patch
	
%endif
	
Patch1: 0002-add-t2-support.patch 
	
# Versions of required components (done so we make sure the buildrequires
	
# match the requires versions of things).
	
%global partedver 1.8.1
	
%global pypartedver 3.10.4
	
%global utillinuxver 2.15.1
	
%global libblockdevver 2.24
	
%global libbytesizever 0.3
	
%global pyudevver 0.18
	
 
	
BuildArch: noarch
	
 
	
%description
	
The python-blivet package is a python module for examining and modifying
	
storage configuration.
	
 
	
%package -n %{realname}-data
	
Summary: Data for the %{realname} python module.
	
 
	
BuildRequires: make
	
BuildRequires: systemd
	
 
	
Conflicts: python-blivet < 1:2.0.0
	
Conflicts: python3-blivet < 1:2.0.0
	
 
	
%description -n %{realname}-data
	
The %{realname}-data package provides data files required by the %{realname}
	
python module.
	
 
	
%if %{with python3}
	
%package -n python3-%{realname}
	
Summary: A python3 package for examining and modifying storage configuration.
	
 
	
%{?python_provide:%python_provide python3-%{realname}}
	
 
	
BuildRequires: gettext
	
BuildRequires: python3-devel
	
BuildRequires: python3-setuptools
	
 
	
Requires: python3
	
Requires: python3-six
	
Requires: python3-pyudev >= %{pyudevver}
	
Requires: parted >= %{partedver}
	
Requires: python3-pyparted >= %{pypartedver}
	
Requires: libselinux-python3
	
Requires: python3-blockdev >= %{libblockdevver}
	
Recommends: libblockdev-btrfs >= %{libblockdevver}
	
Recommends: libblockdev-crypto >= %{libblockdevver}
	
Recommends: libblockdev-dm >= %{libblockdevver}
	
Recommends: libblockdev-fs >= %{libblockdevver}
	
Recommends: libblockdev-kbd >= %{libblockdevver}
	
Recommends: libblockdev-loop >= %{libblockdevver}
	
Recommends: libblockdev-lvm >= %{libblockdevver}
	
Recommends: libblockdev-mdraid >= %{libblockdevver}
	
Recommends: libblockdev-mpath >= %{libblockdevver}
	
Recommends: libblockdev-nvdimm >= %{libblockdevver}
	
Recommends: libblockdev-part >= %{libblockdevver}
	
Recommends: libblockdev-swap >= %{libblockdevver}
	
Recommends: libblockdev-s390 >= %{libblockdevver}
	
Requires: python3-bytesize >= %{libbytesizever}
	
Requires: util-linux >= %{utillinuxver}
	
Requires: lsof
	
Requires: python3-gobject-base
	
Requires: systemd-udev
	
Requires: %{realname}-data = %{epoch}:%{version}-%{release}
	
 
	
Obsoletes: blivet-data < 1:2.0.0
	
 
	
%if %{without python2}
	
Obsoletes: python2-blivet < 1:2.0.2-2
	
Obsoletes: python-blivet < 1:2.0.2-2
	
%else
	
Obsoletes: python-blivet < 1:2.0.0
	
%endif
	
 
	
%description -n python3-%{realname}
	
The python3-%{realname} is a python3 package for examining and modifying storage
	
configuration.
	
%endif
	
 
	
%if %{with python2}
	
%package -n python2-%{realname}
	
Summary: A python2 package for examining and modifying storage configuration.
	
 
	
%{?python_provide:%python_provide python2-%{realname}}
	
 
	
BuildRequires: gettext
	
BuildRequires: python2-devel
	
BuildRequires: python2-setuptools
	
 
	
Requires: python2
	
Requires: python2-six
	
Requires: python2-pyudev >= %{pyudevver}
	
Requires: parted >= %{partedver}
	
Requires: python2-pyparted >= %{pypartedver}
	
Requires: python2-libselinux
	
Requires: python2-blockdev >= %{libblockdevver}
	
Recommends: libblockdev-btrfs >= %{libblockdevver}
	
Recommends: libblockdev-crypto >= %{libblockdevver}
	
Recommends: libblockdev-dm >= %{libblockdevver}
	
Recommends: libblockdev-fs >= %{libblockdevver}
	
Recommends: libblockdev-kbd >= %{libblockdevver}
	
Recommends: libblockdev-loop >= %{libblockdevver}
	
Recommends: libblockdev-lvm >= %{libblockdevver}
	
Recommends: libblockdev-mdraid >= %{libblockdevver}
	
Recommends: libblockdev-mpath >= %{libblockdevver}
	
Recommends: libblockdev-nvdimm >= %{libblockdevver}
	
Recommends: libblockdev-part >= %{libblockdevver}
	
Recommends: libblockdev-swap >= %{libblockdevver}
	
Recommends: libblockdev-s390 >= %{libblockdevver}
	
Requires: python2-bytesize >= %{libbytesizever}
	
Requires: util-linux >= %{utillinuxver}
	
Requires: lsof
	
Requires: python2-hawkey
	
Requires: %{realname}-data = %{epoch}:%{version}-%{release}
	
 
	
Requires: systemd-udev
	
Requires: python2-gobject-base
	
 
	
Obsoletes: blivet-data < 1:2.0.0
	
Obsoletes: python-blivet < 1:2.0.0
	
 
	
%description -n python2-%{realname}
	
The python2-%{realname} is a python2 package for examining and modifying storage
	
configuration.
	
%endif
	
 
	
%prep
	
%autosetup -n %{realname}-%{realversion} -N
	
%autosetup -n %{realname}-%{realversion} -b1 -p1
	
 
	
%build
	
%{?with_python2:make PYTHON=%{__python2}}
	
%{?with_python3:make PYTHON=%{__python3}}
	
 
	
%install
	
%{?with_python2:make PYTHON=%{__python2} DESTDIR=%{buildroot} install}
	
%{?with_python3:make PYTHON=%{__python3} DESTDIR=%{buildroot} install}
	
 
	
%find_lang %{realname}
	
 
	
%files -n %{realname}-data -f %{realname}.lang
	
%{_sysconfdir}/dbus-1/system.d/*
	
%{_datadir}/dbus-1/system-services/*
	
%{_libexecdir}/*
	
%{_unitdir}/*
	
 
	
%if %{with python2}
	
%files -n python2-%{realname}
	
%license COPYING
	
%doc README.md ChangeLog examples
	
%{python2_sitelib}/*
	
%endif
	
 
	
%if %{with python3}
	
%files -n python3-%{realname}
	
%license COPYING
	
%doc README.md ChangeLog examples
	
%{python3_sitelib}/*
	
%endif
