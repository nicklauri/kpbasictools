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
import threading
from libs import kpstd

class prog:
    name = os.path.split(sys.argv[0])[1].replace('.py', '')
    usage = "Usage: %s <host-name> <ip-you-want-to-wait>\n" %name

stop = False
def timer(time_start):
    global stop
    while not stop:
        time.sleep(0.1)
        kpstd.info("Running in: %.2fs \r" %(time.time() - time_start))
    stop = 1

def main():
    global stop, tstart
    if len(sys.argv) != 3:
        kpstd.error("Just 3 parameter.\n")
        kpstd.info(prog.usage)
        exit()
    else:
        host = sys.argv[1]
        ip   = sys.argv[2]

    kpstd.info('Running ...\n')
    tstart = time.time()
    th_timer = threading.Thread(target=timer, args=(tstart,))
    th_timer.run()
    while True:
        if ip == socket.gethostbyname(host):
            stop = True
            th_time.join(timeout=0)
            while not stop:
                pass
            kpstd.info("\nWait done!    \n")
            break
    tend = time.time()
    kpstd.info("Executed in %.2fs\n" %(tend - tstart))
#

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print
        pass

