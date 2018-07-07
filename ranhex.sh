#!/bin/bash
#
## ranhex.sh - creates random names for temp files
#
## # said name is piped to stdout
## ##
#
## ranhex.sh -c <alternate-tmp-dir>
## ##-- This creates a file with said name at /tmp
## ##--		OR at a user-defined path

#output from urandom
DICK=$(echo `head -c 8 /dev/urandom | xxd` | \
	sed -n '/\w*[[:xdigit:]]\w*/{h;x;p};/\"/d')

#remove all garbage
declare -u BPX=$(echo -e \
	"sz=\"$DICK\".split(' ')\ndel sz[0:1]\ndel sz[4:5]\nprint(\"%s%s%s%s\" % (sz[0],sz[1],sz[2],sz[3]))\n" | \
	python3 -)

#create our tempfile name from the random hexa numerii
RANDOM_HXX=`echo -e "rh$BPX\x2Etmp"`
RANDOM_HEX="$RANDOM_HXX"
export RANDOM_HEX
echo $RANDOM_HEX

#
## HANDLE CREATION OF THE TMPFILE IF -c IS PASSEF
#
if [ "$1" != "" ]; then
	####
	#
	# -c flag creates the file at /tmp or the passed path
	#
	####
	if [[ "$1" == "-c" ]]; then
		if [ "$2" != "" ]; then
			if [ -d "$2" ]; then
				HAVE_SLASH="y"
				export HAVE_SLASH
				declare -i Z=$(expr `AA="x"; dirname $2$AA` = `AB="/x"; dirname $2$AB`)
				if [[ $Z -lt 1 ]]; then
					unset $HAVE_SLASH
				fi
				if [ -z `echo $HAVE_SLASH` ]; then
					OUT_DIRECTORY=$(echo -e "$2/")
					export OUT_DIRECTORY
				else
					OUT_DIRECTORY="$2"
					export OUT_DIRECTORY
				fi
			else
				# # AVOID FAILURES # #
				# # # do not create dirs not in ur ~ if non-su
				if [[ $(id -u) -gt 0 && "$2" =~ \/$(id -un)+ ]]; then
					mkdir -p $2; pushd $2 >/dev/null
					OUT_DIRECTORY=$(echo -e "`pwd`/")
					export OUT_DIRECTORY
					popd >/dev/null
				else
					OUT_DIRECTORY="/tmp/"
					export OUT_DIRECTORY
				fi
			fi

		elif [ "$2" == "" ]; then
			OUT_DIRECTORY="/tmp/"
			export OUT_DIRECTORY
		fi

		touch $OUT_DIRECTORY$RANDOM_HEX
	fi
fi

