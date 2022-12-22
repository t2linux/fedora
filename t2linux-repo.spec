Name: t2linux-repo
Version: 3.0.0
Release: 1%{?dist}
Summary: DNF Repo for linux on t2 macs.
License: MIT

URL: https://github.com/sharpenedblade/t2linux-fedora-kernel
Source0: t2linux-fedora-ci.pub
Source1: t2linux-fedora.repo

%description
DNF repo files for linux on t2 macs.

%prep

%build

%install
install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
install -m 644 %{_sourcedir}/t2linux-fedora-ci.pub $RPM_BUILD_ROOT/etc/pki/rpm-gpg/

install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
install -m 644 %{_sourcedir}/t2linux-fedora.repo $RPM_BUILD_ROOT/etc/yum.repos.d

	
%files
	
%dir /etc/yum.repos.d
%config /etc/yum.repos.d/t2linux-fedora.repo
%dir /etc/pki/rpm-gpg	
/etc/pki/rpm-gpg/t2linux-fedora-ci.pub
