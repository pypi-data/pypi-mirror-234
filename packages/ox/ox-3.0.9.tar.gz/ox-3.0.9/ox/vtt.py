# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import codecs

import ox
from . import srt

def _webvtt_timecode(t):
    return ox.format_duration(t * 1000, years=False)


def encode(data, webvtt=False):
    """Encodes subtitles into WebVTT format

    data: list of dicts with 'in', 'out': float and 'value': unicode

    Returns: a UTF-8-encoded bytestring

    >>> encode([{'in': 1.25, 'out': 60 * 60 + 1, 'value': u'touch\\u00E9'}])
    '\\xef\\xbb\\xbfWEBVTT\\r\\n\\r\\n1\\r\\n00:00:01.250 --> 01:00:01.000\\r\\ntouch\\xc3\\xa9\\r\\n\\r\\n'
    """
    srt = u'WEBVTT\r\n\r\n'

    for i, s in enumerate(data, 1):
        srt += '%d\r\n%s --> %s\r\n%s\r\n\r\n' % (
            i,
            _webvtt_timecode(s['in']),
            _webvtt_timecode(s['out']),
            s['value'].replace('\n', '\r\n').strip()
        )

    return codecs.BOM_UTF8 + srt.encode('utf-8')

def load(filename, offset=0):
    '''Parses vtt file

    filename: path to an vtt file
    offset (float, seconds): shift all in/out points by offset

    Returns list with dicts that have in, out, value and id
    '''
    return srt.load(filename, offset)
