#!/usr/bin/env python2.7
from urllib import quote
from argparse import ArgumentParser
import urllib2
import sys
import json
import re

API = "YouDaoCV"
API_KEY = "659600698"


class Colorizing(object):
    colors = {
        'none': "",
        'default': "\033[0m",
        'bold': "\033[1m",
        'underline': "\033[4m",
        'blink': "\033[5m",
        'reverse': "\033[7m",
        'concealed': "\033[8m",

        'black': "\033[30m",
        'red': "\033[31m",
        'green': "\033[32m",
        'yellow': "\033[33m",
        'blue': "\033[34m",
        'magenta': "\033[35m",
        'cyan': "\033[36m",
        'white': "\033[37m",

        'on_black': "\033[40m",
        'on_red': "\033[41m",
        'on_green': "\033[42m",
        'on_yellow': "\033[43m",
        'on_blue': "\033[44m",
        'on_magenta': "\033[45m",
        'on_cyan': "\033[46m",
        'on_white': "\033[47m",

        'beep': "\007",
    }

    @classmethod
    def colorize(cls, s, color=None):
        if color in cls.colors:
            return u"{0}{1}{2}".format(
                cls.colors[color], s, cls.colors['default'])
        else:
            return s


def online_resources(query):

    english = re.compile(r'^[a-z]+$', re.IGNORECASE)
    chinese = re.compile(ur'^[\u4e00-\u9fff]+$', re.UNICODE)

    res_list = [
        (english, 'http://www.ldoceonline.com/search/?q={0}'),
        (english, 'http://dictionary.reference.com/browse/{0}'),
        (english, 'http://www.urbandictionary.com/define.php?term={0}'),
        (chinese, 'http://www.zdic.net/sousuo/?q={0}')
    ]

    return [url.format(quote(query.encode('utf-8')))
            for lang, url in res_list if lang.match(query) is not None]


def print_explanation(data, print_full_web_exp=False):
    _c = Colorizing.colorize
    _w = sys.stdout.write
    _d = data
    has_result = False

    query = _d['query']
    _w(_c(query, 'underline'))

    if 'basic' in _d:
        has_result = True
        basic = _d['basic']
        if 'phonetic' in basic:
            _w(u" [{0}]\n".format(_c(basic['phonetic'], 'yellow')))
        else:
            _w(u"\n")

        _w(_c(u'  Word Explanation:\n', 'cyan'))
        if 'explains' in basic:
            for e in basic['explains']:
                _w(u"     * {0}\n".format(e))
        else:
            _w(u"\n")

    elif 'translation' in _d:
        has_result = True
        _w(_c(u'\n  Translation:\n', 'cyan'))
        for t in _d['translation']:
            _w(u"     * {0}\n".format(t))
    else:
        _w(u"\n")

    if 'web' in _d:
        has_result = True
        _w(_c(u'\n  Web Reference:\n', 'cyan'))

        web = _d['web'] if print_full_web_exp else _d['web'][:3]
        for ref in web:
            _w(u'     * {0}\n'.format(_c(ref['key'], 'yellow')))
            _w(u'       {0}\n'.format(
                u"; ".join([_c(e, 'magenta') for e in ref['value']])))

    if not has_result:
        _w(_c(' -- No result for this query.\n', 'red'))

    ol_res = online_resources(query)
    if len(ol_res) > 0:
        _w(_c(u'\n  Online Resource:\n', 'cyan'))
        res = ol_res if print_full_web_exp else ol_res[:1]
        map(lambda u: _w('     * {0}\n'.format(u)), res)

    _w('\n')

if __name__ == "__main__":
    parser = ArgumentParser(description="Youdao Console Version")
    parser.add_argument('-f', '--full',
                        action="store_true",
                        default=False,
                        help="print full web reference, only the first 3 "
                             "results will be printed without this flag.")
    parser.add_argument('words', nargs='+', help=
                        "words to lookup, or quoted sentences to translate.")

    options = parser.parse_args()

    for word in options.words:
        word = quote(word)
        data = urllib2.urlopen(
            "http://fanyi.youdao.com/openapi.do?"
            "keyfrom=%s&key=%s&type=data&doctype=json"
            "&version=1.1&q=%s"
            % (API, API_KEY, word)).read().decode("utf-8")
        print_explanation(json.loads(data), print_full_web_exp=options.full)
