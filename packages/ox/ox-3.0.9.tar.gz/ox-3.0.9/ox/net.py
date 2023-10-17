# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2008
from __future__ import print_function
import gzip
import json
import os
import re
import struct

import requests

from io import BytesIO
import urllib
from chardet.universaldetector import UniversalDetector


DEBUG = False
# Default headers for HTTP requests.
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.8,fr;q=0.6,de;q=0.4',
    'Accept-Encoding': 'gzip',
}

def status(url, data=None, headers=None):
    try:
        f = open_url(url, data, headers)
        s = f.code
    except urllib.error.HTTPError as e:
        s = e.code
    return s

def exists(url, data=None, headers=None):
    s = status(url, data, headers)
    if s >= 200 and s < 400:
        return True
    return False

def get_headers(url, data=None, headers=None):
    try:
        f = open_url(url, data, headers)
        f.headers['Status'] = "%s" % f.code
        headers = f.headers
        f.close()
    except urllib.error.HTTPError as e:
        e.headers['Status'] = "%s" % e.code
        headers = e.headers
    return dict(headers)

def get_json(url, data=None, headers=None):
    return json.loads(read_url(url, data, headers).decode('utf-8'))  # pylint: disable=no-member

def open_url(url, data=None, headers=None):
    if headers is None:
        headers = DEFAULT_HEADERS.copy()
    if isinstance(url, bytes):
        url = url.decode('utf-8')
    url = url.replace(' ', '%20')
    if data and not isinstance(data, bytes):
        data = data.encode('utf-8')
    req = urllib.request.Request(url, data, headers)
    return urllib.request.urlopen(req)

def read_url(url, data=None, headers=None, return_headers=False, unicode=False):
    if DEBUG:
        print('ox.net.read_url', url)
    f = open_url(url, data, headers)
    result = f.read()
    f.close()
    if f.headers.get('content-encoding', None) == 'gzip':
        result = gzip.GzipFile(fileobj=BytesIO(result)).read()
    if unicode:
        ctype = f.headers.get('content-type', '').lower()
        if 'charset' in ctype:
            encoding = ctype.split('charset=')[-1]
        else:
            encoding = detect_encoding(result)
        if not encoding:
            encoding = 'latin-1'
        result = result.decode(encoding)
    if return_headers:
        f.headers['Status'] = "%s" % f.code
        headers = {}
        for key in f.headers:
            headers[key.lower()] = f.headers[key]
        return headers, result
    return result

def detect_encoding(data):
    data_lower = data.lower().decode('utf-8', 'ignore')
    charset = re.compile('content="text/html; charset=(.*?)"').findall(data_lower)
    if not charset:
        charset = re.compile('meta charset="(.*?)"').findall(data_lower)
    if charset:
        return charset[0].lower()
    detector = UniversalDetector()
    p = 0
    l = len(data)
    s = 1024
    while p < l:
        detector.feed(data[p:p+s])
        if detector.done:
            break
        p += s
    detector.close()
    return detector.result['encoding']

get_url = read_url

def save_url(url, filename, overwrite=False):
    if not os.path.exists(filename) or overwrite:
        dirname = os.path.dirname(filename)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
        headers = DEFAULT_HEADERS.copy()
        r = requests.get(url, headers=headers, stream=True)
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

def _get_size(url):
    req = urllib.request.Request(url, headers=DEFAULT_HEADERS.copy())
    req.get_method = lambda: 'HEAD'
    u = urllib.request.urlopen(req)
    if u.code != 200 or 'Content-Length' not in u.headers:
        raise IOError
    return int(u.headers['Content-Length'])

def _get_range(url, start, end):
    headers = DEFAULT_HEADERS.copy()
    headers['Range'] = 'bytes=%s-%s' % (start, end)
    req = urllib.request.Request(url, headers=headers)
    u = urllib.request.urlopen(req)
    return u.read()

def oshash(url):
    try:
        longlongformat = 'q'  # long long
        bytesize = struct.calcsize(longlongformat)

        filesize = _get_size(url)
        hash_ = filesize
        head = _get_range(url, 0, min(filesize, 65536))
        if filesize > 65536:
            tail = _get_range(url, filesize-65536, filesize)
        if filesize < 65536:
            f = BytesIO(head)
            for _ in range(int(filesize/bytesize)):
                buffer = f.read(bytesize)
                (l_value,) = struct.unpack(longlongformat, buffer)
                hash_ += l_value
                hash_ = hash_ & 0xFFFFFFFFFFFFFFFF  # cut off 64bit overflow
        else:
            for offset in range(0, 65536, bytesize):
                buffer = head[offset:offset+bytesize]
                (l_value,) = struct.unpack(longlongformat, buffer)
                hash_ += l_value
                hash_ = hash_ & 0xFFFFFFFFFFFFFFFF  # cut of 64bit overflow
            for offset in range(0, 65536, bytesize):
                buffer = tail[offset:offset+bytesize]
                (l_value,) = struct.unpack(longlongformat, buffer)
                hash_ += l_value
                hash_ = hash_ & 0xFFFFFFFFFFFFFFFF
        returnedhash = "%016x" % hash_
        return returnedhash
    except IOError:
        return "IOError"
