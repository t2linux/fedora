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
Source2:        80-t2-touchid.preset
Source3:        10-t2-touchid.conf
ExclusiveArch:  x86_64

BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  make
BuildRequires:  systemd-rpm-macros
BuildRequires:  checkpolicy
BuildRequires:  policycoreutils-devel

Requires:       fprintd
Requires:       fprintd-pam
Requires:       libfprint
Requires:       dbus
Requires:       NetworkManager
Requires:       systemd
Requires:       authselect
Requires:       bash
Requires:       iproute
Requires:       iputils
Requires(post): policycoreutils
Requires(preun): policycoreutils
Requires(postun): policycoreutils

%description
Apple T2 Touch ID bridge for stock Fedora fprintd, libfprint and pam_fprintd.
BridgeXPC support is linked into the daemon.

%prep
%forgeautosetup -p1

pushd t2-services/t2-touchid
%cargo_prep
popd

%generate_buildrequires
pushd t2-services/t2-touchid
%cargo_generate_buildrequires
popd

%build
pushd t2-services/t2-touchid
%cargo_build
popd

make -C t2-services/t2-touchid/integration/selinux

%check
pushd t2-services/t2-touchid
%cargo_test
popd

%install
make -C t2-services/t2-touchid install \
    PREFIX=/usr \
    DESTDIR=%{buildroot} \
    SYSTEMD_UNIT_DIR=%{_unitdir} \
    DATADIR=%{_datadir} \
    SYSCONFDIR=%{_sysconfdir}

install -Dm0755 %{SOURCE1} \
    %{buildroot}%{_libexecdir}/t2-touchid/network-setup

sed -i '/^ExecStart=/i ExecStartPre=%{_libexecdir}/t2-touchid/network-setup' \
    %{buildroot}%{_unitdir}/kait2en-t2-touchid.service

install -Dm0644 \
    t2-services/t2-touchid/integration/selinux/kait2en-t2-touchid.pp \
    %{buildroot}%{_datadir}/selinux/packages/kait2en-t2-touchid.pp

install -Dm0644 %{SOURCE2} \
    %{buildroot}%{_prefix}/lib/systemd/system-preset/80-t2-touchid.preset

install -Dm0644 %{SOURCE3} \
    %{buildroot}%{_prefix}/lib/NetworkManager/conf.d/10-t2-touchid.conf

%post
%systemd_post kait2en-t2-touchid.service

/usr/sbin/semodule -X 200 -i \
    %{_datadir}/selinux/packages/kait2en-t2-touchid.pp >/dev/null 2>&1 || :

if [ -d /run/t2-touchid ]; then
    /usr/sbin/restorecon -RF /run/t2-touchid >/dev/null 2>&1 || :
fi

if [ -d /run/systemd/system ]; then
    if /usr/bin/systemctl is-active --quiet dbus-broker.service; then
        /usr/bin/systemctl reload dbus-broker.service >/dev/null 2>&1 || :
    elif /usr/bin/systemctl is-active --quiet dbus.service; then
        /usr/bin/systemctl reload dbus.service >/dev/null 2>&1 || :
    fi
fi

%posttrans
if /usr/bin/authselect current --raw >/dev/null 2>&1; then
    if ! /usr/bin/authselect is-feature-enabled with-fingerprint >/dev/null 2>&1; then
        if ! /usr/bin/authselect enable-feature with-fingerprint -b >/dev/null 2>&1; then
            echo "t2-touchid: could not enable authselect feature with-fingerprint; enable it manually." >&2
        fi
    fi
    /usr/bin/authselect apply-changes >/dev/null 2>&1 || :
else
    echo "t2-touchid: authselect is not managing PAM; fingerprint PAM was not changed." >&2
fi

if [ -d /run/systemd/system ] && /usr/bin/systemctl is-active --quiet fprintd.service; then
    /usr/bin/systemctl restart fprintd.service >/dev/null 2>&1 || :
fi

%preun
%systemd_preun kait2en-t2-touchid.service

%postun
%systemd_postun_with_restart kait2en-t2-touchid.service

if [ "$1" -eq 0 ]; then
    /usr/sbin/semodule -X 200 -r kait2en-t2-touchid >/dev/null 2>&1 || :
fi

if [ -d /run/systemd/system ] && /usr/bin/systemctl is-active --quiet fprintd.service; then
    /usr/bin/systemctl restart fprintd.service >/dev/null 2>&1 || :
fi

%files
%license LICENSE
%doc t2-services/t2-touchid/README.md
%{_bindir}/t2-touchid
%{_libexecdir}/t2-touchid/network-setup
%{_unitdir}/kait2en-t2-touchid.service
%dir %{_unitdir}/fprintd.service.d
%{_unitdir}/fprintd.service.d/kait2en-t2-touchid.conf
%{_datadir}/dbus-1/system.d/org.kait2en.TouchId.conf
%config(noreplace) %{_sysconfdir}/kait2en/t2-touchid.conf
%{_datadir}/selinux/packages/kait2en-t2-touchid.pp
%{_prefix}/lib/systemd/system-preset/80-t2-touchid.preset
%{_prefix}/lib/NetworkManager/conf.d/10-t2-touchid.conf
