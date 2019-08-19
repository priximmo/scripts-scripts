#!/bin/bash

if [[ $# < 2 ]]; then
	echo -e "Symbolic link to dest.\nUsage: $0 dir1 dir2 ... dest"
	exit 1
fi

declare -i index=0
declare dest=""
for dir in $@; do
	index=index+1
	if [[ $index == $# ]]; then
		dest=$dir
	fi
done

for dir in $@; do
	if [ $dir != $dest ]; then
		for file in `ls $dir`; do
			ln -s $dir/$file $dest/$file
		done
	fi
done

