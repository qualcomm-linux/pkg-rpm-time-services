Name:           time-services
Version:        0.1.2
Release:        1%{?dist}
Summary:        Qualcomm time daemon

License:        BSD-3-Clause
URL:            https://github.com/quic/time-services
Source0:        https://github.com/quic/time-services/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(glib-2.0)
# Known gap: no RPM/dnf-repo for qmi-framework exists yet in the
# qualcomm-linux org (only Debian packaging in pkg-qmi-framework). dnf
# builddep will fail to resolve this until a qmi-framework RPM is published
# and registered via this workflow's `extra-repo` input.
BuildRequires:  pkgconfig(qmi-framework)
BuildRequires:  systemd-rpm-macros

Requires(pre):    systemd
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description
The time-services daemon synchronises time from the modem to the applications
processor and maintains time offsets across reboots, once set from any
source.

%prep
%autosetup

%build
autoreconf --install
%configure CFLAGS="%{optflags} -DSYSLOG_ENABLE"
%make_build

%install
%make_install

mkdir -p %{buildroot}%{_unitdir}
cat > %{buildroot}%{_unitdir}/%{name}.service <<'EOF'
[Unit]
Description=time serviced Service
SourcePath=/usr/bin/time_daemon
After= var-lib.mount mount-var-lib.service

[Service]
User=rtc
Group=rtc
Restart=always
RemainAfterExit=yes
CapabilityBoundingSet=CAP_SYS_TIME
AmbientCapabilities=CAP_SYS_TIME
ExecStartPre=+mkdir -p /var/lib/time
ExecStart=/usr/bin/time_daemon

[Install]
WantedBy=multi-user.target
EOF

mkdir -p %{buildroot}%{_sysusersdir}
cat > %{buildroot}%{_sysusersdir}/%{name}.conf <<'EOF'
u rtc - "Time daemon user"
EOF

mkdir -p %{buildroot}%{_udevrulesdir}
cat > %{buildroot}%{_udevrulesdir}/70-%{name}.rules <<'EOF'
ACTION=="add", KERNEL=="rtc0", SUBSYSTEM=="rtc", OWNER="rtc", GROUP="rtc", MODE="0640"
EOF

%pre
%sysusers_create_compat %{name}.conf

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license LICENSE
%doc README.md
%{_bindir}/time_daemon
%{_unitdir}/%{name}.service
%{_sysusersdir}/%{name}.conf
%{_udevrulesdir}/70-%{name}.rules

%changelog
* Wed Aug 05 2026 Jairaj Solanki <jsolanki@qti.qualcomm.com> - 0.1.2-1
- Initial RPM packaging, ported from the Debian/Ubuntu packaging in
  qualcomm-linux/pkg-time-services.
