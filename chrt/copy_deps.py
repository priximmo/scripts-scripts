# coding=utf-8
import os
import sys
import re
import distutils.file_util as dufu
from subprocess import Popen, PIPE

CHROOT_PREFIX=""
LD_LIBRARY_LOC=""

# Zippify two lists and make 'em double-iterable
def pair_up(l1, l2, lengths=(0,0)):
	rv = []
	rx = []
	
	if not len(l1) == len(l2):
		if lengths[0] == 0 and lengths[1] == 0:
			raise ValueError
	
	for i in range(0, len(l1)):
		rv.append(l1[i])
		rx.append(l2[i])
	
	return zip(*(rv,rx))

def main (argc, argv):
	if argc < 4:
		raise RuntimeError
	
	# automate for CHRT script-kit
	if "auto" in argv[2]:
		arg2 = os.environ["CHRT_CHROOT_PREFIX"]
		if len(arg2) > 0 and not "auto" in arg2:
			where_to = arg2
		else:
			raise RuntimeError
	else:
		where_to = argv[2]
	
	###
	# *.py <needed binary> <CHROOT> <path to library files
	###
	what = argv[1]
	##  where_to = argv[2]
	CHROOT_PREFIX = where_to
	where_from = argv[3]
	LD_LIBRARY_LOC = where_from
	
	ldd = Popen(['ldd', what], stdout=PIPE)
	awk = Popen(['awk', '{print $1}'], stdin=ldd.stdout, stdout=PIPE, stderr=PIPE,universal_newlines=True)
	
	depends = awk.communicate()[0]
	
	# we get list of dep libs and empty list
	depends = depends.split("\n") # ldd output, copy from path
	depends2 = []                 # FQ'd libs path to copy from
	depends3 = []                 # copy to path
	dep_len = old_len = len(depends)
	
	# remove anything that's a full path to a file
	a, b = ("", "\'")
	for s in depends:
		if s == a:
			depends.remove(s)
		if b == a:
			depends.remove(s)
		
		# remove paths that are not lib names
		badname = re.match("^[(\/)(\/)].*", s)
		if badname is not None:
			depends.remove(s)
			depends2.append(s)
	
	# Concatenate where_from & lib names
	for i in range(0, len(depends)):
		p1 = re.match("(\/)+$", where_from, re.M)
		if p1 is None:
			p1 = ""
		else:
			p1 = "/"
		depends.append("%s%s%s" % (where_from, p1, depends[i]))
	
	# Depends is now list of all ldd's reported deps
	depends = depends[old_len:dep_len*2] + depends2
	
	# CHROOT
	## CHROOT path + the system location that be fo'reals
	for i in range(0, len(depends)):
		p1 = re.match("(\/)+$", where_to, re.M)
		if p1 is None:
			p1 = ""
		else:
			p1 = "/"
		depends3.append("%s%s%s" % (where_to, p1, depends[i]))
	
	## copy erry thang to CHROOT location
	for a, b in pair_up(depends, depends3):
		if a == where_from:
			continue
		print("COPY: {0} to {1}...\n".format(a,b)) ## talkalotta
		dufu.copy_file(a, b, preserve_times=0)    ## COPY
	
	# Export env variables
	os.environ["CHRT_CHROOT_PREFIX"] = CHROOT_PREFIX
	os.putenv("CHRT_CHROOT_PREFIX", CHROOT_PREFIX)
	os.environ["CHRT_LD_LIBRARY_LOC"] = LD_LIBRARY_LOC
	os.putenv("CHRT_LD_LIBRARY_LOC", LD_LIBRARY_LOC)
	
	return
	
if __name__ == "__main__":
	try:
		main(len(sys.argv), sys.argv)
	except RuntimeError:
		print("USAGE:\n\t{0} <needed binary> <CHROOT> <path to library files>\n".format(sys.argv[0]))
		sys.exit(1)
	
	sys.exit(0)
