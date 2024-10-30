Name: t2linux-repos
Version: 3.0.0
Release: 1%{?dist}
Summary: Copr repo for t2linux owned by sharpenedblade.
License: MIT
URL: https://copr.fedorainfracloud.org/coprs/sharpenedblade/t2linux

Provides: copr-sharpenedblade-t2linux-release = 2.0.0-1
Obsoletes: copr-sharpenedblade-t2linux-release < 1.0.0-2
Obsoletes: t2linux-repo < 7.0.0-2

Source0: copr-sharpenedblade-t2linux.repo

%description
Patched kernel and supporting packages for hardware enablement on t2
macs.

%prep

%build

%install
install -D -m 644 %{SOURCE0} %{buildroot}/etc/yum.repos.d/copr-sharpenedblade-t2linux.repo
	
%files
/etc/yum.repos.d/copr-sharpenedblade-t2linux.repo
