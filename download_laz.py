#!env python
import os
import subprocess
from util import download_file

# Download from http://lastools.org/download/laszip-cli.exe
laszip = "f:/LASTools/bin/laszip64.exe"
if not os.path.exists(laszip):
    print("Can't unpack without the laszip program")
    pass

workspace = "f:/surface/NOAA"

#===========================================================

with open("LAZ.csv") as fp:
    lines = fp.readlines()
del lines[0] # delete header
total = len(lines)

try:
    os.makedirs(workspace)
except:
    pass # It's okay if it already exists
os.chdir(workspace)

count = 0
success = 0
fail = 0
already_in_stock = 0
unpacked = 0
fail_unpack = 0

for f in lines:
    (oid,url) = f.strip().split(',')

    parts = url.split('/')
    fname = parts[-1]

    f,e = os.path.splitext(fname)
    lasfile = None
    if e.lower() == '.laz':
        lasfile = f + '.las'
        if os.path.exists(lasfile):
            already_in_stock += 1
            print("Already have %s" % lasfile)
            continue

    # Fetch the file
    count += 1
    print("Downloading %d/%d %s.." % (count, total, fname), end="")
    try:
        if download_file(url, fname):
            success += 1
    except Exception as e:
        print("..failed, %s" % e)
        fail += 1
    print()
    
    if lasfile:
        # Uncompress the file
        print("Unpacking %s.." % fname, end="")
        try:
            args = [laszip, fname]
            p = subprocess.check_output(args)
            unpacked = True
        except Exception as e:
            print("..failed, %s" % e)
            fail_unpack += 1
        print()

print("Downloaded %d, failed to download %d, already had %d" % (success, fail, already_in_stock))
print("Unpacked %d, failed to unpack %d" % (unpacked, fail_unpack))

exit(0)
