Summary:	A modular SIP proxy server
Summary(pl):	Modularny serwer proxy SIP
Name:		partysip
Version:	0.4.7
Release:	0.1
License:	LGPL
Group:		Networking/Daemons
Source0:	http://savannah.gnu.org/download/partysip/%{name}-%{version}.tar.gz
URL:		http://www.partysip.org/
#BuildRequires:	autoconf
#BuildRequires:	automake
#BuildRequires:	libtool
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

%prep
%setup -q

%build
#rm -f missing
#%{__libtoolize}
#aclocal
#%{__autoconf}
#%{__automake}
%configure2_13 \
	--disable-debug \
	--disable-trace

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/{sysconfig,rc.d/init.d},/var/log/}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

#install contrib/PLD/.init $RPM_BUILD_ROOT/etc/rc.d/init.d/
#install contrib/.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/

touch $RPM_BUILD_ROOT/var/log/dcd/dcd.log
%clean
rm -rf $RPM_BUILD_ROOT

%post
#/sbin/chkconfig --add
#if [ -f /var/lock/subsys/ ]; then
#        /etc/rc.d/init.d/ restart 1>&2
#else
#        echo "Run \"/etc/rc.d/init.d/ start\" to start Daemon."
#fi

%preun
#if [ "$1" = "0" ]; then
#        if [ -f /var/lock/subsys/ ]; then
#               /etc/rc.d/init.d/ stop 1>&2
#        fi
#        /sbin/chkconfig --del
#fi

%files
%defattr(644,root,root,755)
#%doc AUTHORS BUGS FAQ NEWS README TODO doc/*.txt doc/*.html
#%config(noreplace) %{_sysconfdir}/.conf
#%config(noreplace) /etc/sysconfig/
#%attr(755,root,root) %{_sbindir}/
#%attr(754,root,root) /etc/rc.d/init.d/
#%attr(644,daemon,root) /var/log/.log
#%attr(755,daemon,root) %dir /var/log//
#%dir /var/log/archiv/
