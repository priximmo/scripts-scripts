#!/usr/bin/env python3
# coding=utf-8
import sys

class DecodeInstead(Exception):
	pass

class NBName(object):
	def __init__(self, *args, **kwargs):
		self.__init__('','')

	def __init__(self, name, scope=''):
		self._mapping = {
			'A': 'EB',
			'B': 'EC',
			'C': 'ED',
			'D': 'EE',
			'E': 'EF',
			'F': 'EG',
			'G': 'EH',
			'H': 'EI',
			'I': 'EJ',
			'J': 'EK',
			'K': 'EL',
			'L': 'EM',
			'M': 'EN',
			'N': 'EO',
			'O': 'EP',
			'P': 'FA',
			'Q': 'FB',
			'R': 'FC',
			'S': 'FD',
			'T': 'FE',
			'U': 'FF',
			'V': 'FG',
			'W': 'FH',
			'X': 'FI',
			'Y': 'FJ',
			'Z': 'FK',
			'0': 'DA',
			'1': 'DB',
			'2': 'DC',
			'3': 'DD',
			'4': 'DE',
			'5': 'DF',
			'6': 'DG',
			'7': 'DH',
			'8': 'DI',
			'9': 'DJ',
			' ': 'CA',
			'-': 'CN',
			'.': 'CO',
		}
		self._name_e = ''
		self._name_u = name
		self._scope = scope
	
	def decode(self, instr):
		outstr = ''
		for i in range(0, len(instr)):
			c = ''
			try:
				c = instr[i]
				c = c + instr[i+1]  
			except IndexError:
				break
			print(c)
			for k, v in self._mapping.items():
				if v == c:
					outstr = outstr + str(k) 
		return outstr

	@property
	def unencoded(self):
		uen = self.decode(self._name_e)
		
		if len(uen) > 0 and self._name_u is not uen:
			self._name_u = uen

		return self._name_u

	@unencoded.setter
	def unencoded(self, val):
		self._name_u = val
		return

	@property
	def encoded(self):
		if len(self._name_e) > 0 and self.decode(self._name_e) is self._name_u:
			return self._name_e

		r = [c for c in self.unencoded.upper()]
		r = [self._mapping[c] for c in r]
		self._name_e = ''.join(r)
		return self._name_e

	@encoded.setter
	def encoded(self, val):
		self._name_e = val
		return

	@property
	def scope(self):
		return self._scope

	@property
	def full(self):
		dot = '.' if not len(self.scope) is 0 else ''
		return "%s%s%s" % (self.encoded, dot, self.scope.upper())

##########################

if len(sys.argv) < 2:
	print("usage {0}: nbname.nbscope\n".format(sys.argv[0]))
	print("usage {0}: -d nbname\n".format(sys.argv[0]))
	sys.exit(1)

try:
	if "-d" in sys.argv:
		raise DecodeInstead

	if '.' in sys.argv[1]:
		p = sys.argv[1].find('.')
		nns = sys.argv[1][1+p:]
		nnn = sys.argv[1][:p]
	else:
		nnn = sys.argv[1]
		nns = ''

	nn = NBName(nnn, nns)
	print(nn.full)

except DecodeInstead:
	if len(sys.argv) <= 2:
		print("usage {0}: nbname.nbscope\n".format(sys.argv[0]))
		print("usage {0}: -d nbname\n".format(sys.argv[0]))
		sys.exit(1)

	nn = NBName('')
	nn.encoded = sys.argv[2]
	print(nn.unencoded)
#
 #
sys.exit(0)
