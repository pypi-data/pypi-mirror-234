# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from __future__ import print_function
import re

import lxml.html

from ox import strip_tags, decode_html
from ox.cache import read_url


def get_id(url):
    return url.replace('http://www.ubu.com/', '').split('.html')[0].replace('/./', '/')

def get_url(id):
    return 'http://www.ubu.com/%s.html' % id

def get_data(url):
    if not url.startswith('http:'):
        url = get_url(url)
    data = read_url(url, unicode=True)
    m = {
        'id': get_id(url),
        'url': url,
        'type': re.compile('ubu.com/(.*?)/').findall(url)[0]
    }
    if m['type'] == 'sound':
        m['tracks'] = [{
            'title': strip_tags(decode_html(t[1])).strip(),
            'url': t[0]
        } for t in re.compile('"(http.*?.mp3)"[^>]*>(.+)</a', re.IGNORECASE).findall(data)]
    else:
        for videourl, title in re.compile('href="(http://ubumexico.centro.org.mx/.*?)">(.*?)</a>').findall(data):
            if videourl.endswith('.srt'):
                m['srt'] = videourl
            elif not 'video' in m:
                m['video'] = videourl
                m['video'] = m['video'].replace('/video/ ', '/video/').replace(' ', '%20')
                if m['video'] == 'http://ubumexico.centro.org.mx/video/':
                    del m['video']
            if not 'title' in m:
                m['title'] = strip_tags(decode_html(title)).strip()
        if not 'url' in m:
            print(url, 'missing')
        if 'title' in m:
            m['title'] = re.sub('(.*?) \(\d{4}\)$', '\\1', m['title'])

        if not 'title' in m:
            match = re.compile('<span id="ubuwork">(.*?)</span>').findall(data)
            if match:
                m['title'] = strip_tags(decode_html(match[0])).strip()
        if not 'title' in m:
            match = re.compile("<title>.*?&amp;(.*?)</title>", re.DOTALL).findall(data)
            if match:
                m['title'] = re.sub('\s+', ' ', match[0]).strip()
                if ' - ' in m['title']:
                    m['title'] = m['title'].split(' - ', 1)[-1]
        if 'title' in m:
            m['title'] = strip_tags(decode_html(m['title']).strip())
        match = re.compile("flashvars','file=(.*?.flv)'").findall(data)
        if match:
            m['flv'] = match[0]
            m['flv'] = m['flv'].replace('/video/ ', '/video/').replace(' ', '%20')

        match = re.compile('''src=(.*?) type="video/mp4"''').findall(data)
        if match:
            m['mp4'] = match[0].strip('"').strip("'").replace(' ', '%20')
            if not m['mp4'].startswith('http'):
                m['mp4'] = 'http://ubumexico.centro.org.mx/video/' + m['mp4']
        elif 'video' in m and (m['video'].endswith('.mp4') or m['video'].endswith('.m4v')):
            m['mp4'] = m['video']

        doc = lxml.html.document_fromstring(read_url(url))
        desc = doc.xpath("//div[contains(@id, 'ubudesc')]")
        if len(desc):
            txt = []
            for part in desc[0].text_content().split('\n\n'):
                if part == 'RESOURCES:':
                    break
                if part.strip():
                    txt.append(part)
            if txt:
                if len(txt) > 1 and txt[0].strip() == m.get('title'):
                    txt = txt[1:]
                m['description'] = '\n\n'.join(txt).split('RESOURCES')[0].split('RELATED')[0].strip()
        y = re.compile('\((\d{4})\)').findall(data)
        if y:
            m['year'] = int(y[0])
        d = re.compile('Director: (.+)').findall(data)
        if d:
            m['director'] = strip_tags(decode_html(d[0])).strip()

        a = re.compile('<a href="(.*?)">Back to (.*?)</a>', re.DOTALL).findall(data)
        if a:
            m['artist'] = strip_tags(decode_html(a[0][1])).strip()
        else:
            a = re.compile('<a href="(.*?)">(.*?) in UbuWeb Film').findall(data)
            if a:
                m['artist'] = strip_tags(decode_html(a[0][1])).strip()
            else:
                a = re.compile('<b>(.*?)\(b\..*?\d{4}\)').findall(data)
                if a:
                    m['artist'] = strip_tags(decode_html(a[0])).strip()
                elif m['id'] == 'film/lawder_color':
                    m['artist'] = 'Standish Lawder'

        if 'artist' in m:
            m['artist'] = m['artist'].replace('in UbuWeb Film', '')
            m['artist'] = m['artist'].replace('on UbuWeb Film', '').strip()
        if m['id'] == 'film/coulibeuf':
            m['title'] = 'Balkan Baroque'
            m['year'] = 1999
    return m

def get_films():
    ids = get_ids()
    films = []
    for id in ids:
        info = get_data(id)
        if info['type'] == 'film' and ('flv' in info or 'video' in info):
            films.append(info)
    return films

def get_ids():
    data = read_url('http://www.ubu.com/film/')
    ids = []
    author_urls = []
    for url, author in re.compile('<a href="(\./.*?)">(.*?)</a>').findall(data):
        url = 'http://www.ubu.com/film' + url[1:]
        data = read_url(url)
        author_urls.append(url)
        for u, title in re.compile('<a href="(.*?)">(.*?)</a>').findall(data):
            if not u.startswith('http'):
                if u == '../../sound/burroughs.html':
                    u = 'http://www.ubu.com/sound/burroughs.html'
                elif u.startswith('../'):
                    u = 'http://www.ubu.com/' + u[3:]
                else:
                    u = 'http://www.ubu.com/film/' + u
                if u not in author_urls and u.endswith('.html'):
                    ids.append(u)
    ids = [get_id(url) for url in list(set(ids))]
    return ids

def get_sound_ids():
    data = read_url('http://www.ubu.com/sound/')
    ids = []
    for url, author in re.compile('<a href="(\./.*?)">(.*?)</a>').findall(data):
        url = 'http://www.ubu.com/sound' + url[1:]
        ids.append(url)
    ids = [get_id(url) for url in sorted(set(ids))]
    return ids
