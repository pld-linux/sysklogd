%define		source	1.3-31
Summary:     	Linux system and kernel logger
Summary(de): 	Linux-System- und Kerner-Logger 
Summary(fr): 	Le système Linux et le logger du noyau
Summary(pl): 	Programy loguj±ce zdarzenia w systemie i kernelu Linuxa
Summary(tr): 	Linux sistem ve çekirdek kayýt süreci
Name:        	sysklogd
Version:     	1.3.31
Release:    	12
Copyright:   	GPL
Group:       	Daemons
Group(pl):	Serwery
URL:     	ftp://ftp.infodrom.nort.de/pub/pub/people/joey/
Source0:	%{name}-%{source}.tar.gz
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
Patch7:      	sysklogd-utmp-process.patch
Prereq:      	fileutils
Prereq:		/sbin/chkconfig
Requires:	logrotate >= 3.2-3
Requires:	SysVinit >= 2.76-12
BuildRoot:	/tmp/%{name}-%{version}-root

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
%setup -q -n %{name}-%{source}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1 
%patch5 -p1 
%patch6 -p1
%patch7 -p1

%build
make  OPTIMIZE="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d,logrotate.d} \
	$RPM_BUILD_ROOT/usr/{bin,share/man/man{5,8},sbin} \
	$RPM_BUILD_ROOT/{dev,var/log}

make \
    INSTALL=`whereis install | awk '{ print $2} '` \
    DESTDIR=$RPM_BUILD_ROOT \
    MANDIR=$RPM_BUILD_ROOT%{_mandir} \
    install

install %{SOURCE1} $RPM_BUILD_ROOT/etc/syslog.conf

install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/syslog
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/syslog
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/sysklogd

install debian/syslogd-listfiles $RPM_BUILD_ROOT%{_bindir}
install debian/*.8 $RPM_BUILD_ROOT%{_mandir}/man8

for n in messages secure maillog spooler kernel; do
touch $RPM_BUILD_ROOT/var/log/$n ; done

echo .so sysklogd.8 > $RPM_BUILD_ROOT%{_mandir}/man8/syslogd.8

strip $RPM_BUILD_ROOT%{_sbindir}/*

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man[58]/* \
	 ANNOUNCE NEWS Sysklogd-*.lsm

%post
for n in /var/log/{messages,secure,maillog,spooler,kernel}
do
	[ -f $n ] && continue
	touch $n
	chmod 640 $n
done

/sbin/chkconfig --add syslog
if [ -f /var/lock/subsys/syslog ]; then
    /etc/rc.d/init.d/syslog restart &>/dev/null
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
* Fri May 28 1999 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [1.3.31-11]
- based on RH spec,
- spec rewrited by PLD team.
