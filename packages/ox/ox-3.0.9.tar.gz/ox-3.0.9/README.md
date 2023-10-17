# python-ox - the web in a dict

## Depends:

 - python >= 2.7 or python3 >= 3.4
 - python-chardet (http://chardet.feedparser.org/)
 - python-feedparser (http://www.feedparser.org/)
 - python-lxml (http://codespeak.net/lxml/)          [optional]
 - django (otherwise dates < 1900 are not supported) [optional]

## Usage:

    import ox

    data = ox.cache.read_url('http:/...')
    text = ox.strip_tags(data)
    ox.normalize_newlines(text)
    ox.format_bytes(len(data))

    ox.format_bytes(1234567890)
    '1.15 GB'

    import ox.web.imdb
    imdbId = ox.web.imdb.guess('The Matrix')
    info = ox.web.imdb.Imdb(imdbId)
    info['year']
    1999


## Install:

    python setup.py install


## Cookies:

some ox.web modules require user accont information or cookies to work,
those are saved in ~/.ox/auth.json, most basic form looks like this:

    {
        "key": "value"
    }

## Tests:

 nosetests --with-doctest ox
 nosetests3 --with-doctest ox
