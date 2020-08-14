#!env python
from __future__ import print_function
import sys, subprocess, os

workspace = "f:/surface/DOGAMI"

fp = open("LDQzips.csv")

try:
    os.makedirs(workspace)
except:
    pass # It's okay if it already exists
os.chdir(workspace)

success = 0
fail = 0
already_in_stock = 0

for f in fp.readlines():
    (oid,url) = f.strip().split(',')
    if not oid.isnumeric: continue # Skip column headers
    parts = url.split('/')
    fname = parts[-1]
    if not os.path.exists(fname):
        args = ["wget", "--quiet", "--no-check-certificate", url]
        print("Downloading %s" % fname)
        try:
            p = subprocess.check_output(args)
            success += 1
        except Exception as e:
            print("..failed, %s" % e)
            fail += 1
    else:
        already_in_stock += 1

print("Transferred %d, already had %s. %d failed to download." % (success, already_in_stock, fail))
fp.close()

exit(-1)
