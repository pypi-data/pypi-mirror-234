# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from __future__ import print_function

import re
from ox.net import read_url

def get_poster_url(id):
    url = 'http://piratecinema.org/posters/'
    html = read_url(url).decode('utf-8')
    results = re.compile('src="(.+)" title=".+\((\d{6}\d+)\)"').findall(html)
    for result in results:
        if result[1] == id:
            return url + result[0]
    return ''

if __name__ == '__main__':
    print(get_poster_url('0749451'))

