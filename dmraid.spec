#
# Conditional build:
%bcond_without	initrd	# without initrd version
%bcond_without	selinux	# build without SELinux support (needs selinux-disabled device-mapper)
#
Summary:	Device-mapper RAID tool
Summary(pl.UTF-8):	Narzędzie do RAID-u opartego o device-mapper
Name:		dmraid
Version:	1.0.0
%define	_rc	rc13
Release:	0.%{_rc}.1
License:	GPL
Group:		Base
Source0:	http://people.redhat.com/~heinzm/sw/dmraid/src/%{name}-%{version}.%{_rc}.tar.bz2
# Source0-md5:	a2a8948de7717e2e76a1291fc1daf9d1
Patch0:		%{name}-selinux-static.patch
Patch1:		%{name}-fix.patch
Patch2:		%{name}-optflags.patch
Patch3:		%{name}-as-needed.patch
URL:		http://people.redhat.com/~heinzm/sw/dmraid/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	device-mapper-devel >= 1.01.01
%if %{with initrd}
BuildRequires:	device-mapper-static >= 1.02.05-0.4
BuildRequires:	glibc-static
%{?with_selinux:BuildRequires:	libselinux-static}
%{?with_selinux:BuildRequires:	libsepol-static}
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%description initrd
Statically linked version of dmraid utility.

%description initrd -l pl.UTF-8
Statycznie skonsolidowana wersja programu narzędziowego dmraid.

%prep
%setup -q -n %{name}
mv */* ./
%{?with_selinux:%patch0 -p2}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
cp -f /usr/share/automake/config.sub autoconf
%{__aclocal}
%{__autoconf}

%if %{with initrd}
%configure \
	--enable-static_link
%{__make} -j1
cp -f tools/dmraid{,-initrd}
%{__make} clean
%endif

%configure \
	--enable-shared_lib
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	includedir=$RPM_BUILD_ROOT%{_includedir} \
	libdir=$RPM_BUILD_ROOT%{_libdir} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	sbindir=$RPM_BUILD_ROOT%{_sbindir}

%if %{with initrd}
install -D tools/dmraid-initrd $RPM_BUILD_ROOT/sbin/dmraid-initrd
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README TODO doc/dmraid_design.txt
%attr(755,root,root) %{_sbindir}/dmraid
%attr(755,root,root) %{_libdir}/libdmraid.so.*.*.*
%{_mandir}/man8/*

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
%attr(755,root,root) /sbin/dmraid-initrd
%endif
