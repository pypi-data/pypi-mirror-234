#!/usr/bin/python
# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from __future__ import print_function

import re

from .js import minify
from .utils import json


def load(f):
    return loads(f.read())

def loads(source):
    try:
        minified = minify(source)
        return json.loads(minified)
    except ValueError as e:
        msg = e.message if hasattr(e, 'message') else str(e)
        lineno = None
        colno = None
        try:
            m = re.search(r'line (\d+) column (\d+)', msg)
            if m:
                (lineno, colno) = [int(n) for n in m.groups()]
        except:
            pass
        if lineno and colno:
            s = minified.split('\n')
            context = s[lineno-1][max(0, colno-30):colno+30]
            msg += ' at:\n\n %s\n %s\033[1m^\033[0m' % (context, ' ' * (colno - max(0, colno-30) - 2))
        raise ValueError(msg)
