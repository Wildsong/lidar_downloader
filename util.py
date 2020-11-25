import sys
import os
import requests
import shutil

if sys.version_info[:2] < (3, 6):
    raise SystemExit("I need Python 3!")

def download_file(url, local_filename):
    # NOTE the stream=True parameter below

    # Okay, I understand that I am not using good certs. Thanks for the warning.
    requests.packages.urllib3.disable_warnings()

    ok = False
    if not os.path.exists(local_filename):
        with requests.get(url, stream=True, verify=False) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                shutil.copyfileobj(r.raw,f)
            ok = True
    return ok

if __name__ == "__main__":
    # unit tests needed here
    pass

