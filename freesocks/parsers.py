#!/usr/bin/env python
# -*- coding:utf-8 -*-

from HTMLParser import HTMLParser
import urllib2, random

class s163Parser(HTMLParser):

    def __init__(self):
        # self.handledtags = ['code', 'p']
        self.processing = None
        self.code = [{}, {}, {}]
        self.key = ['s', 'p', 'k', 'm']
        self.cnt = 0
        self.time = ''
        self.data = ''
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'code':
            self.processing = 'code'
        if tag == 'p' and len(attrs) > 0:
            self.processing = 'p'

    def handle_endtag(self, tag):
        if tag == self.processing:
            if tag == 'code':
                self.code[self.cnt/4][self.key[self.cnt%4]] = self.data.strip()
                self.cnt += 1
            if tag == 'p':
                self.time = self.data.strip().split()
            self.data = ''
            self.processing = None

    def handle_data(self, data):
        if self.processing:
            self.data += data

    def get_config(self):
        try:
            url = urllib2.urlopen('http://www.socks163.com')
        except urllib2.URLError:
            return None
        else:
            self.feed(url.read())
            config = self.code[random.randint(0, 2)]
            return config

    def __str__(self):
        return 'socks163.com'


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

    def __str__(self):
        return 'ishadowsocks.com'


if __name__ == '__main__':
    cparser = issParser()
    print cparser.get_config()

