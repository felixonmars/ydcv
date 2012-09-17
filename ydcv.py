#!/usr/bin/env python2
from urllib import quote
import urllib2, sys, json

API="YouDaoCV"
API_KEY="659600698"

class Colorizing(object):
    colors = { 
            'none' : "", 
            'default' : "\033[0m", 
            'bold' : "\033[1m", 
            'underline' : "\033[4m", 
            'blink' : "\033[5m", 
            'reverse' : "\033[7m", 
            'concealed' : "\033[8m", 

            'black' : "\033[30m", 
            'red' : "\033[31m", 
            'green' : "\033[32m", 
            'yellow' : "\033[33m", 
            'blue' : "\033[34m", 
            'magenta' : "\033[35m", 
            'cyan' : "\033[36m", 
            'white' : "\033[37m", 

            'on_black' : "\033[40m", 
            'on_red' : "\033[41m", 
            'on_green' : "\033[42m", 
            'on_yellow' : "\033[43m", 
            'on_blue' : "\033[44m", 
            'on_magenta' : "\033[45m", 
            'on_cyan' : "\033[46m", 
            'on_white' : "\033[47m", 

            'beep' : "\007", 
            } 

    @classmethod
    def colorize(cls, s, color = None):
        if color in cls.colors:
            return u"{0}{1}{2}".format(cls.colors[color], s, cls.colors['default'])
        else:
            return s


def print_explanation(data):
    _c = Colorizing.colorize
    _w = sys.stdout.write
    d = data

    _w(_c(d['query'], 'underline'))

    if 'phonetic' in d['basic']:
        _w(u" [{0}]\n".format(_c(d['basic']['phonetic'], 'yellow')))
    else:
        _w(u"\n")

    if 'explains' in d['basic']:
        for e in d['basic']['explains']:
            _w(u"   - {0}\n".format(e))

    if 'web' in d:
        _w(_c(u'\nWeb Reference:\n', 'cyan'))

        for ref in d['web']:
            _w(u"   * {0}\n".format(_c(ref['key'], 'yellow')))
            _w(u'    ')
            for e in ref['value']:
                _w(u" {0};".format(_c(e, 'magenta')))
            _w('\n')

if len(sys.argv) < 2:
    print "Usage:", sys.argv[0], "<words>"
else:
    for word in sys.argv[1:]:
        word = quote(word)
        data = urllib2.urlopen("http://fanyi.youdao.com/openapi.do?keyfrom=%s&key=%s&type=data&doctype=json&version=1.1&q=%s" % (API, API_KEY, word)).read().decode("utf-8")
        print_explanation(json.loads(data))

