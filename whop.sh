#!/bin/sh
# whop.sh - WHO on mah Port xxx
#

lsof | grep $1 > ~/f.log; cat ~/f.log | less; rm ~/f.log

