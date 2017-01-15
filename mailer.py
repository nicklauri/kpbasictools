#!/usr/bin/python 
#
#   File: fakemail.py
#   Author: Nick Lauri
#
#   Coyright (c) 2017 by Nick Lauri.
#

import os
import sys
import socket
import dns.resolver
import libs.kpstd as kpstd

class Mail:
    def __init__(self, host, mail_from, mail_name, rcpt_to, rcpt_name, \
        subject, content):
        self.host = host
        self.fakehost = mail_from.split('@')[1]
        self.mail_from = mail_from
        self.mail_name = mail_name
        self.rcpt_to = rcpt_to
        self.rcpt_name = rcpt_name
        self.subject = subject
        self.content = content

    def send(self):
        for server in self.resolve_mx():
            client = socket.socket()
            kpstd.info("trying to connect to %s ... " %server)
            try:
                client.connect((server, 25))
            except Exception as e:
                kpstd.out("failed.\n")
                kpstd.error("error occured. Stop sending message!\n")
                kpstd.error("Exception: %s\n" %str(e))
                continue
            else:
                kpstd.out("OK!\n")

            try:
                kpstd.info('stage 1: ')
                data = client.recv(1000)
                if '220' in data:
                    kpstd.out("success \n")
                else:
                    kpstd.out("unknow status: '%s'\n" %data)
                
                kpstd.info('stage 2: ')
                client.send('HELO %s\r\n' %self.fakehost)
                data = client.recv(1000)
                if '250' in data:
                    kpstd.out("success \n")
                else:
                    kpstd.out("unknow status: '%s'\n" %data)

                kpstd.info('stage 3: ')
                client.send('MAIL FROM:<%s>\r\n' %self.mail_from)
                data = client.recv(1000)
                if '250' in data:
                    kpstd.out("success \n")
                else:
                    kpstd.out("unknow status: '%s'\n" %data)

                kpstd.info('stage 4: ')
                client.send('RCPT TO:<%s>\r\n' %self.rcpt_to)
                data = client.recv(1000)
                if '250' in data:
                    kpstd.out("success \n")
                else:
                    kpstd.out("unknow status: '%s'\n" %data)

                kpstd.info('stage 5: ')
                client.send('DATA\r\n')
                data = client.recv(1000)
                if '354' in data or 'data' in data:
                    kpstd.out("success \n")
                else:
                    kpstd.out("unknow status: '%s'\n" %data)

                kpstd.info('stage 6: ')
                import datetime as dt
                client.send('From: "%s" <%s>\r\n' %(self.mail_name, self.mail_from))
                client.send('To: "%s" <%s>\r\n' %(self.rcpt_name, self.rcpt_to))
                client.send('Date: Thu %s 00:00:00 +0100\r\n' \
                    %(dt.datetime.strftime(dt.date(2017, 1, 12), '%d %B %Y')))
                client.send('Subject: %s\r\n\r\n%s\r\n.\r\n' \
                     %(self.subject, self.content))
                data = client.recv(1000)
                if '250' in data:
                    kpstd.out("success \n")
                else:
                    kpstd.out("unknow status: '%s'\n" %data)

                kpstd.info('seding fake email complete!\n')
                kpstd.info('closing connection\n')
                client.send('QUIT')
                client.close()
                break
            except Exception as e:
                print
                kpstd.error('error occured!\n')
                raise e
    def resolve_mx(self):
        lmx = list()
        try:
            for item in dns.resolver.query(self.host, 'MX'):
                # 10 mail.example.com. => mail.example.com
                lmx.append(item.to_text().split()[1][:-1])
        except dns.resolver.NXDOMAIN:
            kpstd.error("can't resolve to mail server for host '%s\n'" %self.host)
            exit()
        else:
            self.lmx = lmx
        return lmx

def usage():
    kpstd.info('Usage:\n   python %s ' %sys.argv[0])
    kpstd.out ('<host> <from> <from_name> <to> <to_name> <subject> <content>\n\n')
    kpstd.info('Note:\n')
    kpstd.out (' - host: domain. Ex: abc@yahoo.com => host: yahoo.com\n')
    kpstd.out (' - from: your fake email.\n')
    kpstd.out (' - from_name: your name.\n')
    kpstd.out (' - to  : target\'s email.\n')
    kpstd.out (' - to_name  : target\'s name.\n')
    kpstd.out (' - subject  : subject @@\n')
    kpstd.out (' - content  : email body.\n')

def banner():
    print("KProject Mailer version 1.0 - written by Nick Lauri.")

def main():
    a = sys.argv
    if len(a) != 8:
        kpstd.error('not enough args.\n')
        usage()
        exit()
    mailer = Mail(a[1], a[2], a[3], a[4], a[5], a[6], a[7])
    mailer.send()

main()

