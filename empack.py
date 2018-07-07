#!/usr/bin/python3
# coding: utf-8
#
# by malexa
# represent the 214/DFW metroplex!
#
import os
import sys
from binascii import hexlify
import bz2
import struct

class CompressedData(object):
    def __init__(self, pre_data=b'\x00', *args, **kwargs):
        self.pre_data = pre_data
        self.the_data = b'\x00'

    def __call__(self):
        if self.the_data is not b'\x00':
            return self.the_data
        
        self.the_data = bz2.compress(self.pre_data, 6)
        return self.the_data

class AsmIfNotDef(object):
	def __init__(self, the_what):
		self.what = the_what
	
	def __repr__(self):
		return "%ifndef {0}\n%define {0}\n".format(self.what.replace('.','_'))
	
	def __del__(self):
		print("\n%endif\n")
		return

class AsmEquate(object):
	def __init__(self, prefix, noun, value):
		self.label = "%s_%s" % (prefix, noun)
		self.value = value
	
	def __repr__(self):
		return "{0}\tequ\t{1}".format(self.label.replace('.','_'),self.value)
	

class EmpackedEntree(object):
	def default_entsym(self, cls_name):
		if self.entree_name is None and cls_name is None:
			self.entree_name = self.__name__
			return self.entree_name
		if self.entree_name is not cls_name:
			if cls_name is not None:
				self.entree_name = cls_name
		return self.entree_name
	
	def __init__(self, *args, **kwargs):
		self.entree_name = self.__name__
		self.entree_data = None
		self.is_compressed = False
		self._fd = -1
		self._bzip2 = None
		self._ifndef = AsmIfNotDef(self.entree_name)
		self._sizey = AsmEquate("Esize", self.entree_name, 0)
		return
	def __init__(self, symbol_name, symbol_data, do_compress=False, fd=-1, bz2_data=None):
		self.entree_name = symbol_name
		self.entree_data = symbol_data
		self.is_compressed = do_compress
		self._fd = fd
		self._bzip2 = bz2_data
		self._ifndef = AsmIfNotDef(self.entree_name)
		self._sizey = AsmEquate("Esize", self.entree_name, os.fstat(fd).st_size)
		return
	
	def __del__(self):
		if (self._fd > 0):
			os.close(self._fd)
		return
	
	@property
	def symbol_name(self):
		return self.default_entsym(None)
	
	@property
	def symbol_data(self):
		if self.entree_data is None:
			return 0
		return self.entree_data
	
	@property
	def compressed(self):
		return self.compressed
	
	@classmethod
	def Construct(cls, input_fn, input_sn='', do_compressa=False):
		fido  = os.open(input_fn,os.O_RDONLY)
		frodo = os.read(fido, os.fstat(fido).st_size)
		pretty_name = input_sn
		sexy_cd = None 
		
		if (len(pretty_name) == 0):
			pretty_name = input_fn.rstrip('.')
		
		if do_compressa is True:
			sexy_cd = CompressedData(frodo)
		
		return cls(symbol_name=pretty_name, symbol_data=frodo, do_compress=do_compressa, fd=fido, bz2_data=sexy_cd)
	
	def output_data(self):
		hexxy_list = []
		hdrange = 0
		hexxy_data = None
		
		if self._bzip2 is not None:
			hexxy_data = hexlify(self._bzip2()).decode('utf-8')
			hdrange = len(hexxy_data) - 2
		else:
			hexxy_data = hexlify(self.symbol_data).decode('utf-8')
			hdrange = len(hexxy_data) - 2

		for i in range(0, hdrange):
			hexxy_list.append("0x{0}".format(hexxy_data[i:2+i]))
		
		return ''.join([" db ", ','.join(hexxy_list), '\n'])
	
	def output_sym_data(self):
		sex = "%s_%s%s" % ('sym', self.symbol_name.replace('.','_'),': ')
		return ''.join([sex, self.output_data()])
	
	def output_global(self):
		return "GLOBAL %s_%s:" % ('sym', self.symbol_name.replace('.','_'))
	
	def output_section(self):
		return "SECTION .rodata"
	
	def __repr__(self):
		return ''.join([str(self._ifndef), '\n', str(self._sizey), '\n', self.output_section(), '\n', self.output_global(), '\n', self.output_sym_data()])
	
class EmpackedEntree2(EmpackedEntree):
	pass

def Main(argc, argv):
	if (argc <= 1):
		return uhoh_help()

	optionals = (2, 3)
	optionals = list(map(lambda x: len(argv) > x, optionals))
	dicto = doOptionals(optionals, argv)

	print(";INPUT FILE: {0}".format(argv[1]))
	print(';%s %s' % ("OPTIONS:", dicto))
	print(";-.-.-\n")
	ee = EmpackedEntree2.Construct(argv[1],dicto['symbol'],dicto['compress'])
	print(ee)
	print("; empack.py - generated include file\n;;;; THX MALEXA ;;;;")
	return 0

def doOptionals(opti, argvv):
	o1 = ''
	o2 = False
	
	if opti[0] is True:
		o1 = argvv[2]
	if opti[1] is True:
		if 'yes' in argvv[3] or int(argvv[3]) is 1:
			o2 = True

	return dict(
		{
			'symbol': o1,
			'compress': o2,
		},
	)

def uhoh_help():
	print("\nEMPACK RESOURCES")
	print("./empack.py <input_file> [R] <symbol_name> [O] <compress> [O]\n")
	print("compress may be yes/no/0/1\n")

	return 1
### #ENTRY ## ## ## ## ## ## ## ## # ##
if __name__ == '__main__':
	av = sys.argv
	Main(len(av), av)

