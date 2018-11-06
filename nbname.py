#!/usr/bin/env python3
# coding=utf-8
import sys

class NBName(object):
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
	@property
	def unencoded(self):
		return self._name_u

	@property
	def encoded(self):
		if len(self._name_e) > 0:
			return self._name_e
		r = [c for c in self.unencoded.upper()]
		r = [self._mapping[c] for c in r] 
		return ''.join(r)

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
	sys.exit(1)

if '.' in sys.argv[1]:
	p = sys.argv[1].find('.')
	nns = sys.argv[1][1+p:]
	nnn = sys.argv[1][:p]
else:
	nnn = sys.argv[1]
	nns = ''

nn = NBName(nnn, nns)
print(nn.full)
sys.exit(0)

