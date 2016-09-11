#!/usr/bin/python 
#
#   File:
#   Author: Nick Lauri
#
#   Coyright (c) 2016 by Nick Lauri.
#

import os, sys
from libs import kpstd

def main():
	resolv_conf = '/etc/resolv.conf'
	
	kpstd.info('Writing data: ')
	try:
		with open(resolv_conf, 'w') as f:
			f.write('nameserver 8.8.8.8\n')
			f.write('nameserver 8.8.4.4\n')
		print("OK")
	except Exception as e:
		print("Failed")
		kpstd.error("Cannot change dns: " + str(e) + "\n")
		
#

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("User quit.")
    except Exception as e:
        print("Error: " + str(e))

