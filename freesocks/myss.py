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
    parser = OptionParser('usage: freesocks [OPTION]...', version='0.1.5')
    parser.add_option('-l', dest='local_port', metavar='LOCAL_PORT', type='int', default=1080, help='local binding port, default: 1080')
    parser.add_option('-t', dest='timeout', metavar='TIMEOUT', type='int', default=300, help='timeout for sslocal in seconds, default: 300')
    # parser.add_option('-r', dest='refresh', metavar='REFRESH', type='int', default=5, help='proxy test interval in seconds, default: 5')
    option, _ = parser.parse_args()

    while True:
        print 'trying to collect passwords...'
        tag = False
        while True:
            configs = s163Parser().get_config()
            if len(configs) < 4:
                if not tag:
                    print 'connection to %s failed' % configs['url']
                    print 'reconnecting...'
                tag = True
                if is_exit:
                    sys.exit()
                time.sleep(2)
            else:
                print 'fetched data from %s' % configs['url']
                break


        configs['-l'] = str(option.local_port)
        configs['-t'] = str(option.timeout)

        # start_time = time.strptime(configs['time'], '%Y-%m-%d %X')
        # end_time = time.gmtime(time.mktime(start_time) + 3600 * 9)        # convert to UTC+8

        print 'trying to connect the server %s ...' % configs['-s']

        args = ['sslocal'] + list(reduce(lambda x, y: x + y, filter(lambda (x, y): x.startswith('-'), configs.iteritems())))

        try:
            p = subprocess.Popen(args, stdout=subprocess.PIPE)
        except:
            print 'something wrong with sslocal'
            continue
        print 'connection established'
        # print 'password is to be refreshed at ' + time.strftime('%X', end_time)

        while True:
            time.sleep(0.5)
            if is_exit:
                print '\ntrying to stop...'
                p.terminate()
                print 'freesocks stopped'
                sys.exit()
            # if time.localtime() >= end_time:
            #     p.terminate()
            #     break

        time.sleep(1)


if __name__ == '__main__':
    main()

