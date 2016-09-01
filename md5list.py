#!/usr/bin/python 
#
#   File:
#   Author: Nick Lauri
#
#   Coyright (c) 2016 by Nick Lauri.
#

import os, sys
from libs import kpstd
import md5

def main():
	if len(sys.argv) != 2:
		kpstd.error("Just 1 argument.\n")
		kpstd.norm("Usage: python %s single_string/file\n" %sys.argv[0])
		raise Exception("Parameter(s) error.")
	
	arg = sys.argv[1]
	if not os.path.isfile(arg):
		kpstd.info("MD5 hash for '%s': %s\n"  %(arg, md5.md5(arg).hexdigest()))
		exit()
	
	# arg is file
	kpstd.info("Trying to read file '%s': " %arg)
	try:
		farg = open(arg)
	except IOError as e:
		print("Failed")
		kpstd.error("Can not open file '%s'\n" %arg)
		
		if type(e) == tuple:
			e = e[len(e) - 1]
		raise Exception(str(e))
	else:
		print("OK")
		kpstd.info("Loading data: ")
		try:
			lines = farg.readlines()
		except Exception as e:
			print("failed")
			kpstd.error("Error on loading data.\n")
			raise e
		else:
			print "OK"
			if len(lines) >= 20:
				kpstd.info("Specify a file to store hashes (blank for none): ")
				fout = raw_input()
				if fout:
					fout = open(fout, 'w')
				else:
					fout = False
	
	if fout:
		counter = 0
		for l in lines:
			counter += 1
			l = l.strip('\n').strip(' ')
			fout.write('%s: %s\n' %(l, md5.md5(l).hexdigest()))
			kpstd.info('Progress: %d/%d \r' %(counter, len(lines)))
		print
		kpstd.info("Done. Exiting.\n")
	else:
		kpstd.info("Dumping hashes...\n")
		for l in lines:
			l = l.strip('\n').strip(' ')
			print("%s: %s" %(l, md5.md5(l).hexdigest()))
		kpstd.info("Done. Exiting\n")
	
#

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("User quit.")
    except Exception as e:
        print("Error: " + str(e))

