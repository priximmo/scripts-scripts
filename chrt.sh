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

function user_group_add {
	if id -nu $2 1>/dev/null 2>1; then
		declare -x user=`id -nu $2`
		declare -x group`id -ng $3`
	elif id -u $2 1>/dev/null 2>1; then
		/bin/true
	else
		echo -e "Pass text for non created user/groups."
		/bin/false; exit 1
	fi
	
	if [[ -n "$2" && -n "$3" ]]; then
		declare -i uid=`id -u "$2" || echo -1`
		declare -i gid=`id -g "$3" || echo -1`
		if [[ $uid -eq -1 || $gid -eq -1 ]]; then
			groupadd $3; adduser $2; adduser $2 $3
		fi
		if test -z "$user"; then
			declare -x user=`id -nu $uid`
		fi
		if test -z "$group"; then
			declare -x group=`id -ng $gid`
		fi
		
		unset uid
		unset gid
	fi
	
	declare -x CHRT_CHROOT_PREFIX="$1"
	export CHRT_CHROOT_PREFIX

	echo -e "$user with group $group going to jail under: $CHRT_CHROOT_PREFIX\n"
}

function make_dirs_in_chroot {
	# /
	mkdir -p $CHRT_CHROOT_PREFIX/bin 
	mkdir -p $CHRT_CHROOT_PREFIX/dev
	mkdir -p $CHRT_CHROOT_PREFIX/etc 
	mkdir -p $CHRT_CHROOT_PREFIX/lib
	ln -s $CHRT_CHROOT_PREFIX/lib lib64 1>/dev/null 2>1
	# /usr
	mkdir -p $CHRT_CHROOT_PREFIX/usr
	mkdir -p $CHRT_CHROOT_PREFIX/usr/bin 
	mkdir -p $CHRT_CHROOT_PREFIX/usr/lib 
	ln -s $CHRT_CHROOT_PREFIX/lib lib64 1>/dev/null 2>1
	ln -s $CHRT_CHROOT_PREFIX/usr/lib $CHRT_CHROOT_PREFIX/usr/li64 1>/dev/null 2>1 
	chmod -R 0775 $CHRT_CHROOT_PREFIX
	chown -R root:root $CHRT_CHROOT_PREFIX 
	ls -laZ $CHRT_CHROOT_PREFIX
}

function determine_binaries_deps {
	make_dirs_in_chroot
	if stat "$HOME"/".chrt_bins" 1>/dev/null 2>1; then
		echo "using current binaries list"
		export BINSF="${HOME}/.chrt_bins"
		/bin/true
	else
		echo -e "INPUT REQUIRED BINARIES (eg: /bin/bash): CTRL-D when done\n" ; \
		cat - > /tmp/chrt_binaries.tmp
		mv /tmp/chrt_binaries.tmp "${HOME}/.chrt_bins"
	fi

	array=($(cat $BINSF))
	pwd=`pwd`
	python3 $pwd/chrt/copy_deps.py ${array[@]} auto /lib/x86_64-linux-gnu/ 
}



## ## ENTRY

echo -e "chroot jail creation scriptkit\n"
echo FILES\ TO\ ALTER\ BEHAVIOR
echo -e "~/.chrt_bins\t-\tBINARIES TO INCLUDE IN JAIL\n"

export "CHRT_CHROOT_PREFIX=$1"

uid_check
user_group_add $1 $2 $3 # dir, usr, grp
determine_binaries_deps



#cp -fv /etc/{group,prelink.cache,services,adjtime,shells,gshadow,shadow,hosts.deny,localtime,nsswitch.conf,nscd.conf,prelink.conf,protocols,hosts,passwd,ld.so.cache,ld.so.conf,resolv.conf,host.conf}
