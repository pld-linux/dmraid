Summary:	Device-mapper RAID tool
Summary(pl):	Narzêdzie do RAID-u opartego o device-mapper
Name:		dmraid
Version:	1.0.0
Release:	0.rc5.2
License:	GPL
Group:		Base
Source0:	http://people.redhat.com/~heinzm/sw/dmraid/src/%{name}-%{version}-rc5f.tar.bz2
# Source0-md5:	086fc75133a0fb0ffe95bd9a7fb8a52f
Patch0:		dmraid-selinux-static.patch
URL:		http://people.redhat.com/~heinzm/sw/dmraid/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	device-mapper-devel
BuildRequires:	device-mapper-static
BuildRequires:	gettext-devel
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
Static version of dmraid

%description initrd -l pl
Wersja statyczna dmraid

%prep
%setup -q -n %{name}
mv */* ./
%patch0 -p1

%build
cp -f /usr/share/automake/config.sub autoconf
%{__gettextize}
%{__aclocal}
%{__autoconf}
%configure --enable-static_link
%{__make}
cp tools/dmraid{,-initrd}

%{__make} clean
%configure 
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -D tools/dmraid $RPM_BUILD_ROOT%{_sbindir}/dmraid
install -D tools/dmraid-initrd $RPM_BUILD_ROOT/sbin/dmraid-initrd
install -D man/dmraid.8 $RPM_BUILD_ROOT%{_mandir}/man8/dmraid.8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README TODO doc/dmraid_design.txt
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*

%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) /sbin/*
