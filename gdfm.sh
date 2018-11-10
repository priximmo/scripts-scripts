#!/bin/bash
# gdfm.sh --- Git Diff From Master
#
if [ -z $1 ]; then
	echo -e "git diff from master"
	echo -e "diffs branch from the current branch...\n"
	echo -e "Usage: $0 <branch>\n"
	exit 1
fi

MASTER=`git status | awk '{if(i==0){print $3;i=1;}}'`
TOP_REF=`git reflog show ${MASTER} | awk '{if(i==0){print $1;i=1;}}'`

git checkout $1
git diff $TOP_REF .
git checkout $MASTER
