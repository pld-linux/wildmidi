#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	alsa		# ALSA support (OpenAL/OSS otherwise)
%bcond_with	openal		# OpenAL support if not ALSA (OSS otherwise)
#
Summary:	MIDI player using pat sound sets
Summary(pl.UTF-8):	Odtwarzacz MIDI wykorzystujący zestawy dźwięków pat
Name:		wildmidi
Version:	0.4.6
Release:	1
License:	LGPL v3+ (library), GPL v3+ (player)
Group:		Libraries
Source0:	https://downloads.sourceforge.net/wildmidi/%{name}-%{version}.tar.gz
# Source0-md5:	769606325dc7a54a52555fddc3323dbc
URL:		https://wildmidi.sourceforge.net/
%{?with_openal:BuildRequires:	OpenAL-devel}
%{?with_alsa:BuildRequires:	alsa-lib-devel >= 1.0.1}
BuildRequires:	cmake >= 3.4
# for wildmidi player
%{?with_alsa:Requires:	alsa-lib >= 1.0.1}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
WildMidi is a wave table player that uses GUS pat sound sets to play
MIDI file. The WildMidi player is the frontend, and is only designed
to pass information to the core library and output any audio data the
library returns.

The core of the project, libWildMidi, is the work horse behind the
player. It's capable of multithreading and multiprocessing of MIDI
files, allowing for the mixing of multiple MIDI file at any one time
if someone had a desire to do so. This library is what turns the MIDI
files into audio data using the GUS pat sets.

%description -l pl.UTF-8
WildMidi to odtwarzacz plików MIDI wykorzystujący zestawy dźwięków pat
z GUS-a. WildMidi to frontend służący tylko do przekazywania
informacji do głównej biblioteki i wyprowadzania danych dźwiękowych
zwracanych przez bibliotekę.

Serce projektu, libWildMidi, to silnik stojący za odtwarzaczem. Jest w
stanie przetwarzać pliki MIDI wielowątkowo, pozwalając na miksowanie
wielu plików MIDI. Biblioteka jest tym, co zamienia pliki MIDI na dane
dźwiękowe przy użyciu zestawów pat z GUS-a.

%package devel
Summary:	Header files for WildMidi library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki WildMidi
License:	LGPL v3+
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for WildMidi library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki WildMidi.

%package static
Summary:	Static WildMidi library
Summary(pl.UTF-8):	Statyczna biblioteka WildMidi
License:	LGPL v3+
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static WildMidi library.

%description static -l pl.UTF-8
Statyczna biblioteka WildMidi.

%prep
%setup -q

%build
install -d build
cd build
%cmake .. \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	%{?with_alsa:-DWANT_ALSA=ON} \
	%{!?with_openal:-DWANT_OPENAL=ON} \
	%{!?with_alsa:%{!?with_openal:-DWANT_OSS=ON}} \
	%{?with_static_libs:-DWANT_STATIC=ON} \
	-DWANT_PLAYERSTATIC=OFF
	
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/wildmidi
%attr(755,root,root) %{_libdir}/libWildMidi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libWildMidi.so.2
%{_mandir}/man1/wildmidi.1*
%{_mandir}/man5/wildmidi.cfg.5*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libWildMidi.so
%{_includedir}/wildmidi_lib.h
%{_pkgconfigdir}/wildmidi.pc
%{_libdir}/cmake/WildMidi
%{_mandir}/man3/WildMidi_*.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libWildMidi.a
%endif
