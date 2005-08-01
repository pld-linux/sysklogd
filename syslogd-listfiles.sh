#!/bin/sh
CONF="/etc/syslog.conf"
OPT_DAILY=1
OPT_ALL=0
OPT_AUTH=0
OPT_NEWS=0

usage ()
{
	local VER=$(echo '$Revision$' | awk '{print $2}')
	cat 2>&1 <<EOF
PLD Linux syslogd-listfiles $VER.  Copyright (C) 2000 S.Zagrodzki,
Copyright (C) 2005 Elan Ruusamäe.  This is free software; see the GNU General
Public Licence version 2 or later for copying conditions.  There is NO
warranty.

Usage: syslogd-listfiles <options>
Options: -f file        specifies another syslog.conf file
         -a | --all     list all files (including news)
         --auth         list all files containing auth.<some prio>
         --news         include news logfiles, too
         -w | --weekly  use weekly pattern instead of daily
EOF
# TODO from original .pl file:
#	--ignore-size  don't rotate files which got too large
#	--large nnn	define what is large in bytes (default: 10MB)
#	-s pattern	skip files matching pattern
}

while [ -n "$1" ]; do
	case "$1" in
	-f)
		shift
		CONF="$1"
		shift
		;;
	--weekly|-w)
		OPT_DAILY=0
		shift
		;;
	--all|-a)
		OPT_ALL=1
		shift
		;;
	--auth)
		OPT_AUTH=1
		shift
		;;
	--news)
		OPT_NEWS=1
		shift
		;;
	*)
		usage
		exit 1
		;;
	esac
done

# some magic is appearing here, line continuations are parsed by shell so we
# need not to take extra care on that.
egrep -v '^(#|[ \t]*$)' "$CONF" | while read line; do
	echo "$line"
done | awk -vopt_news=$OPT_NEWS -vopt_all=$OPT_ALL -vopt_auth=$OPT_AUTH -vopt_daily=$OPT_DAILY '{
	file = $NF;
	sub("^-", "", file);

	# skip /dev and not full paths (skips effectively remote logging and program pipes)
	if (file ~ /^\/dev/ || file !~ /^\//) {
		next;
	}
	pat = substr($0, 0, length($0) - length($NF));

	# These files are handled by news.daily from INN, so we ignore them
	if (!opt_news && (pat ~ /news\.(\*|crit|err|info|notice)/)) {
		next;
	}

	output = 0;
	if (opt_all) {
		output = 1;
	} else if (opt_auth) {
		if (pat ~ /auth[^\.]*\./ && pat !~ /auth[^\.]*\.none/) {
			output = 1;
		}
	} else {
		everything = (pat ~ /\*\.\*/);
		if ((everything && opt_daily)) {
			output = 1
		}
		if ((!everything && !opt_daily)) {
			output = 1
		}
	}

	if (output) {
		print file;
	}
}'
