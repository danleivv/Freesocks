#!/usr/bin/env python
# -*- coding:utf-8 -*-
from HTMLParser import HTMLParser
from optparse import OptionParser
import urllib2, json, random, sys, time, subprocess, signal

def signal_handle(signum, frame):
    global is_exit
    is_exit = True

signal.signal(signal.SIGINT, signal_handle)
signal.signal(signal.SIGTERM, signal_handle)

is_exit = False


class codeParser(HTMLParser):

    def __init__(self):
        self.handledtags = ['code', 'p']
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


def main():
    parser = OptionParser('usage: freesocks [OPTION]...', version='0.1.3')
    parser.add_option('-l', dest='local_port', metavar='LOCAL_PORT', type='int', default=1080, help='local binding port, default: 1080')
    parser.add_option('-t', dest='timeout', metavar='TIMEOUT', type='int', default=300, help='timeout in seconds, default: 300')
    parser.add_option('-r', dest='refresh', metavar='REFRESH', type='int', default=3600, help='refresh interval in seconds, default: 3600')
    option, _ = parser.parse_args()

    while True:
        cparser = codeParser()
        print 'trying to collect passwords...'
        tag = False
        while True:
            config = cparser.get_config()
            if not config:
                if not tag:
                    print 'connection to socks163.com failed'
                    print 'reconnecting...'
                tag = True
                if is_exit:
                    sys.exit()
                time.sleep(2)
            else:
                print 'received response from socks163.com'
                break

        config['l'] = str(option.local_port)
        config['t'] = str(option.timeout)

        start_date = '-'.join(map(lambda x: x[-4:], cparser.time[0].split('-')))

        start_time = time.strptime(start_date + ' ' + cparser.time[1], '%Y-%m-%d %X')
        end_time = time.gmtime(time.mktime(start_time) + 3600 * 9)        # convert to UTC+8
        refresh_time = time.gmtime(time.mktime(time.localtime()) + 3600 * 8 + option.refresh)

        print 'password was posted at ' + time.strftime('%X', start_time)
        print 'trying to connect the server %s ...' % config['s']

        args = ['sslocal']
        for key in config.keys():
            args += ['-' + key] + [config[key]]

        try:
            p = subprocess.Popen(args, stdout=subprocess.PIPE)
        except:
            print 'something wrong with sslocal'
            continue
        print 'connection established'
        print 'password is to be refreshed at ' + time.strftime('%X', end_time)

        while True:
            time.sleep(0.5)
            if is_exit:
                print '\ntrying to stop...'
                p.terminate()
                print 'done'
                sys.exit()
            if time.localtime() >= end_time or time.localtime() >= refresh_time:
                p.terminate()
                break

        time.sleep(1)

if __name__ == '__main__':
    main()
