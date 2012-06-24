%define		source	1.3-31

Summary:     	Linux system and kernel logger
Summary(de): 	Linux-System- und Kerner-Logger 
Summary(fr): 	Le syst�me Linux et le logger du noyau
Summary(pl): 	Programy loguj�ce zdarzenia w systemie i kernelu Linuxa
Summary(tr): 	Linux sistem ve �ekirdek kay�t s�reci
Name:        	sysklogd
Version:     	1.3.31
Release:    	8
Copyright:   	GPL
Group:       	Daemons
Group(pl):	Serwery
Source0:     	ftp://ftp.infodrom.nort.de/pub/pub/people/joey/%{name}-%{source}.tar.gz
Source1:     	syslog.conf
Source2:     	syslog.init
Source3:     	syslog.logrotate
Source4:     	sysklogd.sysconfig
Patch0:      	sysklogd-alpha.patch
Patch1:      	sysklogd-alphafoo.patch
Patch2:      	sysklogd-opt.patch
Patch3:      	sysklogd-daemon.patch
Patch4:      	sysklogd-glibc.patch
Patch5:      	sysklogd-sparc.patch
Patch6:      	sysklogd-install.patch
Prereq:      	fileutils
Prereq:		/sbin/chkconfig
Requires:     	logrotate
Requires:	logrotate >= 3.2-3
BuildRoot:   	/tmp/%{name}-%{version}-root

%description
This is the Linux system and kernel logging program. It is run as a daemon
(background process) to log messages to different places. These are usually
things like sendmail logs, security logs, and errors from other daemons.

%description -l de
Dies ist das Linux-System- und Kernel-Protokollierprogramm. Es wird als
D�mon (Hintergrundproze�) ausgef�hrt und protokolliert verschiedene
Meldungen. Es protokolliert z.B. sendmail- und Sicherheits-Protokolle und
Fehler von anderen D�monen.

%description -l fr
Programme de trace du syt�me Linux et du noyau. Il est lanc� en d�mon
(processus en arri�re plan) pour stocker les messages � diff�rents endroits.
Ce sont g�n�ralement des choses comme les traces de sendmail, de s�curit� et
d'erreurs d'autres d�mons. I

%description -l pl
Pakiet ten zawiera programy kt�re s� uruchamiane jako demony i s�u�� do
logowania zadrze� w systemie i w kernelu Linuxa. Same logi mog� by�
sk�adowane w r�nych miejscach (zdalnie i lokalnie). Przewa�nie do log�w
trawiaj� informacje o odbieranej i wysy�anej poczcie np. z sendmaila,
zdarzenia dotycz�ce bezpiecze�stwa systemu, a tak�e informacje o b��dach z
innchy demon�w.

%description -l tr
Bu paket, Linux sistemi ve �ekirde�i i�in kay�t tutan program� i�erir.
De�i�ik yerlerde mesajlar�n kay�tlar�n� tutmak i��n arkaplanda ko�turulur.
Bu mesajlar, sendmail, g�venlik ve di�er sunucu s�re�lerinin hatalar�yla
ilgili mesajlard�r.

%prep
%setup -q -n %{name}-%{source}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1 
%patch5 -p1 
%patch6 -p1

%build
make  OPTIMIZE="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d,logrotate.d} \
	$RPM_BUILD_ROOT/usr/{bin,share/man/man{5,8},sbin} \
	$RPM_BUILD_ROOT/{dev,var/log}

make \
    INSTALL="/bin/install" \
    DESTDIR=$RPM_BUILD_ROOT \
    MANDIR=$RPM_BUILD_ROOT%{_mandir} \
    install

install %{SOURCE1} $RPM_BUILD_ROOT/etc/syslog.conf

install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/syslog
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/syslog
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/sysklogd

install debian/syslogd-listfiles $RPM_BUILD_ROOT%{_bindir}
install debian/*.8 $RPM_BUILD_ROOT%{_mandir}/man8

for n in messages secure maillog spooler kernel wtmp; do
touch $RPM_BUILD_ROOT/var/log/$n ; done

echo .so sysklogd.8 > $RPM_BUILD_ROOT%{_mandir}/man8/syslogd.8

strip $RPM_BUILD_ROOT%{_sbindir}/*

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man[58]/* \
	 ANNOUNCE NEWS Sysklogd-*.lsm

%post
for n in /var/log/{messages,secure,maillog,spooler,kernel,wtmp}
do
	[ -f $n ] && continue
	touch $n
	chmod 640 $n
done

/sbin/chkconfig --add syslog
if test -r /var/run/syslog.pid; then
	 /etc/rc.d/init.d/syslog restart >&2
else
	echo "Run \"/etc/rc.d/init.d/syslog start\" to start syslog daemon."
fi

%preun
if [ "$1" = "0" ]; then
	/etc/rc.d/init.d/syslog stop >&2
	/sbin/chkconfig --del syslog
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {ANNOUNCE,NEWS,Sysklogd-*.lsm}.gz

%attr(640,root,root) %config %verify(not mtime md5 size) /etc/*.conf
%attr(640,root,root) %config %verify(not mtime md5 size) /etc/sysconfig/*
%attr(640,root,root) /etc/logrotate.d/syslog
%attr(755,root,root) /etc/rc.d/init.d/syslog
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /var/log/*

%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man[58]/*

%changelog
* Thu May 20 1999 Wojtek �lusarczyk <wojtek@shadow.eu.org>
  [1.3.31-8]
- some fixes for correct build,
- added forgotten /var/log/ files,
- removed /dev/log -- now again in dev package
- fixed %post script
- changed URL.

* Thu Apr 29 1999 Artur Frysiak <wiget@pld.org.pl>
  [1.3.31-7]
- upgraded to 1.3-31
- gzipping docs
- added /dev/log as %ghost

* Thu Dec 31 1998 Wojtek �lusarczyk <wojtek@shadow.eu.org>
  [1.3.30-3d]
- added sys(k)logd patch prepared by Florian La Rosch <florian@suse.de>,
- fixed syslod.conf,
- added missing debian script.

* Sat Nov 28 1998 Tomasz K�oczko <kloczek@rudy.mif.pg.gda.pl>
  [1.3-27]
- added -q %setup parametr,
- added using %{SOURCE#} macros in %install,
- enhanced /etc/rc.d/init.d/syslog script:
  -- added reload feacture,
  -- added config fields,
  -- added using /etc/sysconfig/sysklogd file with handling variables:
  --- ENABLE_RECEIVE_FROM_NET,
  --- HOSTLIST,
  --- DOMAINLIST,
  --- MARK_TIMESTAMP,
- enhanced %post, %preun sections functionality (automatic restart
  syslog on upgrade),
- added pl translation,
- removed INSTALL, README* from %doc,
- removed %{_mandir}/man[58] directories from packge,
- added %verify rule for /etc/syslog.conf %config file,
- added gzipping man pages,
- removed making /etc/rc.d/rc?.d/* symlinks because
  /etc/rc.d/init.d/syslog support chkconfig.

* Mon Sep 21 1998 Wojtek �lusarczyk <wojtek@shadow.eu.org>
  [1.3.30-1d]
- translation modified for pl,
- fixed files permissions,
- added /var/log/* files,
- build from non root's account,
  by Maciej W. R�ycki <macro@ds2.pg.gda.pl>
- added small glibc patch.

* Thu Jun 19 1998 Wojtek �lusarczyk <wojtek@shadow.eu.org>
  [1.3.25-3d]
- build against glibc-2.1,
- minor patch and spec's corrections.
- start at RH spec file.
