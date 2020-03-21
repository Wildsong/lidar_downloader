#!env python
import sys, subprocess, os
import requests
import shutil

if sys.version_info[:2] < (3, 6):
    raise SystemExit("I need Python 3!")

def download_file(url, local_filename):
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True, verify=False) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw,f)
    return

# Count up how many files we are fetching
count = 0
files = []
with open("downloadableZips.csv") as fp:
    for f in fp.readlines():
        (oid,url) = f.strip().split(',')
        parts = url.split('/')
        fname = parts[-1]
        if (fname == 'LDQ_zip'): # Skip the column header line
            continue
        count += 1
        files.append((url,fname))
total = count

# Fetch the files
count = 0
completed = 0
for (url,fname) in files:
    count += 1
    if os.path.exists(fname) :
        print("%d/%d Refusing to overwrite \"%s\", delete it and run me again." % (count,total,fname))
    else:
        print("Downloading %d/%d %s" % (count, total, fname), end="")
        download_file(url, fname)
        completed += 1
    print()
print("***ALL DONE, %d files were downloaded.***" % completed)
exit(0)
