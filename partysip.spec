# TODO:
# - separate plugin/libs packages
Summary:	A modular SIP proxy server
Summary(pl):	Modularny serwer proxy SIP
Name:		partysip
Version:	0.5.3
Release:	0.9
License:	LGPL
Group:		Networking/Daemons
Source0:	http://savannah.gnu.org/download/partysip/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-DESTDIR_fix.patch
Patch1:		%{name}-config_location.patch
URL:		http://www.partysip.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libosip-devel >= 0.8.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Partysip is a modular SIP proxy server. It can be used as a registrar
and a stateless and stateful SIP server. New capabilities, such as
instant messaging and answering machines, can be added by plugins.

%description -l pl
partysip jest modularnym serwerem proxy SIP. Mo¿e byæ u¿ywany jako
serwer rejestr oraz jako bezstanowy lub obs³uguj±cy stany serwer SIP.
Nowe mo¿liwo¶ci, takie jak przekazywanie wiadomo¶ci i automaty
odpowiadaj±ce, mog± byæ dodane przez wtyczki.

%package devel
Summary:	Header files for a modular SIP proxy server
Summary(pl):	Pliki nag³ówkowe dla modularnego serwera proxy SIP
Group:		Developement
Requires:	%{name} = %{version}

%description devel
Header files for partysip.

%description -l pl devel
Pliki nag³ówkowe dla partysip.

%package static
Summary:	Static libraries for a modular SIP proxy server
Summary(pl):	Statyczne biblioteki dla modularnego serwera proxy SIP
Group:		Developement
Requires:	%{name} = %{version}

%description static
Static libraries for a modular SIP proxy server partysip.

%description -l pl static
Statyczne biblioteki dla modularnego serwera proxy SIP partysip.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
rm -f missing
%{__aclocal} -I scripts
%{__autoconf}
%{__automake}
%configure \
	--sysconfdir=/etc/partysip \
	--disable-debug \
	--disable-trace

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{sysconfig,rc.d/init.d}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

# temporary useless
#install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}

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
%config(noreplace) %{_sysconfdir}/partysip/*.conf
%attr(755,root,root) %{_libdir}/*.so
%attr(644,root,root) %{_libdir}/*.la
%attr(755,root,root) %{_libdir}/partysip/*.so
%attr(644,root,root) %{_libdir}/partysip/*.la
%attr(755,root,root) %{_bindir}/partysip
%config(noreplace) /etc/sysconfig/%{name}
#%attr(754,root,root) /etc/rc.d/init.d/%{name}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/partysip-config
%{_includedir}/partysip/*.h
%{_includedir}/ppl/*.h

%files static
%defattr(644,root,root,755)
%attr(644,root,root) %{_libdir}/*.a
%attr(644,root,root) %{_libdir}/partysip/*.a
