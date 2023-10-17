# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re

import urllib
import ox
from ox import strip_tags, decode_html
from ox.cache import read_url
import lxml.html


def find(query, timeout=ox.cache.cache_timeout):
    """
    Returns tuples with title, url, description
    """
    if not isinstance(query, bytes):
        query = query.encode('utf-8')
    params = urllib.parse.urlencode({'q': query})
    url = 'http://duckduckgo.com/html/?' + params
    data = read_url(url, timeout=timeout).decode('utf-8')
    doc = lxml.html.document_fromstring(data)
    results = []
    for e in doc.xpath("//a[contains(@class, 'result__a')]"):
        url = e.attrib['href']
        if 'uddg=' in url:
            url = urllib.parse.unquote(url.split('&uddg=')[-1])
        title = e.text_content()
        description = ''
        results.append((title, url, description))
    return results
