# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2008
from __future__ import division, print_function
from distutils.spawn import find_executable
from glob import glob
import hashlib
import os
import re
import shutil
import sqlite3
import struct
import subprocess

from .utils import json

__all__ = ['sha1sum', 'oshash', 'avinfo', 'makedirs', 'iexists']

EXTENSIONS = {
    'audio': [
        'aac', 'aif', 'aiff', 'amr',
        'flac', 'm4a', 'mp3', 'oga', 'ogg', 'wav', 'wma', 'opus',
        'ra',  # Real Audio
    ],
    'image': [
        'bmp', 'gif', 'jpeg', 'jpg', 'png', 'svg', 'webp'
    ],
    'subtitle': [
        'idx', 'srt', 'sub', 'vtt'
    ],
    'video': [
        '3gp',
        'avi', 'divx', 'dv', 'flv', 'm2t', 'm2ts', 'm2v', 'm4v', 'mkv', 'mov', 'mp4',
        'mpeg', 'mpg', 'mts', 'ogm', 'ogv', 'vob', 'webm', 'wmv', 'asf',
        'mod', 'tod',  # http://en.wikipedia.org/wiki/MOD_and_TOD
        'mxf', 'ts',
        'dat',  # VOD files
        'rm', 'rmvb',  # Real Media
    ],
}

def cmd(program):
    local = os.path.expanduser('~/.ox/bin/%s' % program)
    if os.path.exists(local):
        program = local
    return program

def _get_file_cache():
    import ox.cache
    path = ox.cache.cache_path()
    if path.startswith('fs:'):
        path = path[3:]
    return os.path.join(path, 'files.sqlite')

def cache(filename, type='oshash', update=False):
    conn = sqlite3.connect(_get_file_cache(), timeout=10)
    conn.row_factory = sqlite3.Row

    if not cache.init:
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS cache (path varchar(1024) unique, oshash varchar(16), sha1 varchar(42), size int, mtime int, info text)')
        c.execute('CREATE INDEX IF NOT EXISTS cache_oshash ON cache (oshash)')
        c.execute('CREATE INDEX IF NOT EXISTS cache_sha1 ON cache (sha1)')
        conn.commit()
        cache.init = True
    c = conn.cursor()
    c.execute('SELECT oshash, sha1, info, size, mtime FROM cache WHERE path = ?', (filename, ))
    stat = os.stat(filename)
    row = None
    h = None
    sha1 = None
    info = ''
    for row in c:
        if stat.st_size == row['size'] and int(stat.st_mtime) == int(row['mtime']):
            if not update:
                value = row[type]
                if value:
                    if type == 'info':
                        value = json.loads(value)
                    return value
            h = row['oshash']
            sha1 = row['sha1']
            info = row['info']
    if type == 'oshash':
        value = h = oshash(filename, cached=False)
    elif type == 'sha1':
        value = sha1 = sha1sum(filename, cached=False)
    elif type == 'info':
        value = avinfo(filename, cached=False)
        info = json.dumps(value)
    t = (filename, h, sha1, stat.st_size, int(stat.st_mtime), info)
    with conn:
        sql = u'INSERT OR REPLACE INTO cache values (?, ?, ?, ?, ?, ?)'
        c.execute(sql, t)
    return value
cache.init = None

def cleanup_cache():
    conn = sqlite3.connect(_get_file_cache(), timeout=10)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT path FROM cache')
    paths = [r[0] for r in c]
    for path in paths:
        if not os.path.exists(path):
            c.execute('DELETE FROM cache WHERE path = ?', (path, ))
    conn.commit()
    c.execute('VACUUM')
    conn.commit()

def sha1sum(filename, cached=False):
    if cached:
        return cache(filename, 'sha1')
    sha1 = hashlib.sha1()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(128*sha1.block_size), b''):
            sha1.update(chunk)
    return sha1.hexdigest()

'''
    os hash - http://trac.opensubtitles.org/projects/opensubtitles/wiki/HashSourceCodes
    plus modification for files < 64k, buffer is filled with file data and padded with 0
'''
def oshash(filename, cached=True):
    if cached:
        return cache(filename, 'oshash')
    try:
        longlongformat = 'q'  # long long
        bytesize = struct.calcsize(longlongformat)

        f = open(filename, "rb")

        filesize = os.path.getsize(filename)
        hash = filesize
        if filesize < 65536:
            for x in range(int(filesize/bytesize)):
                buffer = f.read(bytesize)
                (l_value,) = struct.unpack(longlongformat, buffer)
                hash += l_value
                hash = hash & 0xFFFFFFFFFFFFFFFF  # to remain as 64bit number
        else:
            for x in range(int(65536/bytesize)):
                buffer = f.read(bytesize)
                (l_value,) = struct.unpack(longlongformat, buffer)
                hash += l_value
                hash = hash & 0xFFFFFFFFFFFFFFFF  # to remain as 64bit number
            f.seek(max(0, filesize-65536), 0)
            for x in range(int(65536/bytesize)):
                buffer = f.read(bytesize)
                (l_value,) = struct.unpack(longlongformat, buffer)
                hash += l_value
                hash = hash & 0xFFFFFFFFFFFFFFFF
        f.close()
        returnedhash = "%016x" % hash
        return returnedhash
    except IOError:
        return "IOError"

def avinfo(filename, cached=True):
    if cached:
        return cache(filename, 'info')
    if os.path.getsize(filename):
        if find_executable('ffprobe'):
            return ffprobe(filename)
        raise EnvironmentError('could to find ffprobe. please install ffmpeg')
    return {'path': filename, 'size': 0}


def ffprobe(filename):
    p = subprocess.Popen([
        cmd('ffprobe'),
        '-show_format',
        '-show_chapters',
        '-show_streams',
        '-print_format',
        'json',
        '-i', filename

    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    info, error = p.communicate()
    info = info.decode('utf-8')
    ffinfo = json.loads(info)

    def fix_value(key, value):
        if key == 'r_frame_rate':
            value = value.replace('/', ':')
        elif key == 'bit_rate':
            value = float(value) / 1000
        elif key == 'duration':
            value = float(value)
        elif key == 'size':
            value = int(value)
        return value

    info = {}
    if 'format' not in ffinfo:
        info['error'] = 'badfile'
    else:
        for key in ('duration', 'size', 'bit_rate'):
            if key in ffinfo['format']:
                info[{
                    'bit_rate': 'bitrate'
                }.get(key, key)] = fix_value(key, ffinfo['format'][key])
        info['audio'] = []
        info['video'] = []
        info['metadata'] = ffinfo['format'].get('tags', {})
        chapters = ffinfo.get('chapters', [])
        if chapters:
            info['chapters'] = [
                {
                    'in': float(chapter['start_time']),
                    'out': float(chapter['end_time']),
                    'value': chapter.get('tags', {}).get('title')
                }
                for chapter in chapters if chapter.get('tags', {}).get('title')
            ]
        for s in ffinfo['streams']:
            tags = s.pop('tags', {})
            side_data_list = s.pop('side_data_list', [])
            language = None
            for t in tags:
                if t == 'language':
                    language = tags[t]
                else:
                    info['metadata'][t] = tags[t]
            for kv in side_data_list:
                for k, v in kv.items():
                    info['metadata'][k] = v
            if s.get('codec_type') in ('audio', 'video'):
                stream = {}
                if language and language != 'und':
                    stream['language'] = language
                keys = [ 
                    'codec_name',
                    'width',
                    'height',
                    'bit_rate',
                    'index',
                    'display_aspect_ratio',
                    'sample_rate',
                    'channels',
                ]
                if s['codec_type'] == 'video':
                    keys += [
                        'sample_aspect_ratio',
                        'r_frame_rate',
                        'pix_fmt',
                    ]

                for key in keys:
                    if key in s:
                        stream[{
                            'codec_name': 'codec',
                            'bit_rate': 'bitrate',
                            'index': 'id',
                            'r_frame_rate': 'framerate',
                            'sample_rate': 'samplerate',
                            'pix_fmt': 'pixel_format',
                            'sample_aspect_ratio': 'pixel_aspect_ratio',
                        }.get(key, key)] = fix_value(key, s[key])
                info[s['codec_type']].append(stream)
            elif s.get('codec_type') == 'subtitle':
                info['subtitles'] = info.get('subtitles', [])
                stream = {}
                if language and language != 'und':
                    stream['language'] = language
                for key in (
                    'codec_name',
                    'language',
                    'width',
                    'height',
                ):
                    if key in s:
                        stream[{
                            'codec_name': 'codec',
                        }.get(key, key)] = s[key]
                info['subtitles'].append(stream)
            else:
                pass
                # print s
        for v in info['video']:
            k = 'display_aspect_ratio'
            if 'rotate' in info.get('metadata', {}) and int(info['metadata']['rotate']) in (-90, 90):
                v['width'], v['height'] = v['height'], v['width']
                if k in v:
                    v[k] = ':'.join(reversed(v[k].split(':')))
            elif 'rotation' in info.get('metadata', {}) and int(info['metadata']['rotation']) in (-90, 90):
                v['width'], v['height'] = v['height'], v['width']
                if k in v:
                    v[k] = ':'.join(reversed(v[k].split(':')))
            if k not in v and 'width' in v \
                    or (k in v and v[k] == '0:1'):
                v[k] = '%d:%d' % (v['width'], v['height'])
                v['pixel_aspect_ratio'] = '1:1'
    info['oshash'] = oshash(filename)
    info['path'] = filename
    if 'size' not in info:
        info['size'] = os.path.getsize(filename)

    fix_coverart(info)
    return info

def fix_coverart(info):
    if info.get('video') \
            and info['path'].split('.')[-1] in EXTENSIONS['audio'] \
            and info['video'][0]['codec'] in EXTENSIONS['image'] + ['mjpeg']:
        info['cover'] = info.pop('video')
        info['video'] = []
    return info

def makedirs(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != 17:
                raise

def copy_file(source, target, verbose=False):
    if verbose:
        print('copying', source, 'to', target)
    write_path(target)
    shutil.copyfile(source, target)

def read_file(file, verbose=False):
    if verbose:
        print('reading', file)
    f = open(file, 'rb')
    data = f.read()
    f.close()
    return data

def read_json(file, verbose=False):
    if verbose:
        print('reading', file)
    with open(file) as fd:
        data = json.load(fd)
    return data

def write_file(file, data, verbose=False):
    if verbose:
        print('writing', file)
    if not isinstance(data, bytes):
        data = data.encode('utf-8')
    write_path(file)
    f = open(file, 'wb')
    f.write(data)
    f.close()
    return len(data)

def write_image(file, image, verbose=False):
    if verbose:
        print('writing', file)
    write_path(file)
    image.save(file)

def write_json(file, data, ensure_ascii=True, indent=0, sort_keys=False, verbose=False):
    data = json.dumps(data, ensure_ascii=ensure_ascii, indent=indent, sort_keys=sort_keys)
    write_file(file, data if ensure_ascii else data.encode('utf-8'), verbose=verbose)

def write_link(source, target, verbose=False):
    if verbose:
        print('linking', source, 'to', target)
    write_path(target)
    if os.path.exists(target):
        os.unlink(target)
    os.symlink(source, target)

def write_path(file):
    path = os.path.split(file)[0]
    if path and not os.path.exists(path):
        os.makedirs(path)

def iexists(path):
    parts = path.split(os.sep)
    name = parts[-1].lower()
    if len(parts) == 1:
        folder = '.'
    else:
        folder = os.path.dirname(path)
    try:
        files = os.listdir(folder)
    except FileNotFoundError:
        return False
    files = {os.path.basename(f).lower() for f in files}
    return name in files
