#!env python
from __future__ import print_function
import sys, subprocess, os

fp = open("downloadableZips.csv")
for f in fp.readlines():
    (oid,url) = f.strip().split(',')
    parts = url.split('/')
    fname = parts[-1]
    if (fname == 'LDQ_zip'):
        continue
    args = ["wget", "--quiet", "--no-check-certificate", url]
    print(' '.join(args))
    p = subprocess.check_output(args)
    print(p)
fp.close()

exit(-1)
