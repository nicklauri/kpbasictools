#!/usr/bin/python 
#
#   File:
#   Author: Nick Lauri
#
#   Coyright (c) 2016 by Nick Lauri.
#

import os, sys
from datetime import datetime
from libs import kpstd

aries  = [datetime(1, 3, 21), datetime(1, 4, 19), 'aries']
taurus = [datetime(1, 4, 20), datetime(1, 5, 20), 'taurus']
gemini = [datetime(1, 5, 21), datetime(1, 6, 21), 'gemini']
cancer = [datetime(1, 5, 22), datetime(1, 7, 22), 'cancer']
leo    = [datetime(1, 7, 23), datetime(1, 8, 22), 'leo']
virgo  = [datetime(1, 8, 23), datetime(1, 9, 22), 'virgo']
libra  = [datetime(1, 9, 23), datetime(1, 10, 23), 'libra']
scopio = [datetime(1, 10, 24), datetime(1, 11, 21), 'scopio']
sagitt = [datetime(1, 11, 22), datetime(1, 12, 21), 'sagittarius']
capri  = [datetime(1, 12, 22), datetime(2, 1, 19), 'capricon']
aqua   = [datetime(1, 1, 20), datetime(1, 2, 18), 'aquarius']
pisces = [datetime(1, 2, 19), datetime(1, 3, 20), 'pisces']

horoscope = [aries, taurus, gemini, cancer, leo, virgo, libra, scopio, sagitt, capri,\
			aqua, pisces]
#

def check(day, mon):
	try:
		current = datetime(1, mon, day)
		if mon == 1 and day <= 19:
			current = datetime(2, mon, day)
	except ValueError as e:	
		kpstd.error('Error in parameter input.\n')
		raise e
	
	for item in horoscope:
		if current >= item[0] and current <= item[1]:
			kpstd.norm('Found! You are: `%s`\n' %item[2])
			return
	else:
		kpstd.warn('Something wrong :(\n')
		return 

def main():
	day = mon = 0
	if sys.argv.__len__() != 3:
		kpstd.error('Invalid parameter\n')
		kpstd.norm('Usage: python %s date mon\n' %(os.path.split(sys.argv[0])[1]))
		raise(Exception('Number of parameters must be 3\n'))
		exit()
	
	try:
		day = int(sys.argv[1])
		mon = int(sys.argv[2])
	except Exception as e:
		kpstd.error('Parameter error\n')
		raise e
	
	check(day, mon)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("User quit.")
    except Exception as e:
        print("Error: " + str(e))

