# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2011
from __future__ import print_function
from types import MethodType
import gzip
import mimetypes
import os
import shutil
import sys
import time

from http import cookiejar as cookielib
from io import BytesIO
import urllib
from urllib.parse import urlparse
import requests

from . import __version__
from .utils import json

__all__ = ['getAPI', 'API']


CHUNK_SIZE = 1024*1024*5

def getAPI(url, cj=None):
    return API(url, cj)

class API(object):
    __version__ = __version__
    __name__ = 'ox'
    DEBUG = False
    debuglevel = 0

    def __init__(self, url, cj=None):
        if cj:
            self._cj = cj
        else:
            self._cj = cookielib.CookieJar()

        self._requests_session = requests.Session()
        self._requests_session.cookies = self._cj
        self._requests_session.headers = {
            'User-Agent': '%s/%s' % (self.__name__, self.__version__),
            'Accept-Encoding': 'gzip, deflate',
        }
        self.url = url
        r = self._request('api', {'docs': True})
        self._properties = r['data']['actions']
        self._actions = r['data']['actions'].keys()
        for a in r['data']['actions']:
            self._add_action(a)

    def _add_method(self, method, name):
        if name is None:
            name = method.func_name
        setattr(self, name, MethodType(method, self))

    def _add_action(self, action):
        def method(self, *args, **kw):
            if args and kw:
                raise ValueError('pass either a dictionary or kwargs, not both')
            if not kw:
                if args:
                    kw = args[0]
                else:
                    kw = None
            return self._request(action, kw)
        if 'doc' in self._properties[action]:
            method.__doc__ = self._properties[action]['doc']
        method.func_name = action
        self._add_method(method, action)

    def _json_request(self, url, data, files=None):
        result = {}
        try:
            request = self._requests_session.post(url, data=data, files=files)
            result = request.json()
            return result
        except urllib.error.HTTPError as e:
            if self.DEBUG:
                import webbrowser
                if e.code >= 500:
                    with open('/tmp/error.html', 'wb') as f:
                        f.write(e.read())
                    webbrowser.open_new_tab('/tmp/error.html')

            result = e.read()
            try:
                result = result.decode('utf-8')
                result = json.loads(result)
            except:
                result = {'status': {}}
            result['status']['code'] = e.code
            result['status']['text'] = str(e)
            return result
        except:
            if self.DEBUG:
                import webbrowser
                import traceback
                traceback.print_exc()
                if result:
                    with open('/tmp/error.html', 'w') as f:
                        f.write(str(result))
                    webbrowser.open_new_tab('/tmp/error.html')
            raise

    def _request(self, action, data=None):
        form = {
            'action': action
        }
        if data:
            form['data'] = json.dumps(data)
        return self._json_request(self.url, form)

    def get_url(self, url):
        return self._requests_session.get(url).content

    def save_url(self, url, filename, overwrite=False):
        chunk_size = 16 * 1024
        if not os.path.exists(filename) or overwrite:
            dirname = os.path.dirname(filename)
            if dirname and not os.path.exists(dirname):
                os.makedirs(dirname)
            tmpname = filename + '.tmp'
            with open(tmpname, 'wb') as fd:
                r = self._requests_session.get(url)
                for chunk in iter(lambda: r.read(chunk_size), b''):
                    fd.write(chunk)
            shutil.move(tmpname, filename)

    def upload_chunks(self, url, filename, data=None, silent=False):
        data = self._json_request(url, data)

        def full_url(path):
            if path.startswith('/'):
                u = urlparse(url)
                path = '%s://%s%s' % (u.scheme, u.netloc, path)
            return path

        if 'uploadUrl' in data:
            uploadUrl = full_url(data['uploadUrl'])
            f = open(filename, 'rb')
            fsize = os.stat(filename).st_size
            done = 0
            if 'offset' in data and data['offset'] < fsize:
                done = data['offset']
                f.seek(done)
                resume_offset = done
            else:
                resume_offset = 0
            chunk = f.read(CHUNK_SIZE)
            fname = os.path.basename(filename)
            mime_type = mimetypes.guess_type(fname)[0] or 'application/octet-stream'
            if not isinstance(fname, bytes):
                fname = fname.encode('utf-8')
            while chunk:
                meta = {
                    'offset': str(done)
                }
                if len(chunk) < CHUNK_SIZE or f.tell() == fsize:
                    meta['done'] = '1'
                files = [
                    ('chunk', (fname, chunk, mime_type))
                ]
                try:
                    data = self._json_request(uploadUrl, meta, files=files)
                except KeyboardInterrupt:
                    if not slient:
                        print("\ninterrupted by user.")
                    sys.exit(1)
                except:
                    if not slient:
                        print("uploading chunk failed, will try again in 5 seconds\r", end='')
                    sys.stdout.flush()
                    data = {'result': -1}
                    time.sleep(5)
                if data and 'status' in data:
                    if data['status']['code'] == 403:
                        if not slient:
                            print("login required")
                        return False
                    if data['status']['code'] != 200:
                        if not slient:
                            print("request returned error, will try again in 5 seconds")
                        if self.DEBUG:
                            print(data)
                        time.sleep(5)
                if data and data.get('result') == 1:
                    done += len(chunk)
                    if data.get('offset') not in (None, done):
                        if not slient:
                            print('server offset out of sync, continue from', data['offset'])
                        done = data['offset']
                        f.seek(done)
                    chunk = f.read(CHUNK_SIZE)
            if data and 'result' in data and data.get('result') == 1:
                return data.get('id', True)
            else:
                return False
        return False

def signin(url):
    import sys
    from getpass import getpass
    from .web import auth

    if not url.startswith('http'):
        site = url
        url = 'https://%s/api/' % url
    else:
        site = url.split('/')[2]
    if not url.endswith('/'):
        url += '/'
    api = API(url)
    update = False
    try:
        credentials = auth.get(site)
    except:
        credentials = {}
        print('Please provide your username and password for %s:' % site)
        credentials['username'] = input('Username: ')
        credentials['password'] = getpass('Password: ')
        update = True
    r = api.signin(**credentials)
    if 'errors' in r.get('data', {}):
        for kv in r['data']['errors'].items():
            print('%s: %s' % kv)
        sys.exit(1)
    if update:
        auth.update(site, credentials)
    return api

