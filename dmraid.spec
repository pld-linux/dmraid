#
# Conditional build:
%bcond_without	initrd	# without initrd version
#
Summary:	Device-mapper RAID tool
Summary(pl):	Narzêdzie do RAID-u opartego o device-mapper
Name:		dmraid
Version:	1.0.0
Release:	0.rc6.2
License:	GPL
Group:		Base
Source0:	http://people.redhat.com/~heinzm/sw/dmraid/src/%{name}-%{version}.rc6.tar.bz2
# Source0-md5:	8383b009ac61674fae6de442c6dba910
Patch0:		dmraid-selinux-static.patch
Patch1:		dmraid-bigendian-fix.patch
URL:		http://people.redhat.com/~heinzm/sw/dmraid/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	device-mapper-devel
%{?with_initrd:BuildRequires:	device-mapper-static}
BuildRequires:	gettext-devel
%{?with_initrd:BuildRequires:	glibc-static}
%{?with_initrd:BuildRequires:	libselinux-static}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DMRAID supports device discovery, set activation and display of
properties for ATARAID on Linux >= 2.4 using device-mapper.

%description -l pl
DMRAID obs³uguje wykrywanie urz±dzeñ, ustawianie aktywacji i
wy¶wietlanie w³a¶ciwo¶ci ATARAID-u na Linuksie >= 2.4 przy u¿yciu
device-mappera.

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
%patch0 -p1
%patch1 -p1

%build
cp -f /usr/share/automake/config.sub autoconf
%{__aclocal}
%{__autoconf}

%if %{with initrd}
%configure \
	--enable-static_link
%{__make}
cp -f tools/dmraid{,-initrd}
%{__make} clean
%endif

%configure 
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -D tools/dmraid $RPM_BUILD_ROOT%{_sbindir}/dmraid
%{?with_initrd:install -D tools/dmraid-initrd $RPM_BUILD_ROOT/sbin/dmraid-initrd}
install -D man/dmraid.8 $RPM_BUILD_ROOT%{_mandir}/man8/dmraid.8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README TODO doc/dmraid_design.txt
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*

%if %{with initrd}
%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) /sbin/*
%endif
