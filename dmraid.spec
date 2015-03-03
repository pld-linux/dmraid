#
# Conditional build:
%bcond_with	initrd		# without initrd version
%bcond_with	dietlibc	# build initrd version with static glibc instead of dietlibc
%bcond_without	selinux		# build without SELinux support (needs selinux-disabled device-mapper)

%define		rel	2
%define		subver	rc16.3
Summary:	Device-mapper RAID tool
Summary(pl.UTF-8):	Narzędzie do RAID-u opartego o device-mapper
Name:		dmraid
Version:	1.0.0
Release:	0.%{subver}.%{rel}
License:	GPL v2+
Group:		Base
Source0:	http://people.redhat.com/~heinzm/sw/dmraid/src/%{name}-%{version}.rc16-3.tar.bz2
# Source0-md5:	819338fcef98e8e25819f0516722beeb
Patch0:		%{name}-selinux-static.patch
Patch1:		%{name}-optflags.patch
Patch2:		%{name}-unsigned.patch
Patch3:		%{name}-diet.patch
Patch4:		%{name}-format.patch
URL:		http://people.redhat.com/~heinzm/sw/dmraid/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	device-mapper-devel >= 1.02.02
BuildRequires:	zlib-devel
%if %{with initrd}
	%if %{with dietlibc}
BuildRequires:	device-mapper-dietlibc
BuildRequires:	dietlibc-static >= 2:0.31-5
	%else
BuildRequires:	device-mapper-static >= 1.02.05-0.4
BuildRequires:	glibc-static
BuildRequires:	udev-static
%if %{with selinux}
BuildRequires:	libselinux-static
BuildRequires:	libsepol-static
%endif
	%endif
%endif
%if %{with selinux}
BuildRequires:	libselinux-devel
BuildRequires:	libsepol-devel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
DMRAID supports device discovery, set activation and display of
properties for ATARAID on Linux >= 2.4 using device-mapper.

%description -l pl.UTF-8
DMRAID obsługuje wykrywanie urządzeń, ustawianie aktywacji i
wyświetlanie właściwości ATARAID-u na Linuksie >= 2.4 przy użyciu
device-mappera.

%package devel
Summary:	Header files for dmraid library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki dmraid
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
dmraid-devel provides a library interface for RAID device discovery,
RAID set activation and display of properties for ATARAID volumes.

%description devel -l pl.UTF-8
Ten pakiet udostępnia interfejs biblioteczny do wykrywania urządzeń
RAID, włączania zestawu RAID i wyświetlania właściwości wolumenów
ATARAID.

%package static
Summary:	Static library for dmraid
Summary(pl.UTF-8):	Statyczna biblioteka dmraid
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
dmraid-static provides a library interface for RAID device discovery,
RAID set activation and display of properties for ATARAID volumes.

%description static -l pl.UTF-8
Ten pakiet udostępnia statyczną bibliotekę do wykrywania urządzeń
RAID, włączania zestawu RAID i wyświetlania właściwości wolumenów
ATARAID.

%package initrd
Summary:	Device-mapper RAID tool - statically linked version
Summary(pl.UTF-8):	Narzędzie do RAID-u opartego o device-mapper - wersja statyczna
Group:		Base
Conflicts:	geninitrd < 10000.10

%description initrd
Statically linked version of dmraid utility.

%description initrd -l pl.UTF-8
Statycznie skonsolidowana wersja programu narzędziowego dmraid.

%prep
%setup -q -n %{name}
mv %{version}.*/dmraid/* .
%{?with_selinux:%patch0 -p2}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
cp -f /usr/share/automake/config.sub autoconf
%{__aclocal}
%{__autoconf}

%if %{with initrd}
%configure \
	%if %{with dietlibc}
	CC="diet %{__cc} %{rpmcflags} %{rpmldflags} -Os -static" \
	--disable-libselinux \
	--disable-libsepol \
	%else
		%if %{with selinux}
	--enable-libselinux \
	--enable-libsepol \
		%endif
	%endif
	--enable-static_link

%{__make} -j1
mv -f tools/dmraid dmraid-initrd
%{__make} clean
%endif

%configure \
	--with-usrlibdir=%{_libdir} \
	--disable-static_link \
	--enable-led \
	--enable-intel_led
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_lib}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_libdir}/libdmraid.so.* $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/$(cd $RPM_BUILD_ROOT/%{_lib} ; echo libdmraid.so.*.*.*) \
        $RPM_BUILD_ROOT%{_libdir}/libdmraid.so

%if %{with initrd}
install -d $RPM_BUILD_ROOT%{_libdir}/initrd
install -p dmraid-initrd $RPM_BUILD_ROOT%{_libdir}/initrd/dmraid
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG CREDITS KNOWN_BUGS README TODO doc/dmraid_design.txt
%attr(755,root,root) %{_sbindir}/dmevent_tool
%attr(755,root,root) %{_sbindir}/dmraid
%attr(755,root,root) /%{_lib}/libdmraid.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libdmraid.so.1
%attr(755,root,root) %{_libdir}/libdmraid-events-isw.so
%attr(755,root,root) %{_libdir}/device-mapper/libdmraid-events-isw.so
%{_mandir}/man8/dmevent_tool.8*
%{_mandir}/man8/dmraid.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdmraid.so
%{_includedir}/dmraid

%files static
%defattr(644,root,root,755)
%{_libdir}/libdmraid.a

%if %{with initrd}
%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/initrd/dmraid
%endif
