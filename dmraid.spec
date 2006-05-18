#
# Conditional build:
%bcond_without	initrd	# without initrd version
#
%define	_rc rc10
%define	_rel 1.3
Summary:	Device-mapper RAID tool
Summary(pl):	Narzêdzie do RAID-u opartego o device-mapper
Name:		dmraid
Version:	1.0.0
Release:	0.%{_rc}.%{_rel}
License:	GPL
Group:		Base
Source0:	http://people.redhat.com/~heinzm/sw/dmraid/src/%{name}-%{version}.%{_rc}.tar.bz2
# Source0-md5:	0206f8166bfdc370c4ee8efcb35af111
Patch0:		%{name}-selinux-static.patch
URL:		http://people.redhat.com/~heinzm/sw/dmraid/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	device-mapper-devel >= 1.01.01
%{?with_initrd:BuildRequires:	device-mapper-static >= 1.02.05-0.4}
%{?with_initrd:BuildRequires:	glibc-static}
%{?with_initrd:BuildRequires:	libselinux-static}
%{?with_initrd:BuildRequires:	libsepol-static}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DMRAID supports device discovery, set activation and display of
properties for ATARAID on Linux >= 2.4 using device-mapper.

%description -l pl
DMRAID obs³uguje wykrywanie urz±dzeñ, ustawianie aktywacji i
wy¶wietlanie w³a¶ciwo¶ci ATARAID-u na Linuksie >= 2.4 przy u¿yciu
device-mappera.

%package devel
Summary:	Header files for dmraid library
Summary(pl):	Pliki nag³ówkowe biblioteki dmraid
Group:		Development/Libraries

%description devel
dmraid-devel provides a library interface for RAID device discovery,
RAID set activation and display of properties for ATARAID volumes.

%description devel -l pl
Ten pakiet udostêpnia interfejs biblioteczny do wykrywania urz±dzeñ
RAID, w³±czania zestawu RAID i wy¶wietlania w³a¶ciwo¶ci wolumenów
ATARAID.

%package static
Summary:	Static library for dmraid
Summary(pl):	Statyczna biblioteka dmraid
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
dmraid-static provides a library interface for RAID device discovery,
RAID set activation and display of properties for ATARAID volumes.

%description static -l pl
Ten pakiet udostêpnia statyczn± bibliotekê do wykrywania urz±dzeñ
RAID, w³±czania zestawu RAID i wy¶wietlania w³a¶ciwo¶ci wolumenów
ATARAID.

%package initrd
Summary:	Device-mapper RAID tool - statically linked version
Summary(pl):	Narzêdzie do RAID-u opartego o device-mapper - wersja statyczna
Group:		Base

%description initrd
Statically linked version of dmraid utility.

%description initrd -l pl
Statycznie skonsolidowana wersja programu narzêdziowego dmraid.

%prep
%setup -q -n %{name}
mv */* ./
%patch0 -p2

%build
cp -f /usr/share/automake/config.sub autoconf
%{__aclocal}
%{__autoconf}

%if %{with initrd}
%configure \
	--enable-static_link
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"
cp -f tools/dmraid{,-initrd}
%{__make} clean
%endif

%configure
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

install -D tools/dmraid $RPM_BUILD_ROOT%{_sbindir}/dmraid
%{?with_initrd:install -D tools/dmraid-initrd $RPM_BUILD_ROOT/sbin/dmraid-initrd}
install -D man/dmraid.8 $RPM_BUILD_ROOT%{_mandir}/man8/dmraid.8

install -d $RPM_BUILD_ROOT{%{_includedir}/dmraid,%{_libdir}}
install include/dmraid/*.h $RPM_BUILD_ROOT%{_includedir}/dmraid
# install the static library
install lib/libdmraid.a $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README TODO doc/dmraid_design.txt
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/dmraid

%files static
%defattr(644,root,root,755)
%{_libdir}/libdmraid.a

%if %{with initrd}
%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) /sbin/*
%endif
