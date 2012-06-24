# TODO:
# - trigger for upgrade from inetutils-syslogd
Summary:	Linux system and kernel logger
Summary(de.UTF-8):   Linux-System- und Kerner-Logger
Summary(es.UTF-8):   Registrador de log del sistema linux
Summary(fr.UTF-8):   Le système Linux et le logger du noyau
Summary(pl.UTF-8):   Programy logujące zdarzenia w systemie i jądrze Linuksa
Summary(pt_BR.UTF-8):   Registrador de log do sistema linux
Summary(tr.UTF-8):   Linux sistem ve çekirdek kayıt süreci
Name:		sysklogd
Version:	1.4.1
Release:	21.20
License:	BSD/GPL
Group:		Daemons
Source0:	http://www.ibiblio.org/pub/Linux/system/daemons/%{name}-%{version}.tar.gz
# Source0-md5:	d214aa40beabf7bdb0c9b3c64432c774
Source1:	syslog.conf
Source2:	syslog.init
Source3:	syslog.logrotate
Source4:	syslog.sysconfig
Source5:	klogd.init
Source6:	klogd.sysconfig
Source7:	syslogd-listfiles.sh
Source8:	syslogd-listfiles.8
Patch0:		%{name}-cvs.patch
Patch1:		%{name}-bind.patch
Patch2:		%{name}-querymod.patch
Patch3:		%{name}-alpha.patch
Patch4:		%{name}-alphafoo.patch
Patch5:		%{name}-opt.patch
Patch6:		%{name}-glibc.patch
Patch7:		%{name}-sparc.patch
Patch8:		%{name}-install.patch
Patch9:		%{name}-openlog.patch
Patch10:	%{name}-security.patch
Patch11:	%{name}-fmt-string.patch
Patch12:	%{name}-SO_BSDCOMPAT.patch
Patch13:	%{name}-ksyms.patch
URL:		http://www.infodrom.org/projects/sysklogd/
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_exec_prefix	/
%define 	_bindir		/usr/sbin
%define 	_sbindir	/sbin

%description
This is the Linux system and kernel logging program. It is run as a
daemon (background process) to log messages to different places. These
are usually things like sendmail logs, security logs, and errors from
other daemons.

%description -l de.UTF-8
Dies ist das Linux-System- und Kernel-Protokollierprogramm. Es wird
als Dämon (Hintergrundprozeß) ausgeführt und protokolliert
verschiedene Meldungen. Es protokolliert z.B. sendmail- und
Sicherheits-Protokolle und Fehler von anderen Dämonen.

%description -l es.UTF-8
Este es el programa de log para el kernel y el sistema Linux. Se
ejecuta como un daemon (proceso en background) para registrar mensajes
en diferentes lugares. Estos son generalmente registros del sendmail,
seguridad, y mensajes de otros daemons.

%description -l fr.UTF-8
Programme de trace du sytème Linux et du noyau. Il est lancé en démon
(processus en arrière plan) pour stocker les messages à différents
endroits. Ce sont généralement des choses comme les traces de
sendmail, de sécurité et d'erreurs d'autres démons. I

%description -l pl.UTF-8
Pakiet ten zawiera programy, które są uruchamiane jako demony i służą
do logowania zdarzeń w systemie i w jądrze Linuksa. Same logi mogą być
składowane w różnych miejscach (zdalnie i lokalnie). Przeważnie do
logów trafiają informacje o odbieranej i wysyłanej poczcie np. z
sendmaila, zdarzenia dotyczące bezpieczeństwa systemu, a także
informacje o błędach z innych demonów.

%description -l pt_BR.UTF-8
Este é o programa de log para o kernel e o sistema Linux. Ele roda
como um daemon (processo em background) para registrar mensagens em
diferentes lugares. Estes são geralmente registros do sendmail,
segurança, e mensagens de outros daemons.

%description -l tr.UTF-8
Bu paket, Linux sistemi ve çekirdeği için kayıt tutan programı içerir.
Değişik yerlerde mesajların kayıtlarını tutmak içın arkaplanda
koşturulur. Bu mesajlar, sendmail, güvenlik ve diğer sunucu
süreçlerinin hatalarıyla ilgili mesajlardır.

%package -n syslog
Summary:	Linux system logger
Summary(de.UTF-8):   Linux-System-Logger
Summary(pl.UTF-8):   Program logujący zdarzenia w systemie Linux
License:	BSD
Group:		Daemons
Requires(post):	fileutils
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun):	rc-scripts >= 0.2.0
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/usr/lib/rpm/user_group.sh
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(pre):	/usr/sbin/usermod
Requires(triggerpostun):	sed >= 4.0
# for vservers we don't need klogd and syslog works without klogd
# (just it doesn't log kernel buffer into syslog)
# Requires:	klogd
Requires:	logrotate >= 3.2-3
Requires:	psmisc >= 20.1
Provides:	group(syslog)
Provides:	syslogdaemon
Provides:	user(syslog)
Obsoletes:	msyslog
Obsoletes:	sysklogd
Obsoletes:	syslog-ng

%description -n syslog
This is the Linux system logging program. It is run as a daemon
(background process) to log messages to different places. These are
usually things like sendmail logs, security logs, and errors from
other daemons.

%description -n syslog -l pl.UTF-8
Pakiet ten zawiera program, który jest uruchamiany jako demon i służy
do logowania zdarzeń w systemie Linux. Same logi mogą być składowane w
różnych miejscach (zdalnie i lokalnie). Przeważnie do logów trafiają
informacje o odbieranej i wysyłanej poczcie np. z sendmaila, zdarzenia
dotyczące bezpieczeństwa systemu, a także informacje o błędach z
innych demonów.

%package -n klogd
Summary:	Linux kernel logger
Summary(de.UTF-8):   Linux-Kerner-Logger
Summary(pl.UTF-8):   Program logujący zdarzenia w jądrze Linuksa
License:	GPL
Group:		Daemons
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun):	rc-scripts >= 0.2.0
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/usr/lib/rpm/user_group.sh
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(pre):	/usr/sbin/usermod
Provides:	group(syslog)
Provides:	user(syslog)
Obsoletes:	sysklogd

%description -n klogd
This is the Linux kernel logging program. It is run as a daemon
(background process) to log messages from kernel.

%description -n klogd -l pl.UTF-8
Pakiet ten zawiera program, który jest uruchamiany jako demon i służy
do logowania komunikatów jądra Linuksa.

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
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1

%build
%{__make} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

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

for n in debug kernel maillog messages secure syslog user spooler lpr daemon
do
	> $RPM_BUILD_ROOT/var/log/$n
done

echo .so sysklogd.8 > $RPM_BUILD_ROOT%{_mandir}/man8/syslogd.8

# our strip can't strip otherwise
chmod u+w $RPM_BUILD_ROOT%{_sbindir}/{klogd,syslogd}

%pre -n syslog
%groupadd -P syslog -g 18 syslog
%useradd -P syslog -u 18 -g syslog -c "Syslog User" syslog
%addusertogroup syslog logs

%post -n syslog
for n in /var/log/{cron,daemon,debug,kernel,lpr,maillog,messages,secure,spooler,syslog,user}; do
	if [ -f $n ]; then
		chown syslog:syslog $n
		continue
	else
		touch $n
		chmod 000 $n
		chown syslog:syslog $n
		chmod 640 $n
	fi
done

/sbin/chkconfig --add syslog
%service syslog restart "syslog daemon"
%service -q klogd restart

%preun -n syslog
if [ "$1" = "0" ]; then
	%service syslog stop
	/sbin/chkconfig --del syslog
fi

%postun -n syslog
if [ "$1" = "0" ]; then
	%userremove syslog
	%groupremove syslog
fi

%pre -n klogd
%groupadd -P klogd -g 18 syslog
%useradd -P klogd -u 18 -g syslog -c "Syslog User" syslog
%addusertogroup syslog logs

%post -n klogd
/sbin/chkconfig --add klogd
%service klogd restart "kernel logger daemon"

%preun -n klogd
if [ "$1" = "0" ]; then
	%service klogd stop
	/sbin/chkconfig --del klogd
fi

%postun -n klogd
if [ "$1" = "0" ]; then
	%userremove syslog
	%groupremove syslog
fi

%triggerpostun -- inetutils-syslogd
/sbin/chkconfig --del syslog
/sbin/chkconfig --add syslog
if [ -f /etc/syslog.conf.rpmsave ]; then
	mv -f /etc/syslog.conf{,.rpmnew}
	mv -f /etc/syslog.conf{.rpmsave,}
	echo "Moved /etc/syslog.conf.rpmsave to /etc/syslog.conf"
	echo "Original file from package is available as /etc/syslog.conf.rpmnew"
fi

%triggerpostun -n syslog -- syslog < 1.4.1-17.7
# remove any -a option from ADDITIONAL_SOCK
cp -f /etc/sysconfig/syslog{,.rpmsave}
sed -i -e '/^ADDITIONAL_SOCK=/s/-a //g' /etc/sysconfig/syslog

# reset config file permission, so people running with syslog uid can
# survive syslog reload
chgrp syslog /etc/syslog.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files -n syslog
%defattr(644,root,root,755)
%doc ANNOUNCE NEWS README* CHANGES
%attr(640,root,syslog) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/syslog
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/syslog
%attr(754,root,root) /etc/rc.d/init.d/syslog
%attr(640,root,root) %ghost /var/log/*
%attr(755,root,root) %{_sbindir}/syslogd
%attr(755,root,root) %{_bindir}/syslogd-listfiles
%{_mandir}/man5/*
%{_mandir}/man8/sys*

%files -n klogd
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/klogd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/klogd
%attr(755,root,root) %{_sbindir}/klogd
%{_mandir}/man8/klog*
