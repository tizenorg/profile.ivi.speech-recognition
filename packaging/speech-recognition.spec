%{!?_with_debug:%{!?_without_debug:%define _with_debug 1}}
%{!?_with_sphinx:%{!?_without_sphinx:%define _with_sphinx 1}}
%{!?_with_festival:%{!?_without_festival:%define _with_festival 1}}
%{!?_with_wrt:%{!?_without_wrt:%define _with_wrt 1}}
%{!?_with_dbus:%{!?_without_dbus:%define _without_dbus 1}}
%{!?_with_systemd:%{!?_without_systemd:%define _with_systemd 1}}

Summary: Speech recognition service for Tizen
Name: speech-recognition
Version: 0.0.5
Release: 0
License: BSD-3-Clause
Group: Base/Utilities
URL: https://github.com/otcshare/speech-recognition
Source0: %{name}-%{version}.tar.gz

BuildRequires: pkgconfig(libpulse)

# Termporarily had to replace these with explicit package-dependencies,
# because the murphy pkgconfig files lack the correct version (needs to
# be fixed) and now we need a new enough murphy with native-types support.
# Switch these back once this is fixed on the murphy side.

# BuildRequires: pkgconfig(murphy-common) >= 0.0.42
# BuildRequires: pkgconfig(murphy-pulse) >= 0.0.42
# BuildRequires: pkgconfig(murphy-glib) >= 0.0.42

BuildRequires: murphy-devel >= 0.0.43
BuildRequires: murphy-glib-devel >= 0.0.43
BuildRequires: murphy-pulse-devel >= 0.0.43

BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(json)
%if %{?_with_sphinx:1}%{!?_with_sphinx:0}
BuildRequires: pkgconfig(pocketsphinx)
BuildRequires: pkgconfig(sphinxbase)
%endif
%if %{?_with_festival:1}%{!?_with_festival:0}
BuildRequires: festival-devel
Requires: festival
%endif
%if %{?_with_dbus:1}%{!?_with_dbus:0}
BuildRequires: pkgconfig(dbus-1)
%endif
Requires: pulseaudio
%if %{?_with_sphinx:1}%{!?_with_sphinx:0}
Requires: sphinxbase
Requires: pocketsphinx
%endif
%if %{?_with_systemd:1}%{!?_with_systemd:0}
BuildRequires: pkgconfig(libsystemd-daemon)
%endif

%description
SRS/Winthorpe speech recognition system service.

%package devel
Summary: The header files and libraries needed for SRS/Winthorpe clients
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
This package contains header files and libraries necessary for development.

%package tests
Summary: Various test binaries for SRS/Winthorpe
Group: Development/Debug
Requires: %{name} = %{version}

%description tests
This package contains various test binaries for SRS/Winthorpe.

%prep
%setup -q -n %{name}-%{version}

%build
%if %{?_with_debug:1}%{!?_with_debug:0}
export CFLAGS="-O0 -g3"
export CXXFLAGS="-O0 -g3"
V="V=1"
%endif

CONFIG_OPTIONS=""

%if %{?_with_sphinx:1}%{!?_with_sphinx:0}
CONFIG_OPTIONS="$CONFIG_OPTIONS --enable-sphinx"
%else
CONFIG_OPTIONS="$CONFIG_OPTIONS --disable-sphinx"
%endif

%if %{?_with_festival:1}%{!?_with_festival:0}
CONFIG_OPTIONS="$CONFIG_OPTIONS --enable-festival"
%else
CONFIG_OPTIONS="$CONFIG_OPTIONS --disable-festival"
%endif

%if %{?_with_wrt:1}%{!?_with_wrt:0}
CONFIG_OPTIONS="$CONFIG_OPTIONS --enable-wrt-client"
%else
CONFIG_OPTIONS="$CONFIG_OPTIONS --disable-wrt-client"
%endif

%if %{?_with_dbus:1}%{!?_with_dbus:0}
CONFIG_OPTIONS="$CONFIG_OPTIONS --enable-gpl --enable-dbus"
%else
CONFIG_OPTIONS="$CONFIG_OPTIONS --disable-dbus"
%endif

%if %{?_with_systemd:1}%{!?_with_systemd:0}
CONFIG_OPTIONS="$CONFIG_OPTIONS --enable-systemd"
%else
CONFIG_OPTIONS="$CONFIG_OPTIONS --disable-systemd"
%endif


./bootstrap && \
    %configure $CONFIG_OPTIONS && \
    make

%install
rm -fr $RPM_BUILD_ROOT

%make_install

# Install dictionaries, configuration and service files.
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir} \
    $RPM_BUILD_ROOT%{_sysconfdir}/speech-recognition \
    $RPM_BUILD_ROOT/lib/systemd/user \
    $RPM_BUILD_ROOT%{_datadir}/speech-recognition/dictionaries/demo \
    $RPM_BUILD_ROOT%{_libdir}/srs/scripts \
    $RPM_BUILD_ROOT%{_datadir}/dbus-1/services

/usr/bin/install -m 644 packaging/speech-recognition.conf \
    $RPM_BUILD_ROOT%{_sysconfdir}/speech-recognition
/usr/bin/install -m 644 packaging/speech-recognition.service \
    $RPM_BUILD_ROOT/lib/systemd/user
%if %{?_with_systemd:1}%{!?_with_systemd:0}
/usr/bin/install -m 644 packaging/speech-recognition.socket \
    $RPM_BUILD_ROOT/lib/systemd/user
%endif
/usr/bin/install -m 644 \
    -t $RPM_BUILD_ROOT%{_datadir}/speech-recognition/dictionaries/demo \
    dictionaries/demo/demo.*
/usr/bin/install -m 755 packaging/start-speech-service.sh \
     $RPM_BUILD_ROOT%{_libdir}/srs/scripts
/usr/bin/install -m 755 packaging/org.tizen.srs.service \
     $RPM_BUILD_ROOT%{_datadir}/dbus-1/services

%clean
rm -rf $RPM_BUILD_ROOT

%post
ldconfig
%if %{?_with_systemd:1}%{!?_with_systemd:0}
systemctl --user enable speech-recognition.socket
%endif

%preun
%if %{?_with_systemd:1}%{!?_with_systemd:0}
systemctl --user disable speech-recognition.socket
%endif

%postun
ldconfig

%files
%defattr(-,root,root,-)
%{_sbindir}/srs-daemon
%if %{?_with_dbus:1}%{!?_with_dbus:0}
%{_bindir}/srs-client
%endif
%{_libdir}/srs
%{_libdir}/libsrs*.so.*
%{_sysconfdir}/speech-recognition/speech-recognition.conf
%{_datadir}/speech-recognition/dictionaries
/lib/systemd/user/speech-recognition.service
%if %{?_with_systemd:1}%{!?_with_systemd:0}
/lib/systemd/user/speech-recognition.socket
%endif
%{_datadir}/dbus-1/services/org.tizen.srs.service

%files devel
%defattr(-,root,root,-)
%{_includedir}/srs
%{_libdir}/libsrs*.so
%{_libdir}/pkgconfig/srs*.pc

%files tests
%defattr(-,root,root,-)
%{_bindir}/srs-native-client
