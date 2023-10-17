#!/usr/bin/env python
import re
import subprocess
from ailab.log import logger

cmd = '''pip index versions pyatp-buildkit | grep -o  '(.*)' |cut -d  '('  -f2|cut -d  ')'  -f1|awk -F "." '{print $1"."$2"."$3+1}' '''


def get_latest_version(package_name):
    output = subprocess.run(["pip", "index", "versions", package_name],
                            capture_output=True)
    output = output.stdout.decode('utf-8')
    if output:
        output = list(filter(lambda x: len(x) > 0, output.split('\n')))
        latest_version = output[-1].split(':')[1].strip()
        return latest_version
    else:
        return None

def incre_version(version):
    regex = "\d+\.\d+\.\d+"
    if not re.match(regex, version):
        logger.info("not match version ")
        return  version
    o,tw,th = version.split(".")

    th = str(int(th) + 1)
    nv = '.'.join([o, tw,th])
    return nv


if __name__ == '__main__':
    result = get_latest_version('pyatp-buildkit')
    increment = incre_version(result)
    p = open("pyproject.toml",'r')
    fc = p.read()
    fc.replace("version= ")
