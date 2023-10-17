import re

import requests

def parse_url(url):
    params = url.split('downloads/')[1].split('/')
    file_id, recipient_id, security_hash = '', '', ''
    if len(params) > 2:
        # https://www.wetransfer.com/downloads/XXXXXXXXXX/YYYYYYYYY/ZZZZZZZZ
        file_id, recipient_id, security_hash = params
    else:
        # The url is similar to https://www.wetransfer.com/downloads/XXXXXXXXXX/ZZZZZZZZ
        file_id, security_hash = params
    return file_id, recipient_id, security_hash


def get_download_link(url):
    with requests.session() as s:
        r = s.get(url)
        url = r.url
        file_id, recipient_id, security_hash = parse_url(url)
        content = r.text
        token = re.compile('<meta name="csrf-token" content="(.*?)" />').findall(content)[0]
        api_url = 'https://wetransfer.com/api/v4/transfers/{file_id}/download'.format(file_id=file_id)
        r = s.post(api_url, json={"security_hash": security_hash}, headers={'X-CSRF-Token': token})
        link = r.json()['direct_link']
        return link

