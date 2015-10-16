#!/usr/bin/env python
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
                self.time = self.data.strip().split()[-1]
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
        url = urllib2.urlopen('http://www.socks163.com')
        parser.feed(url.read())
        config = parser.code[random.randint(0, 2)]
        config['local_port'] = 1080
        config['timeout'] = 300
        if len(sys.argv) > 1:
            config['local_port'] = int(sys.argv[1])
        json.dump(config, open('config.json', 'w'))
        now = time.localtime()[3:6]
        nxt = map(int, parser.time.split(':'))
        nxt[0] += 1
        print 'password was posted at ' + parser.time
        print 'trying to connect...'
        p = subprocess.Popen('sslocal', stdout=subprocess.PIPE)
        print 'connection succeed'
        print 'password is to be refresh at ' + ':'.join(map(lambda x: str(x).rjust(2, '0'), nxt))
        while True:
            time.sleep(0.5)
            if is_exit:
                print '\ntrying to stop...'
                p.terminate()
                print 'done'
                sys.exit()
            now = time.localtime()[3:6]
            if now[0] == nxt[0] and now[1] == nxt[1] and now[2] == nxt[2]:
                p.terminate()
                break
        
        time.sleep(1)

if __name__ == '__main__':
    main()
