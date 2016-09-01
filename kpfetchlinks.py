#!/usr/bin/python 

from __future__ import print_function, absolute_import
import os, sys
import urllib2, re
from libs import kpstd

target_root = "http://data.ceh.vn/CEHv9-TV"		# Change if nessessary
target_ext  = ['pdf', 'mp4', 'avi']
target_output = 'ceh_links.txt'

fout = open(target_output, "w")

links = []

rule_a   = re.compile("""<a\s+(?:[^>]*?\s+)?href="([^"]*)["]""")
#rule_pdf = re.compile("""<a\s+(?:[^>]*?\s+)?href="([^"]+.pdf)["]""")
#rule_mp4 = re.compile("""<a\s+(?:[^>]*?\s+)?href="([^"]+.mp4)["]""")
def fetch_alink(strings):
    if strings == None:
        return []
    
    l = []
    for t in rule_a.findall(strings):
        if type(t) == tuple:
            l.append(t[0])
        elif type(t) == str:
            l.append(t)
    return l
#

def get_data(url, verbose=True):
    try:
        src = urllib2.urlopen(url).read()
    except Exception as e:
        if verbose:
            print("Failed")
            kpstd.error("Exception: %s\n" %str(e))
        return None
    else:
        return src
#

def loop_getlinks(url):
    global links, scanned
    for item in fetch_alink(get_data(url, verbose=False)):
        kpstd.info('Found: %3d links\r' %len(links))
        item = item.strip('/').strip('/').strip('/')
        if item.endswith(".pdf") or item.endswith(".mp4") or item.endswith(".avi"):
            if item not in links:
                links.append(''.join([url, '/', item]))
                kpstd.info('Found: %3d links\r' %len(links))
        else:
            if ''.join([url, '/', item]) not in scanned:
                scanned.append(''.join([url, '/', item]))
                if not item.startswith('?'):
                    loop_getlinks(''.join([url, '/', item]))
#

scanned = []
def main():
    global links, scanned
    
    kpstd.norm('Get source from root target: ')
    src = get_data(target_root); print("OK")
    
    scanned.append(target_root)
    scanned.append("http://data.ceh.vn/CEHv9-TV/")
    for item in fetch_alink(src):
        item = item.strip('/').strip('/').strip('/')
        if item.endswith(".pdf") or item.endswith(".mp4") or item.endswith(".avi"):
            links.append(''.join([target_root, '/', item]))
            kpstd.info('Found: %3d links\r' %len(links))
        else:
            if ''.join([target_root, '/', item]) not in scanned:
                if not item.startswith('?'):
                    loop_getlinks(''.join([target_root, '/', item]))
                scanned.append(''.join([target_root, '/', item]))
    
    kpstd.norm('Scan done. Analyzing results.\n')
    
    pdf_links = []
    mp4_links = []
    avi_links = []
    for item in links:
        if item.endswith('.pdf'):
            pdf_links.append(item)
        elif item.endswith('.mp4'):
            mp4_links.append(item)
        else:
            avi_links.append(item)
    
    kpstd.norm('Analyzed results.\n')
    kpstd.info('Scanned: %3d links\n' %len(scanned))
    kpstd.info('Found: %3d pdf | %3d mp4 | %3d avi\n' %(len(pdf_links), len(mp4_links), len(avi_links)))
    kpstd.info('Writing data to file: ')
    for i in pdf_links:
        fout.write('%s\n' %i)
        fout.flush()
    
    fout.write('\n')
    for i in mp4_links:
        fout.write('%s\n' %i)
        fout.flush()
    
    fout.write('\n')
    for i in avi_links:
        fout.write('%s\n' %i)
        fout.flush()
    
    print(" OK")
    
#

try:
    main()
except KeyboardInterrupt:   
    print
    kpstd.error('User quit\n')

