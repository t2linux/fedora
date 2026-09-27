%global forgeurl https://github.com/kaiT2en/KaiT2en-Fedora
%global commit fbc43ad316312228e27d70aa39710fb44dd1464f
%forgemeta -iv

Name:           t2-touchid
Version:        0.1.0
Release:        1%{?dist}
Summary:        Apple T2 Touch ID bridge for fprintd
License:        GPL-3.0-or-later
URL:            %{forgeurl}
Source0:        %{forgesource}
Source1:        t2-touchid-network-setup
Source2:        t2-touchid-network-setup.service
Source3:        10-network-setup.conf
Source4:        t2-touchid.nmconnection
ExclusiveArch:  x86_64

BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  make
BuildRequires:  systemd-rpm-macros
BuildRequires:  checkpolicy
BuildRequires:  policycoreutils-devel

Requires:       t2linux-config >= 16.0.0-2
Requires:       fprintd
Requires:       fprintd-pam
Requires:       libfprint
Requires:       dbus
Requires:       NetworkManager
Requires:       systemd
Requires:       bash
Requires(post): policycoreutils
Requires(preun): policycoreutils
Requires(postun): policycoreutils

%description
Apple T2 Touch ID bridge for stock Fedora fprintd, libfprint and pam_fprintd.
BridgeXPC support is linked into the daemon.

%prep
%forgeautosetup -p1

cd t2-services/t2-touchid
%cargo_prep

%generate_buildrequires
# cargo2rpm does not recurse into in-tree path dependencies, so generate the
# requirements for each Rust crate that is linked into t2-touchid.
cd t2-services/t2-touchid
%cargo_generate_buildrequires

cd protocols/t2-biometrickit
%cargo_generate_buildrequires

cd ../../../shared/protocols/t2-bridgexpc
%cargo_generate_buildrequires

%build
cd t2-services/t2-touchid
%cargo_build

make -C integration/selinux

%check
cd t2-services/t2-touchid
%cargo_test

%install
make -C t2-services/t2-touchid install \
    PREFIX=/usr \
    DESTDIR=%{buildroot} \
    SYSTEMD_UNIT_DIR=%{_unitdir} \
    DATADIR=%{_datadir} \
    SYSCONFDIR=%{_sysconfdir}

install -Dm0755 %{SOURCE1} \
    %{buildroot}%{_libexecdir}/t2-touchid/network-setup

install -Dm0644 %{SOURCE2} \
    %{buildroot}%{_unitdir}/t2-touchid-network-setup.service

install -Dm0644 %{SOURCE3} \
    %{buildroot}%{_unitdir}/kait2en-t2-touchid.service.d/10-network-setup.conf

install -Dm0600 %{SOURCE4} \
    %{buildroot}%{_prefix}/lib/NetworkManager/system-connections/t2-touchid.nmconnection

install -Dm0644 \
    t2-services/t2-touchid/integration/selinux/kait2en-t2-touchid.pp \
    %{buildroot}%{_datadir}/selinux/packages/kait2en-t2-touchid.pp

%post
%systemd_post kait2en-t2-touchid.service

/usr/sbin/semodule -X 200 -i \
    %{_datadir}/selinux/packages/kait2en-t2-touchid.pp >/dev/null 2>&1 || :

if [ -d /run/t2-touchid ]; then
    /usr/sbin/restorecon -RF /run/t2-touchid >/dev/null 2>&1 || :
fi

%preun
%systemd_preun kait2en-t2-touchid.service

%postun
%systemd_postun_with_restart kait2en-t2-touchid.service

if [ "$1" -eq 0 ]; then
    /usr/sbin/semodule -X 200 -r kait2en-t2-touchid >/dev/null 2>&1 || :
fi

%files
%license LICENSE
%doc t2-services/t2-touchid/README.md
%{_bindir}/t2-touchid
%{_libexecdir}/t2-touchid/network-setup
%{_unitdir}/t2-touchid-network-setup.service
%dir %{_unitdir}/kait2en-t2-touchid.service.d
%{_unitdir}/kait2en-t2-touchid.service.d/10-network-setup.conf
%{_unitdir}/kait2en-t2-touchid.service
%dir %{_unitdir}/fprintd.service.d
%{_unitdir}/fprintd.service.d/kait2en-t2-touchid.conf
%{_datadir}/dbus-1/system.d/org.kait2en.TouchId.conf
%config(noreplace) %{_sysconfdir}/kait2en/t2-touchid.conf
%{_datadir}/selinux/packages/kait2en-t2-touchid.pp
%{_prefix}/lib/NetworkManager/system-connections/t2-touchid.nmconnection
