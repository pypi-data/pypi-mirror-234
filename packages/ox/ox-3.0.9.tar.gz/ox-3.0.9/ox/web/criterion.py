# -*- coding: UTF-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from __future__ import print_function
import re

import ox.cache
from ox.cache import read_url
from ox.html import strip_tags, decode_html
from ox.text import find_re

from . import imdb

def get_id(url):
    return url.split("/")[-1]

def get_url(id):
    return "https://www.criterion.com/films/%s" % id

def get_data(id, timeout=ox.cache.cache_timeout, get_imdb=False):
    '''
    >>> get_data('1333').get('imdbId')
    '0060304'

    >>> get_data('236')['posters'][0]
    'http://s3.amazonaws.com/criterion-production/release_images/1586/ThirdManReplace.jpg'

    >>> get_data('786')['posters'][0]
    'http://s3.amazonaws.com/criterion-production/product_images/185/343_box_348x490.jpg'
    '''
    data = {
        "id": id,
        "url": get_url(id)
    }
    try:
        html = read_url(data["url"], timeout=timeout, unicode=True)
    except:
        html = read_url(data["url"], timeout=timeout).decode('utf-8', 'ignore')

    data["number"] = find_re(html, "<b>Spine #(\d+)")

    data["title"] = decode_html(find_re(html, "<h1 class=\"header__primarytitle\".*?>(.*?)</h1>"))
    data["title"] = data["title"].split(' \u2014 The Television Version')[0].strip()
    results = find_re(html, '<ul class="film-meta-list">(.*?)</ul>')
    info = re.compile('<li itemprop="(.*?)".*?>(.*?)</li>', re.DOTALL).findall(results)
    info = {k: strip_tags(v).strip() for k, v in info}
    meta = re.compile('<meta.*? name="(.*?)".*? content="(.*?)"', re.DOTALL).findall(html)
    meta = {k: v.strip() for k, v in meta}
    if 'director' in info:
        data['director'] = info['director']
    elif 'director' in meta:
        data['director'] = meta['director']
    if 'countryOfOrigin' in info:
        data['country'] = [c.strip() for c in decode_html(info['countryOfOrigin']).split(', ')]
    if 'inLanguage' in info:
        data['language'] = [l.strip() for l in decode_html(info['inLanguage']).split(', ')]
    for v in re.compile('<li>(.*?)</li>', re.DOTALL).findall(results):
        if 'datePublished' in v:
            data['year'] = strip_tags(v).strip()
        elif 'duration' in v:
            data['duration'] = strip_tags(v).strip()
    data["synopsis"] = decode_html(strip_tags(find_re(html,
                                   "<div class=\"product-summary\".*?>.*?<p>(.*?)</p>")))

    result = find_re(html, "<div class=\"purchase\">(.*?)</div>")
    if 'Blu-Ray' in result or 'Essential Art House DVD' in result:
        r = re.compile('<h3 class="section_title first">Other Editions</h3>(.*?)</div>', re.DOTALL).findall(html)
        if r:
            result = r[0]
    result = find_re(result, "<a href=\"(.*?)\"")
    if not "/boxsets/" in result:
        data["posters"] = [result]
    else:
        html_ = read_url(result, unicode=True)
        result = find_re(html_, '//www.criterion.com/films/%s.*?">(.*?)</a>' % id)
        result = find_re(result, "src=\"(.*?)\"")
        if result:
            data["posters"] = [result.replace("_w100", "")]
        else:
            data["posters"] = []
    data['posters'] = [re.sub('(\?\d+)$', '', p) for p in data['posters']]
    data['posters'] = [p for p in data['posters'] if p]

    posters = find_re(html, '<div class="product-box-art".*?>(.*?)</div>')
    for poster in re.compile('<img src="(.*?)"').findall(posters):
        data['posters'].append(poster)

    result = re.compile('<div class="gallery-item ">.*?src="(.*?)"', re.DOTALL).findall(html)
    #result = find_re(html, "<img alt=\"Film Still\" height=\"252\" src=\"(.*?)\"")
    if result:
        data["stills"] = [result]
        data["trailers"] = []
    else:
        data["stills"] = list(filter(lambda x: x, [find_re(html, "\"thumbnailURL\", \"(.*?)\"")]))
        data["trailers"] = list(filter(lambda x: x, [find_re(html, "\"videoURL\", \"(.*?)\"")]))

    if timeout == ox.cache.cache_timeout:
        timeout = -1
    if get_imdb and 'title' in data and 'director' in data:
        # removed year, as "title (year)" may fail to match
        data['imdbId'] = imdb.get_movie_id(data['title'], data['director'], timeout=timeout)
    return data

def get_ids(page=None):
    ids = []
    html = read_url("https://www.criterion.com/shop/browse/list?sort=spine_number", unicode=True)
    results = re.compile("films/(\d+)-").findall(html)
    ids += results
    results = re.compile("boxsets/(.*?)\"").findall(html)
    for result in results:
        html = read_url("https://www.criterion.com/boxsets/" + result, unicode=True)
        results = re.compile("films/(\d+)-").findall(html)
        ids += results
    return sorted(set(ids), key=int)


if __name__ == '__main__':
    print(get_ids())
