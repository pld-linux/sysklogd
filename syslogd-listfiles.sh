#!/bin/sh
CONF="/etc/syslog.conf"
OPT_DAILY=1
OPT_ALL=0
OPT_AUTH=0
OPT_NEWS=0

usage ()
{
	cat > /dev/stderr <<EOF
PLD GNU/Linux syslogd-listfiles =VER=.  Copyright (C) 2000 S.Zagrodzki.
This is free software; see the GNU General Public Licence
version 2 or later for copying conditions.  There is NO warranty.

Usage: syslogd-listfiles <options>
Options: -f file        specifies another syslog.conf file
         -a | --all     list all files (including news)
         --auth         list all files containing auth.<some prio>
         --news         include news logfiles, too
         -w | --weekly  use weekly pattern instead of daily
EOF
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

while read LINIA; do
	if echo "$LINIA" | grep -qv "^#" && [ -n "$LINIA" ]; then
		LINIA="`echo "$LINIA" | sed 's/^[[:space:]]*//'`"
		if [ "$LINIA" = "${LINIA%\\}" ]; then
			LINIA="`echo "$LINIA" | sed \
				-e "s/[[:space:]]\+/	/g" \
				-e 's/	-/	/g' \
			`"
			if 
				echo "$LINIA" | grep -qv "	/dev" &&\
				echo "$LINIA" | grep -qv "	\*"
			then
				PAT="`echo "$LINIA" | cut -f 1`"
				FILE="`echo "$LINIA" | cut -f 2`"
				OUTPUT=0
				if
					echo "$PAT" |\
					grep -qv 'news\.\(crit|err|notice\)' ||\
					[ "$OPT_NEWS" = "1" ]
				then
					if [ "$OPT_ALL" = "1" ]; then
						OUTPUT=1
					elif [ "$OPT_AUTH" = "1" ]; then
						echo "$PAT" |\
						grep 'auth[^\.]*\.' |\
						grep -qv 'auth[^\.]*\.none' &&\
						OUTPUT=1
					else
						echo "$PAT" | grep -q '\*\.\*'
						I="$?"
						if [ "$I" = "0" ] &&\
							[ "$OPT_DAILY" = "1" ]
						then
							OUTPUT=1
						elif [ "$I" = "1" ] &&\
							[ "$OPT_DAILY" = "0" ]
						then
							OUTPUT=1
						fi
					fi
				fi
				if [ "$OUTPUT" = "1" ]; then
					echo "$FILE"
				fi
			fi
		fi
	fi
done < "$CONF"
