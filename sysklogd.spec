Summary:	Linux system and kernel logger
Summary(de):	Linux-System- und Kerner-Logger
Summary(fr):	Le système Linux et le logger du noyau
Summary(pl):	Programy loguj±ce zdarzenia w systemie i j±drze Linuksa
Summary(tr):	Linux sistem ve çekirdek kayýt süreci
Name:		sysklogd
Version:	1.4.1
Release:	6
License:	GPL
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery
Source0:	http://www.ibiblio.org/pub/Linux/system/daemons/sysklogd-1.4.1.tar.gz
Source1:	syslog.conf
Source2:	syslog.init
Source3:	syslog.logrotate
Source4:	syslog.sysconfig
Source5:	klogd.init
Source6:	klogd.sysconfig
Source7:	syslogd-listfiles.sh
Source8:	syslogd-listfiles.8
Patch0:		%{name}-alpha.patch
Patch1:		%{name}-alphafoo.patch
Patch2:		%{name}-opt.patch
Patch3:		%{name}-glibc.patch
Patch4:		%{name}-sparc.patch
Patch5:		%{name}-install.patch
Patch6:		%{name}-utmp-process.patch
Patch7:		%{name}-openlog.patch
Patch8:		%{name}-ksyms.patch
Patch9:		%{name}-nullterm.patch
URL:		http://www.infodrom.ffis.de/sysklogd/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_exec_prefix	/
%define		_bindir		/usr/bin
%define		_sysconfdir	/etc

%description
This is the Linux system and kernel logging program. It is run as a
daemon (background process) to log messages to different places. These
are usually things like sendmail logs, security logs, and errors from
other daemons.

%description -l de
Dies ist das Linux-System- und Kernel-Protokollierprogramm. Es wird
als Dämon (Hintergrundprozeß) ausgeführt und protokolliert
verschiedene Meldungen. Es protokolliert z.B. sendmail- und
Sicherheits-Protokolle und Fehler von anderen Dämonen.

%description -l fr
Programme de trace du sytème Linux et du noyau. Il est lancé en démon
(processus en arrière plan) pour stocker les messages à différents
endroits. Ce sont généralement des choses comme les traces de
sendmail, de sécurité et d'erreurs d'autres démons. I

%description -l pl
Pakiet ten zawiera programy, które s± uruchamiane jako demony i s³u¿±
do logowania zdarzeñ w systemie i w kernelu Linuksa. Same logi mog±
byæ sk³adowane w ró¿nych miejscach (zdalnie i lokalnie). Przewa¿nie do
logów trafiaj± informacje o odbieranej i wysy³anej poczcie np. z
sendmaila, zdarzenia dotycz±ce bezpieczeñstwa systemu, a tak¿e
informacje o b³êdach z innych demonów.

%description -l tr
Bu paket, Linux sistemi ve çekirdeði için kayýt tutan programý içerir.
Deðiþik yerlerde mesajlarýn kayýtlarýný tutmak içýn arkaplanda
koþturulur. Bu mesajlar, sendmail, güvenlik ve diðer sunucu
süreçlerinin hatalarýyla ilgili mesajlardýr.

%package -n syslog
Summary:	Linux system logger
Summary(de):	Linux-System-Logger
Summary(pl):	Program loguj±cy zdarzenia w systemie Linux
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery
Prereq:		/sbin/chkconfig
Prereq:		fileutils
Prereq:		rc-scripts >= 0.2.0
Requires:	SysVinit >= 2.76-12
Requires:	klogd
Requires:	logrotate >= 3.2-3
Requires:	psmisc >= 20.1
Provides:	syslogdaemon
Obsoletes:	sysklogd
Obsoletes:	syslog-ng

%description -n syslog
This is the Linux system logging program. It is run as a daemon
(background process) to log messages to different places. These are
usually things like sendmail logs, security logs, and errors from
other daemons.

%description -n syslog -l pl
Pakiet ten zawiera program, który jest uruchamiany jako demon i s³u¿y
do logowania zdarzeñ w systemie Linux. Same logi mog± byæ sk³adowane
w ró¿nych miejscach (zdalnie i lokalnie). Przewa¿nie do logów trafiaj±
informacje o odbieranej i wysy³anej poczcie np. z sendmaila, zdarzenia
dotycz±ce bezpieczeñstwa systemu, a tak¿e informacje o b³êdach z
innych demonów.

%package -n klogd
Summary:	Linux kernel logger
Summary(de):	Linux-Kerner-Logger
Summary(pl):	Program loguj±cy zdarzenia w j±drze Linuksa
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery
Prereq:		/sbin/chkconfig
Prereq:		rc-scripts >= 0.2.0
Obsoletes:	sysklogd

%description -n klogd
This is the Linux kernel logging program. It is run as a daemon
(background process) to log messages from kernel.

%description -n klogd -l pl
Pakiet ten zawiera program, który jest uruchamiany jako demon i s³u¿y
do logowania komunikatów j±dra Linuksa.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

%build
%{__make} \
	OPTIMIZE="%{rpmcflags}" \
	LDFLAGS=%{rpmldflags}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d,logrotate.d} \
	$RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,8},%{_bindir}} \
	$RPM_BUILD_ROOT/{dev,var/log}

%{__make} install \
	BINDIR=$RPM_BUILD_ROOT%{_sbindir} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/syslog.conf

install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/syslog
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/syslog
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/syslog
install %{SOURCE5} $RPM_BUILD_ROOT/etc/rc.d/init.d/klogd
install %{SOURCE6} $RPM_BUILD_ROOT/etc/sysconfig/klogd

install %{SOURCE7} $RPM_BUILD_ROOT%{_bindir}/syslogd-listfiles
install %{SOURCE8} $RPM_BUILD_ROOT%{_mandir}/man8

for n in messages secure maillog spooler kernel
do
	> $RPM_BUILD_ROOT/var/log/$n
done

echo .so sysklogd.8 > $RPM_BUILD_ROOT%{_mandir}/man8/syslogd.8

gzip -9nf ANNOUNCE NEWS README* CHANGES

%post -n syslog
for n in /var/log/{messages,secure,maillog,spooler,kernel}
do
	[ -f $n ] && continue
	> $n
	chmod 640 $n
done

/sbin/chkconfig --add syslog
if [ -f /var/lock/subsys/syslog ]; then
	/etc/rc.d/init.d/syslog restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/syslog start\" to start syslog daemon." 1>&2
fi
if [ -f /var/lock/subsys/klogd ]; then
	/etc/rc.d/init.d/klogd restart 1>&2
fi

%preun -n syslog
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/syslog ]; then
		/etc/rc.d/init.d/syslog stop 1>&2
	fi
	/sbin/chkconfig --del syslog
fi

%post -n klogd
/sbin/chkconfig --add klogd
if [ -f /var/lock/subsys/klogd ]; then
	/etc/rc.d/init.d/klogd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/klogd start\" to start kernel daemon." 1>&2
fi

%preun -n klogd
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/klogd ]; then
		/etc/rc.d/init.d/klogd stop 1>&2
	fi
	/sbin/chkconfig --del klogd
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files -n syslog
%defattr(644,root,root,755)
%doc {ANNOUNCE,NEWS,CHANGES,README*}.gz

%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/*.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/syslog
%attr(640,root,root) /etc/logrotate.d/syslog
%attr(754,root,root) /etc/rc.d/init.d/syslog

%attr(640,root,root) %ghost /var/log/*

%attr(755,root,root) %{_sbindir}/syslogd
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man5/*
%{_mandir}/man8/sys*

%files -n klogd
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/klogd
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/klogd

%attr(755,root,root) %{_sbindir}/klogd

%{_mandir}/man8/klog*
