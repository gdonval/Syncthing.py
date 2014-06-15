#!/usr/bin/env python3.4
import os
import re
import sys

path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
pathMatch = re.compile("(%s|^)%s(%s|$)" % (os.pathsep, re.escape(path), os.pathsep))
pathIsMissing = True
try:
    if pathMatch.match(os.environ['PYTHONPATH']):
        pathIsMissing = False
except:
    pass

if pathIsMissing:
    sys.path.append(path)
