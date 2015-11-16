#!/usr/bin/env python
# -*- coding:utf-8 -*-

from HTMLParser import HTMLParser
import urllib2, random, requests

#from bs4 import BeautifulSoup


class s163Parser(HTMLParser):
    """The login module is authored by hxer.

    """

    def __init__(self):
        self.processing = None
        self.key = ['-s', '-p', '-k']
        self.value = []
        self.time = ''
        self.data = ''
        self.config = {
            'url': 'socks163.com',
        }
        self.httpInit()
        HTMLParser.__init__(self)

    def httpInit(self):
        self.session = requests.Session()
        self.headers =  {
            "User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:42.0) Gecko/20100101 Firefox/42.0",
            "Connection": "keep-alive"
        }
        # default username and password
        self.payload = {
            "username": "s163",
            "password": "socks163",
        }

    def login(self, user='', passwd=''):
        if user and passwd:
            self.payload['username'] = user
            self.payload['password'] = passwd
        url = "http://www.socks163.com/user.php?action=login"
        try:
            response = self.session.post(url, headers=self.headers, data=self.payload)
        except Exception:
            return None
        else:
            return response.content

    def handle_starttag(self, tag, attrs):
        if not self.processing and tag == 'tbody':
            self.processing = 'tbody'
        if tag == 'th' and self.processing == 'tbody':
            self.processing = 'th'

    def handle_endtag(self, tag):
        if tag == 'tbody':
            self.processing = 'done'
        if tag == 'th':
            self.processing = 'tbody'
            self.value.append(self.data)
            self.data = ''

    def handle_data(self, data):
        if self.processing == 'th':
            self.data += data

    def get_config(self):
        page = self.login()
        if page:
            self.feed(page)
            # self.config['time'] = self.value[9]
            for k, v in zip(self.key, self.value[6:9]):
                self.config[k] = v
        return self.config


class issParser(HTMLParser):

    def __init__(self):
        self.processing = None
        self.code = [{}, {}, {}]
        self.key = ['s', 'p', 'k', 'm']
        self.cnt = 0
        self.time = ''
        self.data = ''
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'h4':
            self.processing = True

    def handle_endtag(self, tag):
        if tag == 'h4':
            if ':' in self.data and '状态' not in self.data:
                self.code[self.cnt/4][self.key[self.cnt%4]] = self.data.strip().split(':')[-1]
                self.cnt += 1
            self.data = ''
            self.processing = None

    def handle_data(self, data):
        if self.processing:
            self.data += data

    def get_config(self):
        try:
            url = urllib2.urlopen('http://www.ishadowsocks.com')
        except urllib2.URLError:
            return None
        else:
            self.feed(url.read())
            return self.code


if __name__ == '__main__':
    cparser = s163Parser()
    print cparser.get_config()

