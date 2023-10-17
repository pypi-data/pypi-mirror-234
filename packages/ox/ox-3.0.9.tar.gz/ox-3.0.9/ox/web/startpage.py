# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import urllib

import lxml.html
import ox

DEFAULT_MAX_RESULTS = 10
DEFAULT_TIMEOUT = 24*60*60

def read_url(url, data=None, headers=ox.net.DEFAULT_HEADERS, timeout=DEFAULT_TIMEOUT):
    return ox.cache.read_url(url, data, headers, timeout, unicode=True)

def quote_plus(s):
    if not isinstance(s, bytes):
        s = s.encode('utf-8')
    return urllib.parse.quote_plus(s)

def find(query, max_results=DEFAULT_MAX_RESULTS, timeout=DEFAULT_TIMEOUT):
    """
    Return max_results tuples with title, url, description 

    >>> find("The Matrix site:imdb.com", 1)[0][0]
    'The Matrix (1999) - IMDb'

    >>> find("The Matrix site:imdb.com", 1)[0][1]
    'http://www.imdb.com/title/tt0133093/'
    """
    results = []
    url = 'https://eu1.startpage.com/do/search?nosteeraway=1&abp=1&language=english&cmd=process_search&query=%s&x=0&y=0&cat=web&engine0=v1all' % quote_plus(query)

    data = read_url(url, timeout=timeout)
    doc = lxml.html.document_fromstring(data)
    for r in doc.xpath("//div[contains(@class, 'result')]"):
        t = r.find('h3')
        if t is not None:
            title = t.text_content().strip()
            url = t.find('a').attrib['href']
            description = r.find_class('desc')[0].text_content()
            results.append((title, url, description))
            if len(results) >= max_results:
                break
    return results

