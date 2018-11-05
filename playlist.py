#!/usr/bin/env python3
# coding=utf-8
#
###
# i sorted my collection by gid since none of my FM's could
# do metadata... lol wtf
#
# clicking & selecting with a laptop mouse is pain
#
import sys
import os
from pathlib import Path
from grp import getgrnam

# return a list of ONLY files matching gid
def sort_by_group(wa, wd, gid):
	sorty = []
	for i in range(0,len(wd)):
		with Path('%s/%s' % (wa, wd[i])) as filo:
			if os.stat(filo.resolve(strict=True))[5] == gid:
				sorty.append(str(filo.resolve(strict=True)))
	return sorty

# does what it says
def create_playlist(fname, contents):
	with open(fname, 'w', newline='\n') as f:
		for c in contents:
			f.write('{0}\n'.format(c))
	return

###
### GIDS, how I sorted my pr0n
###
gid_clip = getgrnam('clip')[2]

#get all files in current dir
we_at = os.getcwd()
we_dir = os.listdir(path=we_at)
we_dir = [f for f in we_dir if f is not '.' or f is not '..']

print("Working in %s" % we_at)
print("Creating clip playlist...")
create_playlist('clip.m3u', sort_by_group(we_at, we_dir, gid_clip))
print("DONE. Fuck the mouse! >:(")

sys.exit(0)

