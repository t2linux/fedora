Name: t2linux-repo
Version: 5.0.1
Release: 2%{?dist}
Summary: DNF Repo for linux on t2 macs.
License: MIT

URL: https://github.com/t2linux/t2linux-fedora-kernel
Source0: t2linux-fedora.pub
Source1: t2linux-fedora-new.pub
Source2: t2linux-fedora.repo

%description
DNF repo files for linux on t2 macs.

%prep

%build

%install
install -D -m 644 %{SOURCE0} %{buildroot}/etc/pki/rpm-gpg/t2linux-fedora.pub
install -D -m 644 %{SOURCE1} %{buildroot}/etc/pki/rpm-gpg/t2linux-fedora-new.pub

install -D -m 644 %{SOURCE2} %{buildroot}/etc/yum.repos.d/t2linux-fedora.repo
	
%files
/etc/yum.repos.d/t2linux-fedora.repo
/etc/pki/rpm-gpg/t2linux-fedora.pub
/etc/pki/rpm-gpg/t2linux-fedora-new.pub
