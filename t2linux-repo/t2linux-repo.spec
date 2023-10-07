Name: t2linux-repo
Version: 6.0.0
Release: 1%{?dist}
Summary: DNF Repo for linux on t2 macs.
License: MIT
URL: https://github.com/t2linux/fedora-kernel

Source0: t2linux-fedora.repo
Source1: t2linux-fedora-38.pub
Source3: t2linux-fedora-39.pub

%description
DNF repo files for linux on t2 macs.

%prep

%build

%install
install -D -m 644 %{SOURCE1} %{buildroot}/etc/pki/rpm-gpg/t2linux-fedora-38.pub
install -D -m 644 %{SOURCE2} %{buildroot}/etc/pki/rpm-gpg/t2linux-fedora-39.pub
install -D -m 644 %{SOURCE2} %{buildroot}/etc/yum.repos.d/t2linux-fedora.repo
	
%files
/etc/yum.repos.d/t2linux-fedora.repo
/etc/pki/rpm-gpg/t2linux-fedora-38.pub
/etc/pki/rpm-gpg/t2linux-fedora-39.pub
