# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from collections import defaultdict

import json
import re
import time
import unicodedata

from urllib.parse import urlencode

from .. import find_re, strip_tags, decode_html
from .. import cache


from . siteparser import SiteParser
from . import duckduckgo
from ..utils import datetime
from ..geo import normalize_country_name, get_country_name


def prepare_url(url, data=None, headers=cache.DEFAULT_HEADERS, timeout=cache.cache_timeout, valid=None, unicode=False):
    headers = headers.copy()
    # https://webapps.stackexchange.com/questions/11003/how-can-i-disable-reconfigure-imdbs-automatic-geo-location-so-it-does-not-defau
    #headers['X-Forwarded-For'] = '72.21.206.80'
    headers['Accept-Language'] = 'en'

    return url, data, headers, timeout, unicode

def read_url(url, data=None, headers=cache.DEFAULT_HEADERS, timeout=cache.cache_timeout, valid=None, unicode=False):
    url, data, headers, timeout, unicode = prepare_url(url, data, headers, timeout, valid, unicode)
    return cache.read_url(url, data, headers, timeout, unicode=unicode)

def delete_url(url, data=None, headers=cache.DEFAULT_HEADERS):
    url, data, headers, timeout, unicode = prepare_url(url, data, headers)
    cache.store.delete(url, data, headers)

def get_url(id):
    return "http://www.imdb.com/title/tt%s/" % id


def reference_section(id):
    return {
        'page': 'reference',
        're': [
            '<h4 name="{id}" id="{id}".*?<table(.*?)</table>'.format(id=id),
            '<a href="/name/.*?>(.*?)</a>'
        ],
        'type': 'list'
    }


def zebra_list(label, more=None):
    conditions = {
        'page': 'reference',
        're': [
            '_label">' + label + '</td>.*?<ul(.*?)</ul>',
            '<li.*?>(.*?)</li>'
        ],
        'type': 'list',
    }
    if more:
        conditions['re'] += more
    return conditions

def zebra_table(label, more=None, type='string'):
    conditions = {
        'page': 'reference',
        're': [
            '_label">' + label + '</td>.*?<td>(.*?)</td>',
        ],
        'type': type,
    }
    if more:
        conditions['re'] += more
    return conditions

def parse_aspectratio(value):
    r = value
    if ':' in value:
        r = value.split(':')
        n = r[0]
        d = r[1].strip().split(' ')[0]
        try:
            if float(d):
                value = str(float(n) / float(d))
            else:
                value = str(float(n))
        except:
            print('failed to parse aspect: %s' % value)
    else:
        value = '.'.join(value.strip().split('.')[:2])
    return value


def technical(label):
    return {
        'page': 'technical',
        're': [
            '<td class="label">\s*?%s\s*?</td>.*?<td>\s*?(.*?)\s*?</td>' % label,
            lambda data: [
                re.sub('\s+', ' ', d.strip()) for d in data.strip().split('<br>')
            ] if data else []
        ],
        'type': 'list'
    }


def tech_spec(metadata):
    tech = {}
    for row in metadata['props']['pageProps']['contentData']['section']['items']:
        title = {
            'aspect ratio': 'aspectratio',
            'sound mix': 'sound',
        }.get(row['rowTitle'].lower(), row['rowTitle'].lower())
        tech[title] = []
        for content in row['listContent']:
            value = content['text']
            tech[title].append(value)
    return tech


def movie_connections(metadata):
    
    connections = {}
    if 'props' not in metadata:
        return connections
    for row in metadata['props']['pageProps']['contentData']['categories']:
        title = {
        }.get(row['name'], row['name'])
        if title not in connections:
            connections[title] = []

        for item in row['section']['items']:
            item_ = {
                'id': item['id'][2:],
            }

            item_['title'] = re.compile('<a.*?>(.*?)</a>').findall(item['listContent'][0]['html'])[0]
            if len(item['listContent']) >=2:
                item_['description'] = strip_tags(item['listContent'][1]['html'])
            connections[title].append(item_)
    return connections


def get_category_by_id(metadata, id):
    for category in metadata['props']['pageProps']['contentData']['categories']:
        if category['id'] == id:
            return category


def get_release_date(metadata):
    releases = get_category_by_id(metadata, 'releases')
    def parse_date(d):
        parsed = None
        for fmt in (
            '%B %d, %Y',
            '%d %B %Y',
            '%B %Y',
        ):
            try:
                parsed = datetime.strptime(d, fmt)
                break
            except:
                pass
        if not parsed:
            return None
        return '%d-%02d-%02d' % (parsed.year, parsed.month, parsed.day)

    dates = []
    for item in releases['section']['items']:
        content = item['listContent'][0]
        date = parse_date(content['text'])
        if date:
            dates.append(date)

    if dates:
        return min(dates)

def get_locations(metadata):
    try:
        locations = [
            row['cardText']
            for row in metadata['props']['pageProps']['contentData']['categories'][0]['section']['items']
        ]
    except:
        locations = []
    return locations


def get_keywords(metadata):
    try:
        keywords = [
            row['rowTitle']
            for row in metadata['props']['pageProps']['contentData']['section']['items']
        ]
    except:
        keywords = []
    return keywords


def get_entity_metadata(metadata):
    data = {}
    entity = metadata['props']['pageProps']['contentData']['entityMetadata']
    data['title'] = entity['titleText']['text']
    data['originalTitle'] = entity['originalTitleText']['text']
    data['year'] = entity['releaseYear']['year']
    data['plot'] = entity['plot']['plotText']['plainText']
    data['country'] = [get_country_name(c['id']) for c in entity['countriesOfOrigin']['countries']]
    data['poster'] = metadata['props']['pageProps']['contentData']['posterData']['image']['url']
    return data


def alternative_titles(metadata):
    titles = defaultdict(list)
    akas = get_category_by_id(metadata, 'akas')

    skip = [
        metadata['props']['pageProps']['contentData']['entityMetadata']['titleText']['text'],
        metadata['props']['pageProps']['contentData']['entityMetadata']['originalTitleText']['text']
    ]
    for row in akas['section']['items']:
        content = row['listContent'][0]
        title = content['text']
        country = row['rowTitle']
        if title in skip:
            continue
        titles[title].append(country)
        #if content.get('subText'):
        #    titles[-1]['subText'] = content['subText']
    return [kv for kv in titles.items()]


'''
'posterIds': {
    'page': 'posters',
    're': '/unknown-thumbnail/media/rm(.*?)/tt',
    'type': 'list'
},
'''

class Imdb(SiteParser):
    '''
    >>> Imdb('0068646')['title'] == 'The Godfather'
    True

    >>> Imdb('0133093')['title'] == 'The Matrix'
    True
    '''
    regex = {
        'alternativeTitles': {
            'page': 'releaseinfo',
            're': [
                '<li role="presentation" class="ipc-metadata-list__item" data-testid="list-item"><button class="ipc-metadata-list-item__label" role="button" tabindex="0" aria-disabled="false">([^>]+)</button.*?<li role="presentation" class="ipc-inline-list__item"><label class="ipc-metadata-list-item__list-content-item"[^>]*?>([^<]+)</label>',
            ],
            'type': 'list'
        },
        'aspectratio': {
            'page': 'reference',
            're': [
                'Aspect Ratio</td>.*?ipl-inline-list__item">\s+([\d\.\:\ ]+)',
                parse_aspectratio,
            ],
            'type': 'float',
        },
        'budget': zebra_table('Budget', more=[
            lambda data: find_re(decode_html(data).replace(',', ''), '\d+')
        ], type='int'),
        'cast': {
            'page': 'reference',
            're': [
                ' <table class="cast_list">(.*?)</table>',
                '<td.*?itemprop="actor".*?>.*?>(.*?)</a>.*?<td class="character">(.*?)</td>',
                lambda ll: [strip_tags(l) for l in ll] if isinstance(ll, list) else strip_tags(ll)
            ],
            'type': 'list'
        },
        'cinematographer': reference_section('cinematographers'),
        'country': zebra_list('Country', more=['<a.*?>(.*?)</a>']),
        'director': reference_section('directors'),
        'editor': reference_section('editors'),
        'composer': reference_section('composers'),
        'episodeTitle': {
            'page': 'reference',
            're': '<h3 itemprop="name">(.*?)<',
            'type': 'string'
        },
        'genre': zebra_list('Genres', more=['<a.*?>(.*?)</a>']),
        'gross': zebra_table('Cumulative Worldwide Gross', more=[
            lambda data: find_re(decode_html(data).replace(',', ''), '\d+')
        ], type='int'),
        'language': zebra_list('Language', more=['<a.*?>(.*?)</a>']),
        'originalTitle': {
            'page': 'releaseinfo',
            're': '<li role="presentation" class="ipc-metadata-list__item" data-testid="list-item"><button class="ipc-metadata-list-item__label" role="button" tabindex="0" aria-disabled="false">\(original title\)</button.*?<li role="presentation" class="ipc-inline-list__item"><label class="ipc-metadata-list-item__list-content-item"[^>]*?>([^<]+)</label>',
            'type': 'string'
        },
        'summary': zebra_table('Plot Summary', more=[
            '<p>(.*?)<em'
        ]),
        'storyline': {
            'page': '',
            're': '<h2>Storyline</h2>.*?<p>(.*?)</p>',
            'type': 'string'
        },
        'posterId': {
            'page': 'reference',
            're': '<img.*?class="titlereference-primary-image".*?src="(.*?)".*?>',
            'type': 'string'
        },
        'producer': reference_section('producers'),
        'productionCompany': {
            'page': 'reference',
            're': [
                'Production Companies.*?<ul(.*?)</ul>',
                '<a href="/company/.*?/">(.*?)</a>'
            ],
            'type': 'list'
        },
        'rating': {
            'page': 'reference',
            're': [
                '<div class="ipl-rating-star ">(.*?)</div>',
                'ipl-rating-star__rating">([\d,.]+?)</span>',
            ],
            'type': 'float'
        },
        #FIXME using some /offsite/ redirect now
        #'reviews': {
        #    'page': 'externalreviews',
        #    're': [
        #        '<ul class="simpleList">(.*?)</ul>',
        #        '<li>.*?<a href="(http.*?)".*?>(.*?)</a>.*?</li>'
        #    ],
        #    'type': 'list'
        #},
        'runtime': zebra_list('Runtime'),
        'color': zebra_list('Color', more=[
            '<a.*?>([^(<]+)',
            lambda r: r[0] if isinstance(r, list) else r,
            strip_tags
        ]),
        'season': {
            'page': 'reference',
            're': [
                '<ul class="ipl-inline-list titlereference-overview-season-episode-numbers">(.*?)</ul>',
                'Season (\d+)',
             ],
            'type': 'int'
        },
        'episode': {
            'page': 'reference',
            're': [
                '<ul class="ipl-inline-list titlereference-overview-season-episode-numbers">(.*?)</ul>',
                'Episode (\d+)',
             ],
            'type': 'int'
        },
        'series': {
            'page': 'reference',
            're': '<h4 itemprop="name">.*?<a href="/title/tt(\d+)',
            'type': 'string'
        },
        'isSeries': {
            'page': 'reference',
            're': 'property=\'og:title\'.*?content=".*?(TV series|TV mini-series).*?"',
            'type': 'string'
        },
        'title': {
            'page': 'releaseinfo',
            're': '<h2.*?>(.*?)</h2>',
            'type': 'string'
        },
        'trivia': {
            'page': 'trivia',
            're': [
                '<div class="sodatext">(.*?)<(br|/div)',
                lambda data: data[0]
            ],
            'type': 'list',
        },
        'votes': {
            'page': 'reference',
            're': [
                'class="ipl-rating-star__total-votes">\((.*?)\)',
                lambda r: r.replace(',', '')
            ],
            'type': 'string'
        },
        'writer': reference_section('writers'),
        'year': {
            'page': 'reference',
            're': [
                '<span class="titlereference-title-year">(.*?)</span>',
                '<a.*?>(\d+)',
            ],
            'type': 'int'
        },
        'credits': {
            'page': 'fullcredits',
            're': [
                lambda data: data.split('<h4'),
                '>(.*?)</h4>.*?(<table.*?</table>)',
                lambda data: [d for d in data if d]
            ],
            'type': 'list'
        },
        'laboratory': technical('Laboratory'),
        'camera': technical('Camera'),
    }

    def read_url(self, url, timeout):
        if self.debug:
            print(url)
        if url not in self._cache:
            self._cache[url] = read_url(url, timeout=timeout, unicode=True)
        return self._cache[url]

    def get_page_data(self, page, timeout=-1):
        url = self.get_url(page)
        data = self.read_url(url, timeout)
        pdata = re.compile('<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', re.DOTALL).findall(data)
        if pdata:
            pdata = pdata[0]
            return json.loads(pdata)
        return {}

    def __init__(self, id, timeout=-1):
        # http://www.imdb.com/help/show_leaf?titlelanguagedisplay
        self.baseUrl = "http://www.imdb.com/title/tt%s/" % id
        self._id = id
        if timeout != 0:
            self._cache = {}
            url = self.baseUrl + 'releaseinfo'
            page = self.read_url(url, timeout=-1)
            if '<h2>See also</h2>' in page:
                timeout = 0
        super(Imdb, self).__init__(timeout)

        url = self.baseUrl + 'reference'
        page = self.read_url(url, timeout=-1)
        if '<title>IMDb: Page not found</title>' in page \
            or 'The requested URL was not found on our server.' in page:
            return
        if "<p>We're sorry, something went wrong.</p>" in page:
            time.sleep(1)
            super(Imdb, self).__init__(0)

        if 'alternativeTitles' in self:
            if len(self['alternativeTitles']) == 2 and \
               isinstance(self['alternativeTitles'][0], str):
               self['alternativeTitles'] = [self['alternativeTitles']]

        for key in ('country', 'genre', 'language', 'sound', 'color'):
            if key in self:
                self[key] = [x[0] if len(x) == 1 and isinstance(x, list) else x for x in self[key]]
                self[key] = list(filter(lambda x: x.lower() != 'home', self[key]))

        #normalize country names
        if 'country' in self:
            self['country'] = [normalize_country_name(c) or c for c in self['country']]


        def cleanup_title(title):
            if isinstance(title, list):
                title = title[0]
            if title.startswith('"') and title.endswith('"'):
                title = title[1:-1]
            if title.startswith("'") and title.endswith("'"):
                title = title[1:-1]
            title = re.sub('\(\#[.\d]+\)', '', title)
            return title.strip()

        for t in ('title', 'originalTitle'):
            if t in self:
                self[t] = cleanup_title(self[t])

        if 'alternativeTitles' in self:
            alt = {}
            for t in self['alternativeTitles']:
                if t[0].strip() in ('World-wide (English title)', ):
                    self['title'] = cleanup_title(t[1])
            for t in self['alternativeTitles']:
                title = cleanup_title(t[1])
                if title.lower() not in (self.get('title', '').lower(), self.get('originalTitle', '').lower()):
                    if title not in alt:
                        alt[title] = []
                    for c in t[0].split('/'):
                        for cleanup in ('International', '(working title)', 'World-wide'):
                            c = c.replace(cleanup, '')
                        c = c.split('(')[0].strip()
                        if c:
                            alt[title].append(c)
            self['alternativeTitles'] = []
            for t in sorted(alt, key=lambda a: sorted(alt[a])):
                countries = sorted(set([normalize_country_name(c) or c for c in alt[t]]))
                self['alternativeTitles'].append((t, countries))
            if not self['alternativeTitles']:
                del self['alternativeTitles']

        if 'runtime' in self and self['runtime']:
            if isinstance(self['runtime'], list):
                self['runtime'] = self['runtime'][0]
            if 'min' in self['runtime']:
                base = 60
            else:
                base = 1
            self['runtime'] = int(find_re(self['runtime'], '([0-9]+)')) * base
        if 'runtime' in self and not self['runtime']:
            del self['runtime']

        if 'sound' in self:
            self['sound'] = list(sorted(set(self['sound'])))

        if 'cast' in self:
            if isinstance(self['cast'][0], str):
                self['cast'] = [self['cast']]
            self['actor'] = [c[0] for c in self['cast']]
            def cleanup_character(c):
                c = c.replace('(uncredited)', '').strip()
                c = re.sub('\s+', ' ', c)
                return c
            self['cast'] = [{'actor': x[0], 'character': cleanup_character(x[1])}
                            for x in self['cast']]


        if 'isSeries' in self:
            del self['isSeries']
            self['isSeries'] = True
        if 'episodeTitle' in self:
            self['episodeTitle'] = re.sub('Episode \#\d+\.\d+', '', self['episodeTitle'])


        #make lists unique but keep order
        for key in ('director', 'language'):
            if key in self:
                self[key] = [x for i,x in enumerate(self[key])
                             if x not in self[key][i+1:]]

        for key in ('actor', 'writer', 'producer', 'editor', 'composer'):
            if key in self:
                if isinstance(self[key][0], list):
                    self[key] = [i[0] for i in self[key] if i]
                self[key] = sorted(list(set(self[key])), key=lambda a: self[key].index(a))


        if 'budget' in self and 'gross' in self:
            self['profit'] = self['gross'] - self['budget']

        metadata = self.get_page_data('releaseinfo')
        releasedate = get_release_date(metadata)
        if releasedate:
            self['releasedate'] = releasedate

        metadata = self.get_page_data('keywords')
        keywords = get_keywords(metadata)
        if keywords:
            self['keyword'] = keywords

        metadata = self.get_page_data('locations')
        locations = get_locations(metadata)
        if locations:
            self['filmingLocations'] = locations

        if 'summary' not in self and 'storyline' in self:
            self['summary'] = self.pop('storyline')
        if 'summary' in self:
            if isinstance(self['summary'], list):
                self['summary'] = self['summary'][0]
            self['summary'] = strip_tags(self['summary'].split('</p')[0]).split('  Written by\n')[0].strip()
        else:

            try:
                summary = metadata['props']['pageProps']['contentData']['entityMetadata']['plot']['plotText']['plainText']
                self['summary'] = summary

            except:
                pass

        #self['connections'] = movie_connections(self.get_page_data('movieconnections'))
        self['connections'] = self._get_connections()

        spec = tech_spec(self.get_page_data('technical'))
        for key in spec:
            if not self.get(key):
                self[key] = spec[key]

        if 'credits' in self:
            credits = [
                [
                    strip_tags(d[0].replace(' by', '')).strip(),
                    [
                        [
                            strip_tags(x[0]).strip(),
                            [t.strip().split(' (')[0].strip() for t in x[2].split(' / ')]
                        ]
                        for x in
                        re.compile('<td class="name">(.*?)</td>.*?<td>(.*?)</td>.*?<td class="credit">(.*?)</td>', re.DOTALL).findall(d[1])
                    ]
                ] for d in self['credits'] if d
            ]
            credits = [c for c in credits if c[1]]

            self['credits'] = []
            self['lyricist'] = []
            self['singer'] = []
            for department, crew in credits:
                department = department.replace('(in alphabetical order)', '').strip()
                for c in crew:
                    name = c[0]
                    roles = c[1]
                    self['credits'].append({
                        'name': name,
                        'roles': roles,
                        'deparment': department
                    })
                    if department == 'Music Department':
                        if 'lyricist' in roles:
                            self['lyricist'].append(name)
                        if 'playback singer' in roles:
                            self['singer'].append(name)
            if not self['credits']:
                del self['credits']

        if 'credits' in self:
            for key, deparment in (
                ('director', 'Series Directed'),
                ('writer', 'Series Writing Credits'),
                ('cinematographer', 'Series Cinematography'),
            ):
                if key not in self:
                    series_credit = [c for c in self['credits'] if c.get('deparment') == deparment]
                    if series_credit:
                        self[key] = [c['name'] for c in series_credit]
        creator = []
        for c in self.get('credits', []):
            if '(created by)' in c['roles'] and c['name'] not in creator:
                creator.append(c['name'])
            if '(creator)' in c['roles'] and c['name'] not in creator:
                creator.append(c['name'])
        if creator:
            self['creator'] = creator

        if 'series' in self:
            series = Imdb(self['series'], timeout=timeout)
            self['seriesTitle'] = series['title']
            if 'episodeTitle' in self:
                self['seriesTitle'] = series['title']
                if 'season' in self and 'episode' in self:
                    self['title'] = "%s (S%02dE%02d) %s" % (
                        self['seriesTitle'], self['season'], self['episode'], self['episodeTitle'])
                else:
                    self['title'] = "%s (S01) %s" % (self['seriesTitle'], self['episodeTitle'])
                    self['season'] = 1
                self['title'] = self['title'].strip()
            if 'director' in self:
                self['episodeDirector'] = self['director']

            if 'creator' not in series and 'director' in series:
                series['creator'] = series['director']
                if len(series['creator']) > 10:
                    series['creator'] = series['director'][:1]

            for key in ['creator', 'country']:
                if key in series:
                    self[key] = series[key]

            if 'year' in series:
                self['seriesYear'] = series['year']
                if 'year' not in self:
                    self['year'] = series['year']

            if 'year' in self:
                self['episodeYear'] = self['year']
            if 'creator' in self:
                self['seriesDirector'] = self['creator']
            if 'originalTitle' in self:
                del self['originalTitle']
        else:
            for key in ('seriesTitle', 'episodeTitle', 'season', 'episode'):
                if key in self:
                    del self[key]
        if 'creator' in self:
            if 'director' in self:
                self['episodeDirector'] = self['director']
            self['director'] = self['creator']

    def _get_connections(self):
        query = '''query {
    title(id: "tt%s") {
        id
        titleText {
           text
        }
        connections(first: 5000) {
            edges {
                node {
                    associatedTitle {
                        id
                        titleText {
                            text
                        }
                    }
                    category {
                        text
                    }
                    text
                }
            }
        }
    }
}
''' % self._id
        url = 'https://caching.graphql.imdb.com/'
        headers = cache.DEFAULT_HEADERS.copy()
        headers.update({
             'Accept': 'application/graphql+json, application/json',
             'Origin': 'https://www.imdb.com',
             'Referer': 'https://www.imdb.com',
             'x-imdb-user-country': 'US',
             'x-imdb-user-language': 'en-US',
             'content-type': 'application/json',
             'Accept-Language': 'en,en-US;q=0.5'
        })
        #response = requests.post(url, json=
        response = json.loads(read_url(url, data=json.dumps({
            "query": query
        }), headers=headers))
        connections = {}
        for c in response['data']['title']['connections']['edges']:
            cat = c['node']['category']['text']
            if cat not in connections:
                connections[cat] = []
            connection = {
                'id': c['node']['associatedTitle']['id'][2:],
                'title': c['node']['associatedTitle']['titleText']['text'],
            }
            description = c['node'].get('text', '')
            if description:
                connection['description'] = description
            connections[cat].append(connection)
        return connections


class ImdbCombined(Imdb):
    def __init__(self, id, timeout=-1):
        _regex = {}
        for key in self.regex:
            if self.regex[key]['page'] in ('releaseinfo', 'reference'):
                _regex[key] = self.regex[key]
        self.regex = _regex
        super(ImdbCombined, self).__init__(id, timeout)

def get_movie_by_title(title, timeout=-1):
    '''
    This only works for exact title matches from the data dump
    Usually in the format
        Title (Year)
        "Series Title" (Year) {(#Season.Episode)}
        "Series Title" (Year) {Episode Title (#Season.Episode)}

    If there is more than one film with that title for the year
        Title (Year/I)

    >>> str(get_movie_by_title(u'"Father Knows Best" (1954) {(#5.34)}'))
    '1602860'

    >>> str(get_movie_by_title(u'The Matrix (1999)'))
    '0133093'

    >>> str(get_movie_by_title(u'Little Egypt (1951)'))
    '0043748'

    >>> str(get_movie_by_title(u'Little Egypt (1897/I)'))
    '0214882'

    >>> get_movie_by_title(u'Little Egypt')
    None 

    >>> str(get_movie_by_title(u'"Dexter" (2006) {Father Knows Best (#1.9)}'))
    '0866567'
    '''
    params = {'s': 'tt', 'q': title}
    if not isinstance(title, bytes):
        try:
            params['q'] = unicodedata.normalize('NFKC', params['q']).encode('latin-1')
        except:
            params['q'] = params['q'].encode('utf-8')
    params = urlencode(params)
    url = "http://www.imdb.com/find?" + params
    data = read_url(url, timeout=timeout, unicode=True)
    #if search results in redirect, get id of current page
    r = '<meta property="og:url" content="http://www.imdb.com/title/tt(\d+)/" />'
    results = re.compile(r).findall(data)    
    if results:
        return results[0]
    return None
 
def get_movie_id(title, director='', year='', timeout=-1):
    '''
    >>> str(get_movie_id('The Matrix'))
    '0133093'

    >>> str(get_movie_id('2 or 3 Things I Know About Her', 'Jean-Luc Godard'))
    '0060304'

    >>> str(get_movie_id('2 or 3 Things I Know About Her', 'Jean-Luc Godard', '1967'))
    '0060304'

    >>> str(get_movie_id(u"Histoire(s) du cinema: Le controle de l'univers", u'Jean-Luc Godard'))
    '0179214'

    >>> str(get_movie_id(u"Histoire(s) du cinéma: Le contrôle de l'univers", u'Jean-Luc Godard'))
    '0179214'

    '''
    imdbId = {
        (u'Le jour se l\xe8ve', u'Marcel Carn\xe9'): '0031514',
        (u'Wings', u'Larisa Shepitko'): '0061196',
        (u'The Ascent', u'Larisa Shepitko'): '0075404',
        (u'Fanny and Alexander', u'Ingmar Bergman'): '0083922',
        (u'Torment', u'Alf Sj\xf6berg'): '0036914',
        (u'Crisis', u'Ingmar Bergman'): '0038675',
        (u'To Joy', u'Ingmar Bergman'): '0043048',
        (u'Humain, trop humain', u'Louis Malle'): '0071635',
        (u'Place de la R\xe9publique', u'Louis Malle'): '0071999',
        (u'God\u2019s Country', u'Louis Malle'): '0091125',
        (u'Flunky, Work Hard', u'Mikio Naruse'): '0022036',
        (u'The Courtesans of Bombay', u'Richard Robbins') : '0163591',
        (u'Je tu il elle', u'Chantal Akerman') : '0071690',
        (u'Hotel Monterey', u'Chantal Akerman') : '0068725',
        (u'No Blood Relation', u'Mikio Naruse') : '023261',
        (u'Apart from You', u'Mikio Naruse') : '0024214',
        (u'Every-Night Dreams', u'Mikio Naruse') : '0024793',
        (u'Street Without End', u'Mikio Naruse') : '0025338',
        (u'Sisters of the Gion', u'Kenji Mizoguchi') : '0027672',
        (u'Osaka Elegy', u'Kenji Mizoguchi') : '0028021',
        (u'Blaise Pascal', u'Roberto Rossellini') : '0066839',
        (u'Japanese Girls at the Harbor', u'Hiroshi Shimizu') : '0160535',
        (u'The Private Life of Don Juan', u'Alexander Korda') : '0025681',
        (u'Last Holiday', u'Henry Cass') : '0042665',
        (u'A Colt Is My Passport', u'Takashi  Nomura') : '0330536',
        (u'Androcles and the Lion', u'Chester Erskine') : '0044355',
        (u'Major Barbara', u'Gabriel Pascal') : '0033868',
        (u'Come On Children', u'Allan King') : '0269104',

        (u'Jimi Plays Monterey & Shake! Otis at Monterey', u'D. A. Pennebaker and Chris Hegedus') : '',
        (u'Martha Graham: Dance on Film', u'Nathan Kroll') : '',
        (u'Carmen', u'Carlos Saura'): '0085297',
        (u'The Story of a Cheat', u'Sacha Guitry'): '0028201',
        (u'Weekend', 'Andrew Haigh'): '1714210',
    }.get((title, director), None)
    if imdbId:
        return imdbId
    params = {'s': 'tt', 'q': title}
    if director:
        params['q'] = u'"%s" %s' % (title, director)
    if year:
        params['q'] = u'"%s (%s)" %s' % (title, year, director)
    google_query = "site:imdb.com %s" % params['q']
    if not isinstance(params['q'], bytes):
        try:
            params['q'] = unicodedata.normalize('NFKC', params['q']).encode('latin-1')
        except:
            params['q'] = params['q'].encode('utf-8')
    params = urlencode(params)
    url = "http://www.imdb.com/find?" + params
    #print url

    data = read_url(url, timeout=timeout, unicode=True)
    #if search results in redirect, get id of current page
    r = '<meta property="og:url" content="http://www.imdb.com/title/tt(\d+)/" />'
    results = re.compile(r).findall(data)    
    if results:
        return results[0]
    #otherwise get first result
    r = '<td valign="top">.*?<a href="/title/tt(\d+)/"'
    results = re.compile(r).findall(data)
    if results:
        return results[0]

    #print((title, director), ": '',")
    #print(google_query)
    #results = google.find(google_query, timeout=timeout)
    results = duckduckgo.find(google_query, timeout=timeout)
    if results:
        for r in results[:2]:
            imdbId = find_re(r[1], 'title/tt(\d+)')
            if imdbId:
                return imdbId
    #or nothing
    return ''

def get_movie_poster(imdbId):
    '''
    >>> get_movie_poster('0133093')
    'http://ia.media-imdb.com/images/M/MV5BMjEzNjg1NTg2NV5BMl5BanBnXkFtZTYwNjY3MzQ5._V1._SX338_SY475_.jpg'
    '''
    info = ImdbCombined(imdbId)
    if 'posterId' in info:
        poster = info['posterId']
        if '@._V' in poster:
            poster = poster.split('@._V')[0] + '@.jpg'
        return poster
    elif 'series' in info:
        return get_movie_poster(info['series'])
    return ''

def get_episodes(imdbId, season=None):
    episodes = {}
    url = 'http://www.imdb.com/title/tt%s/episodes' % imdbId
    if season:
        url += '?season=%d' % season
        data = cache.read_url(url).decode()
        for e in re.compile('<div data-const="tt(\d+)".*?>.*?<div>S(\d+), Ep(\d+)<\/div>\n<\/div>', re.DOTALL).findall(data):
            episodes['S%02dE%02d' % (int(e[1]), int(e[2]))] = e[0]
    else:
        data = cache.read_url(url)
        match = re.compile('<strong>Season (\d+)</strong>').findall(data)
        if match:
            for season in range(1, int(match[0]) + 1):
               episodes.update(get_episodes(imdbId, season))
    return episodes

def max_votes():
    url = 'http://www.imdb.com/search/title?num_votes=500000,&sort=num_votes,desc'
    data = cache.read_url(url).decode('utf-8', 'ignore')
    votes = max([
        int(v.replace(',', ''))
        for v in re.compile('<span name="nv" data-value="(\d+)"').findall(data)
    ])
    return votes

def guess(title, director='', timeout=-1):
    return get_movie_id(title, director, timeout=timeout)

if __name__ == "__main__":
    import json
    print(json.dumps(Imdb('0306414'), indent=2))
    #print json.dumps(Imdb('0133093'), indent=2)

