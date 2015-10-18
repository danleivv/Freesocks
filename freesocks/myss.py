#!/usr/bin/env python
# -*- coding:utf-8 -*-
from HTMLParser import HTMLParser
from optparse import OptionParser
import urllib2, json, random, sys, time, subprocess, signal


class codeParser(HTMLParser):

    def __init__(self):
        self.handledtags = ['code', 'p']
        self.processing = None
        self.code = [{}, {}, {}]
        self.key = ['server', 'server_port', 'password', 'method']
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

def signal_handle(signum, frame):
    global is_exit
    is_exit = True

signal.signal(signal.SIGINT, signal_handle)
signal.signal(signal.SIGTERM, signal_handle)

is_exit = False

def main():
    while True:
        parser = codeParser()
        print 'trying to collect passwords...'
        tag = False
        while True:
            try:
                url = urllib2.urlopen('http://www.socks163.com')
            except urllib2.URLError:
                if not tag:
                    print 'connection to socks163.com failed'
                    print 'reconnecting...'
                tag = True
                if is_exit:
                    sys.exit()
                time.sleep(2)
            else:
                print 'received response from socks163.com'
                parser.feed(url.read())
                break


        config = parser.code[random.randint(0, 2)]
        config['local_port'] = 1080
        config['timeout'] = 300
        if len(sys.argv) > 1:
            config['local_port'] = int(sys.argv[1])
        json.dump(config, open('config.json', 'w'))

        start_date = '-'.join(map(lambda x: x[-4:], parser.time[0].split('-')))

        start_time = time.strptime(start_date + ' ' + parser.time[1], '%Y-%m-%d %X')
        end_time = time.gmtime(time.mktime(start_time) + 3600 * 9)        # convert to UTC+8

        print 'password was posted at ' + time.strftime('%X', start_time)
        print 'trying to connect the server %s ...' % config['server']
        try:
            p = subprocess.Popen('sslocal', stdout=subprocess.PIPE)
        except:
            print 'something wrong with sslocal'
            continue
        print 'connection established'
        print 'password is to be refresh at ' + time.strftime('%X', end_time)

        while True:
            time.sleep(0.5)
            if is_exit:
                print '\ntrying to stop...'
                p.terminate()
                print 'done'
                sys.exit()
            if time.localtime() >= end_time:
                print time.localtime()
                p.terminate()
                break

        time.sleep(1)

if __name__ == '__main__':
    main()
