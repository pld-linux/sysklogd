%define mjrver	1.3
%define minver	31

Summary:     	Linux system and kernel logger
Summary(de): 	Linux-System- und Kerner-Logger 
Summary(fr): 	Le système Linux et le logger du noyau
Summary(pl): 	Programy loguj±ce zdarzenia w systemie i kernelu Linuxa
Summary(tr): 	Linux sistem ve çekirdek kayýt süreci
Name:        	sysklogd
Version:     	%{mjrver}.%{minver}
Release:    	7
Copyright:   	GPL
Group:       	Daemons
Group(pl):	Serwery
Source0:     	ftp://sunsite.unc.edu/pub/Linux/system/daemons/%{name}-%{mjrver}-%{minver}.tar.gz
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
BuildRoot:   	/tmp/%{name}-%{version}-root

%description
This is the Linux system and kernel logging program. It is run as a daemon
(background process) to log messages to different places. These are usually
things like sendmail logs, security logs, and errors from other daemons.

%description -l de
Dies ist das Linux-System- und Kernel-Protokollierprogramm. Es wird als
Dämon (Hintergrundprozeß) ausgeführt und protokolliert verschiedene
Meldungen. Es protokolliert z.B. sendmail- und Sicherheits-Protokolle und
Fehler von anderen Dämonen.

%description -l fr
Programme de trace du sytème Linux et du noyau. Il est lancé en démon
(processus en arrière plan) pour stocker les messages à différents endroits.
Ce sont généralement des choses comme les traces de sendmail, de sécurité et
d'erreurs d'autres démons. I

%description -l pl
Pakiet ten zawiera programy które s± uruchamiane jako demony i s³u¿± do
logowania zadrzeñ w systemie i w kernelu Linuxa. Same logi mog± byæ
sk³adowane w ró¿nych miejscach (zdalnie i lokalnie). Przewa¿nie do logów
trawiaj± informacje o odbieranej i wysy³anej poczcie np. z sendmaila,
zdarzenia dotycz±ce bezpieczeñstwa systemu, a tak¿e informacje o b³êdach z
innchy demonów.

%description -l tr
Bu paket, Linux sistemi ve çekirdeði için kayýt tutan programý içerir.
Deðiþik yerlerde mesajlarýn kayýtlarýný tutmak içýn arkaplanda koþturulur.
Bu mesajlar, sendmail, güvenlik ve diðer sunucu süreçlerinin hatalarýyla
ilgili mesajlardýr.

%prep
%setup -q -n %{name}-%{mjrver}-%{minver}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1 
%patch5 -p1 
%patch6 -p1

%build
make OPTIMIZE="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d,logrotate.d} \
	$RPM_BUILD_ROOT/usr/{bin,man/man{5,8},sbin} \
	$RPM_BUILD_ROOT/dev

make install DESTDIR=$RPM_BUILD_ROOT
install %{SOURCE1} $RPM_BUILD_ROOT/etc/syslog.conf

install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/syslog
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/syslog
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/sysklogd

mkfifo $RPM_BUILD_ROOT/dev/log

strip $RPM_BUILD_ROOT/usr/sbin/*

gzip -9nf $RPM_BUILD_ROOT/usr/man/man[58]/* \
	 ANNOUNCE NEWS Sysklogd-*.lsm

%post
for n in /var/log/{messages,secure,maillog,spooler}
do
	[ -f $n ] && continue
	touch $n
	chmod 600 $n
done

/sbin/chkconfig --add syslog
if test -r /var/run/syslogd.pid
	then /etc/rc.d/init.d/syslog restart >&2
fi

%preun
if [ $1 = 0 ]; then
	/etc/rc.d/init.d/syslog stop >&2
	/sbin/chkconfig --del syslog
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {ANNOUNCE,NEWS,Sysklogd-*.lsm}.gz
%config %verify(not mtime md5 size) /etc/syslog.conf
%config %verify(not mtime md5 size) /etc/sysconfig/sysklogd
%attr(600,root,root) /etc/logrotate.d/syslog
%attr(744,root,root) /etc/rc.d/init.d/syslog
%attr(755,root,root) /usr/sbin/*
%attr(644,root,root) /usr/man/man[58]/*
%attr(666,root,root) %ghost /dev/log

%changelog
* Thu Apr 29 1999 Artur Frysiak <wiget@pld.org.pl>
  [1.3.31-7]
- upgraded to 1.3-31
- gzipping docs
- added /dev/log as %ghost

* Sat Nov 28 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
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
- removed /usr/man/man[58] directories from packge,
- added %verify rule for /etc/syslog.conf %config file,
- added gzipping man pages,
- removed making /etc/rc.d/rc?.d/* symlinks because
  /etc/rc.d/init.d/syslog support chkconfig.

* Thu Nov 12 1998 Jeff Johnson <jbj@redhat.com>
- plug potential buffer overflow.

* Tue Aug 11 1998 Jeff Johnson <jbj@redhat.com>
- add %clean

* Tue Aug  4 1998 Chris Adams <cadams@ro.com>
- only log to entries that are USER_PROCESS (fix #822)

* Mon Jul 27 1998 Jeff Johnson <jbj@redhat.com>
- remove RPM_BUILD_ROOT from %post

* Wed Apr 29 1998 Cristian Gafton <gafton@redhat.com>
- patch to support Buildroot
- package is now buildrooted

* Wed Apr 29 1998 Michael K. Johnson <johnsonm@redhat.com>
- Added exit patch so that a normal daemon exit is not flagged as an error.

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Oct 29 1997 Donnie Barnes <djb@redhat.com>
- added (missingok) to init symlinks

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- added status|restart support to syslog.init
- added chkconfig support
- various spec file cleanups

* Tue Jun 17 1997 Erik Troan <ewt@redhat.com>
- built against glibc
