#!/usr/bin/env python
# -*- coding:utf-8 -*-

from parsers import *
from optparse import OptionParser
import json, sys, time, subprocess, signal, random

def signal_handle(signum, frame):
    global is_exit
    is_exit = True

signal.signal(signal.SIGINT, signal_handle)
signal.signal(signal.SIGTERM, signal_handle)

is_exit = False


def main():
    parser = OptionParser('usage: freesocks [OPTION]...', version='0.1.4')
    parser.add_option('-l', dest='local_port', metavar='LOCAL_PORT', type='int', default=1080, help='local binding port, default: 1080')
    parser.add_option('-t', dest='timeout', metavar='TIMEOUT', type='int', default=300, help='timeout for sslocal in seconds, default: 300')
    parser.add_option('-r', dest='refresh', metavar='REFRESH', type='int', default=5, help='proxy test interval in seconds, default: 5')
    option, _ = parser.parse_args()

    configs = None

    while True:

        tag = False
        while True:
            if not configs:
                if not tag:
                    print 'trying to collect passwords...'
                else:
                    print 'reconnecting...'
                configs = issParser().get_config()
                tag = True
                if is_exit:
                    sys.exit()
                time.sleep(2)
            else:
                print 'received response'
                break

        config = configs[random.randint(0, 2)]
        config['l'] = str(option.local_port)
        config['t'] = str(option.timeout)


        print 'trying to connect the server %s ...' % config['s']

        args = ['sslocal'] + reduce(lambda x, y: x + y, map(lambda x: ['-' + x, config[x]], config.keys()))

        try:
            p = subprocess.Popen(args, stdout=subprocess.PIPE)
        except:
            print 'something wrong with sslocal'
            continue
        print 'connection established'

        while True:
            for i in range(option.refresh * 2):
                time.sleep(0.5)
                if is_exit:
                    print '\ntrying to stop...'
                    p.terminate()
                    print 'freesocks stopped'
                    sys.exit()
            configs = issParser().get_config()
            if config['k'] not in map(lambda x: x['k'], configs):
                p.terminate()
                break


if __name__ == '__main__':
    main()

