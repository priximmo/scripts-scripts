#!/bin/bash

##
## ## FUNCTIONS
##

function uid_check {
	declare -i CURUID=`id -u`
	if [ $CURUID -ne 0 ]; then
		echo Run\ these\ as\ root.
		/bin/false; exit 1
	fi
}

## ## ENTRY
echo -e "chroot jail creation scriptkit\n"
echo FILES\ TO\ ALTER\ BEHAVIOR
echo -e "~/.chrt_bins\t-\tBINARIES TO INCLUDE IN JAIL\n"


uid_check
