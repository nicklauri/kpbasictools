#!/usr/bin/python 
#
#   File:	maskshow.py - change between subnet mask address and integer 
#   Author: Nick Lauri
#
#   Coyright (c) 2016 by Nick Lauri.
#

import os, sys
from libs import kpstd

class prog:
	fname = os.path.split(sys.argv[0])[1]
	name  = fname.split('.')[0]
	version  = "1.0"
	hversion = 0x0100

usage_string = """
Usage: python %s <arg1> [<arg2> [<arg3> [...]]]
Note:
    - Must be subnet mask address or integer.
    - Integer must be less than or equal 32.
    - Type of subnet mask address must be xxx.xxx.xxx.xxx
"""

banner  = "KProject MaskShow version %s - Change between subnetmask address and integer.\n"
banner += "Copyright (c) 2016 by Nick Lauri."

def usage():
	print(banner %(prog.version))
	print(usage_string %(prog.fname))
#

def is_subnm(string):
	if len(string.split('.')) != 3:
		return False
	
	for i in string.split('.'):
		if not i.isdigit():
			return False
		elif int(i) > 255 or int(i) < 0:
			return False
	else:
		return True
#

def is_int(string):
	if not string.isdigit():
		return False
	elif int(string) > 32 or int(string) < 0:
		return False
	else:
		return True
#

def sub2int(string):
	res = ''
	ret = 0
	for i in string.split('.'):
		res = ''.join([res, bin(int(i, 10))[2:]])
	
	for c in res:
		if c == '1':
			ret += 1
	
	return ret
#

def int2sub(integer):
	bstr = ''
	for i in xrange(integer):
		bstr = ''.join([bstr, '1'])
	
	while len(bstr) < 8*4:
		bstr = ''.join([bstr, '0'])
	
	ret = ''
	for i in xrange(0, 8*4, 8):
		ret = ''.join([ret, '.', str(int(bstr[i:i+8], 2))])
	
	return ret if not ret.startswith('.') else ret[1:]
#

def main():
	if len(sys.argv) == 1:
		usage()
		exit()
	
	# Filter subnetmask address and integer:
	submn = []
	integ = []
	error = False
	nerro = []
	
	for item in sys.argv[1:]:
		if is_submn(item):
			submn.append(item)
		elif is_int(item):
			integ.append(int(item))
		else:
			error = True
			nerro.append(item)
	
	# Report errors and exit:
	if error:
		for item in nerro:
			kpstd.error("Unknow type of argument: %s" %item)
			exit()
	
	
	
#

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        kpstd.norm("\nUser quit.\n")
    except Exception as e:
        kpstd.error("\nError: " + str(e) + "\n")

