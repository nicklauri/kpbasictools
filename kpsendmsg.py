#!/usr/bin/python 
#
#   File:	kpbuffattack.py
#   Author: Nick Lauri
#
#   Coyright (c) 2016 by Nick Lauri.
#

import os, sys
import socket, threading
from libs import kpstd

class target:
	name = None
	port = None
	is_alive = False
	
class packet:
	sent  = None		# in bytes
	count = None		# number of packets
	data  = None		# string of data (default: 'A')
	ndata = None		# number of clonning data

def attack(host, port, data, ndata):
	"""
	attack(host, port, data, cclone)
	
	- host  : target host
	- port  : target port
	- data  : data to send
	- ndata : clonning number of <data> to send
	"""
	
#

def thread_manager(target, num, verbose=False, *arg, **kwarg):
	"""
	thread_manager(target, num, *arg, **kwarg)
	
	- target: target function
	- num   : inital number of threads
	- arg   : (tuple) args of function
	- kwarg : (dict) args of function
	"""
	
	while True:
		if len(threading.enumerate()) - 1 < num:
			try:
				threading.Thread(target, arg, kwarg).start()
			except Exception as e:
				kpstd.error("Can not start thread.\n")
		else:
			pass
		
		if verbose:
			kpstd.info("Thread active
	
#

def main():
	
#

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        kpstd.error("User quit.")
    except Exception as e:
        print("Error: " + str(e))

