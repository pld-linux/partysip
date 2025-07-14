# TODO:
# - separate plugin/libs packages
Summary:	A modular SIP proxy server
Summary(pl.UTF-8):	Modularny serwer proxy SIP
Name:		partysip
Version:	0.6.0
Release:	1
License:	LGPL
Group:		Networking/Daemons
Source0:	http://savannah.gnu.org/download/partysip/%{name}-%{version}.tar.gz
# Source0-md5:	55a0bbf61df281393a093513e9a44808
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-DESTDIR_fix.patch
URL:		http://www.partysip.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libosip-devel >= 0.8.9
BuildRequires:	libtool
Requires(post):	/sbin/ldconfig
#Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Partysip is a modular SIP proxy server. It can be used as a registrar
and a stateless and stateful SIP server. New capabilities, such as
instant messaging and answering machines, can be added by plugins.

%description -l pl.UTF-8
partysip jest modularnym serwerem proxy SIP. Może być używany jako
serwer rejestr oraz jako bezstanowy lub obsługujący stany serwer SIP.
Nowe możliwości, takie jak przekazywanie wiadomości i automaty
odpowiadające, mogą być dodane przez wtyczki.

%package devel
Summary:	Header files for a modular SIP proxy server
Summary(pl.UTF-8):	Pliki nagłówkowe dla modularnego serwera proxy SIP
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for partysip.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla partysip.

%package static
Summary:	Static libraries for a modular SIP proxy server
Summary(pl.UTF-8):	Statyczne biblioteki dla modularnego serwera proxy SIP
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static libraries for a modular SIP proxy server partysip.

%description static -l pl.UTF-8
Statyczne biblioteki dla modularnego serwera proxy SIP partysip.

%prep
%setup -q
%patch -P0 -p1

%build
rm -f missing
%{__libtoolize}
%{__aclocal} -I scripts
%{__autoconf}
%{__automake}
%configure \
	--disable-debug \
	--disable-trace

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# temporary useless
#install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

rm -f $RPM_BUILD_ROOT%{_libdir}/partysip/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
#/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/%{name} start\" to start partysip."
fi

%preun
#/sbin/chkconfig --del %{name}
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/%{name} ]; then
		/etc/rc.d/init.d/%{name} stop 1>&2
	fi
fi

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README TODO
%dir %{_sysconfdir}/partysip
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/partysip/*.conf
%attr(755,root,root) %{_bindir}/partysip
%attr(755,root,root) %{_libdir}/libppl.so.*.*.*
%dir %{_libdir}/partysip
%attr(755,root,root) %{_libdir}/partysip/*.so
# needed or not?
%{_libdir}/partysip/*.la
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
#%attr(754,root,root) /etc/rc.d/init.d/%{name}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/partysip-config
%attr(755,root,root) %{_libdir}/libppl.so
%{_libdir}/libppl.la
%{_includedir}/partysip
%{_includedir}/ppl

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
