#!/usr/bin/python 
#
#   File: expectedip.py
#   Author: Nick Lauri
#
#   Coyright (c) 2016 by Nick Lauri.
#

import os, sys
import socket
import time
from libs import kpstd

class prog:
    name = os.path.split(sys.argv[0])[1].replace('.py', '')
    usage = "Usage: %s <host-name> <ip-you-want-to-wait>\n" %name

def main():
    if len(sys.argv) != 3:
        kpstd.error("Just 3 parameter.\n")
        kpstd.info(prog.usage)
        exit()
    else:
        host = sys.argv[1]
        ip   = sys.argv[2]

    kpstd.info('Running ...\n')
    tstart = time.time()
    while True:
        if ip == socket.gethostbyname(host):
            kpstd.info("Wait done!\n")
            break
    tend = time.time()
    kpstd.info("Executed in %.3fs\n" %(tend - tstart))
#

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("User quit.")
    except Exception as e:
        print("Error: " + str(e))

