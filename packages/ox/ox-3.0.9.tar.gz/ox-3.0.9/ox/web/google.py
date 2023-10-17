# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re
import urllib

import ox
from ox import strip_tags, decode_html

DEFAULT_MAX_RESULTS = 10
DEFAULT_TIMEOUT = 24*60*60

def read_url(url, data=None, headers=ox.net.DEFAULT_HEADERS, timeout=DEFAULT_TIMEOUT):
    return ox.cache.read_url(url, data, headers, timeout, unicode=True)

def quote_plus(s):
    if not isinstance(s, bytes):
        s = s.encode('utf-8')
    return urllib.parse.quote_plus(s)


def infobox(query, timeout=DEFAULT_TIMEOUT):
    import lxml.html
    data = read_url(url, timeout=timeout)
    doc = lxml.html.document_fromstring(data)
    k = 'kp-wholepage'
    wholepage = doc.cssselect('.' + k)
    infobox = {}
    if wholepage:
        page = wholepage[0]
        for a in page.cssselect('a'):
            if a.attrib.get('href', '').startswith('http'):
                domain = '.'.join(a.attrib['href'].split('/')[2].split('.')[-2:])
                infobox[domain] = a.attrib['href']
        for e in page.cssselect('*[data-attrid]'):
            key = e.attrib['data-attrid']
            value = e.text_content()
            if value and key not in (
                'kc:/film/film:media_actions_wholepage',
                'action:watch_film'
            ):
                infobox[key] = value
    return infobox


def find(query, max_results=DEFAULT_MAX_RESULTS, timeout=DEFAULT_TIMEOUT):
    """
    Return max_results tuples with title, url, description 

    >>> str(find("The Matrix site:imdb.com", 1)[0][0])
    'The Matrix (1999) - IMDb'

    >>> str(find("The Matrix site:imdb.com", 1)[0][1])
    'http://www.imdb.com/title/tt0133093/'
    """
    results = []
    offset = 0
    while len(results) < max_results:
        url = 'http://google.com/search?q=%s' % quote_plus(query)
        if offset:
            url += '&start=%d' % offset
        data = read_url(url, timeout=timeout)
        data = re.sub('<span class="f">(.*?)</span>', '\\1', data)
        for a in re.compile('<a href="(htt\S+?)".*?>(.*?)</a>.*?<span class="st">(.*?)<\/span>').findall(data):
            results.append((strip_tags(decode_html(a[1])), a[0], strip_tags(decode_html(a[2]))))
            if len(results) >= max_results:
                break
        offset += 10
    return results

