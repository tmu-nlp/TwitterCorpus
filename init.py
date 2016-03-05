'''
python3 init.py public_data.txt urls.txt oauth_key.ini
'''

import sys
import requests
from requests_oauthlib import OAuth1
from configparser import ConfigParser

__author__ = 'ryosukee'
__date__ = '2016/03/05'


def get_auth():
    config = ConfigParser()
    config.read(oauthf)
    auth = [config['Key'][k] for k in ['CK', 'CS', 'AT', 'AS']]
    return OAuth1(*auth)


def make_url2tweet():
    api = 'https://api.twitter.com/1.1/statuses/lookup.json'
    auth = get_auth()
    template = 'https://twitter.com/{name}/status/{id}'
    url2tweet = dict()
    ids = list()
    for line in open(urlf):
        ids.append(line.strip().split('/')[-1])
        if len(ids) == 100:
            r = requests.get(api, params={'id': ','.join(ids)}, auth=auth)
            if r.status_code != 200:
                print('some error occurred in twitter api')
                exit()
            for item in r.json():
                url = template.format(id=item['id'], name=item['user']['screen_name'])
                # remove line break
                url2tweet[url] = item['text'].replace('\n', '')
            ids = list()
    r = requests.get(api, params={'id': ','.join(ids)}, auth=auth)
    if r.status_code != 200:
        print('some error occurred')
        return
    for item in r.json():
        url = template.format(id=item['id'], name=item['user']['screen_name'])
        # remove line break
        url2tweet[url] = item['text'].replace('\n', '')
    return url2tweet


if __name__ == '__main__':
    if len(sys.argv) == 1:
        pubf = 'public_data.txt'
        urlf = 'urls.txt'
        oauthf = 'OAuthKey.ini'
    else:
        pubf = sys.argv[1]
        urlf = sys.argv[2]
        oauthf = sys.argv[3]
    outf = open('annotated.txt', 'w')

    bot = '/'.join(['__BOT__', '補助記号'])
    eot = '/'.join(['__EOT__', '補助記号'])

    url2tweet = make_url2tweet()

    # output annotated data
    for line, url in zip(open(pubf), open(urlf)):
        url = url.strip()
        line = line.strip()
        if url not in url2tweet:
            continue
        print(bot, file=outf)
        text = url2tweet[url]
        for i, content in enumerate(line.split(',')):
            i = i + 1
            # sep
            if i % 2 == 1:
                sep = int(content)
                if sep == -1:
                    output = ['']
                    continue
                else:
                    output = [text[:sep]]
                    text = text[sep:]
            # pos
            else:
                if content != '-1':
                    output.append(content)
                print('/'.join(output), file=outf)
        print(eot, file=outf)
    outf.close()
